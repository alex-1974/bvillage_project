# bvillage/types/fachwerkhaus/hallenhaus/architect.py

"""
bvillage.types.fachwerkhaus.hallenhaus.architect
================================================

Type Orchestration: Fachwerkhaus – Hallenhaus

ARC-001A hardened rules
-----------------------
- The type orchestrator must NOT invent structural defaults.
- All culturally/structurally meaningful knobs come from the layered PolicyStack
  (ResolvedPolicy.fachwerk + constraints).
- Blender layer should consume artifacts and must not set defaults (next step).

Artifacts produced
------------------
- core.resolved_policy        (debuggable policy snapshot)
- policy_trace                (layer trace with values)
- core.constraints            (sampled/penalized values for key constraints)
- core.house_params           (renderer-facing params: roof_pitch_deg, post_section, dims)
- fachwerk.frameplan          (structural truth: members, openings frames, braces, infills)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, Final, Tuple, Optional

from bvillage.core.errors import SchemaError
from bvillage.core.model import (
    Context,
    StructurePlan,
    Footprint,
    BayFrame,
    WallSegment,
    ReservedSlot,
    Issue,
)
from bvillage.core.grid import build_rect_grid
from bvillage.core.notes import set_domain_artifact

from bvillage.core.constraints import (
    RangeHard,
    RangeSoft,
    CostProfile,
    eval_range,
    sample_soft,
)

from bvillage.core.policy_stack import resolve_policy_stack_with_trace
from bvillage.core.policy_types import (
    ResolvedPolicy,
    ConstraintSpec,
    RangeHardSpec,
    RangeSoftSpec,
)

from bvillage.domains.fachwerk.core.frameplan import (
    build_frameplan,
    FramePolicy,
    frameplan_to_dict,
    frameplan_report,
)

from bvillage.types.fachwerkhaus.hallenhaus.planner import plan_interior
from bvillage.types.fachwerkhaus.hallenhaus.openings import plan_openings

logger = logging.getLogger(__name__)


# ============================================================
# Dims
# ============================================================

@dataclass(frozen=True, slots=True)
class HallenhausDims:
    L: float = 19.9
    W: float = 6.9
    H_e: float = 2.58
    z0: float = 0.0


DEFAULT_DIMS: Final[HallenhausDims] = HallenhausDims()


# ============================================================
# Cost Profiles (scoring lenses)
# ============================================================

_DEFAULT_COST_PROFILES: Final[Tuple[CostProfile, ...]] = (
    CostProfile(name="auth", mode="quadratic", outside_allowed_step=3.0),
    CostProfile(name="risk", mode="quadratic", outside_allowed_step=6.0),
    CostProfile(name="complexity", mode="linear", outside_allowed_step=2.0),
)


# ============================================================
# Helpers
# ============================================================

def _issue_to_dict(i: Issue) -> Dict[str, Any]:
    return {
        "code": i.code,
        "severity": i.severity,
        "message": i.message,
        "related_ids": list(i.related_ids),
        "suggested_repairs": list(i.suggested_repairs),
    }


def _hard_from_spec(h: Optional[RangeHardSpec]) -> Optional[RangeHard]:
    if h is None:
        return None
    return RangeHard(float(h.min_v), float(h.max_v))


def _soft_from_spec(s: Optional[RangeSoftSpec]) -> Optional[RangeSoft]:
    if s is None:
        return None
    return RangeSoft(
        ideal=(float(s.ideal[0]), float(s.ideal[1])),
        allowed=(float(s.allowed[0]), float(s.allowed[1])),
        weight=float(s.weight),
    )


def _policy_to_dict(pol: ResolvedPolicy) -> Dict[str, Any]:
    c_out: Dict[str, Any] = {}
    for k, spec in pol.constraints.items():
        c_out[k] = {
            "unit": spec.unit,
            "code_prefix": spec.code_prefix,
            "hard": None if spec.hard is None else {"min_v": spec.hard.min_v, "max_v": spec.hard.max_v},
            "soft": None if spec.soft is None else {
                "ideal": [spec.soft.ideal[0], spec.soft.ideal[1]],
                "allowed": [spec.soft.allowed[0], spec.soft.allowed[1]],
                "weight": spec.soft.weight,
            },
        }

    fw = pol.fachwerk
    return {
        "schema": pol.schema,
        "fachwerk": {
            "binder_max": fw.binder_max,
            "default_jamb_thickness": fw.default_jamb_thickness,
            "post_section_width": fw.post_section_width,
            "post_section_depth": fw.post_section_depth,
            "plate_section_width": fw.plate_section_width,
            "plate_section_depth": fw.plate_section_depth,
            "opening_jamb_width": fw.opening_jamb_width,
            "opening_jamb_depth": fw.opening_jamb_depth,
            "braces_enable": fw.braces_enable,
            "brace_section_width": fw.brace_section_width,
            "brace_section_depth": fw.brace_section_depth,
            "brace_min_cell_width": fw.brace_min_cell_width,
            "brace_min_cell_height": fw.brace_min_cell_height,
            "target_gefach_width": fw.target_gefach_width,
            "target_gefach_jitter": fw.target_gefach_jitter,
            "z_merge_tol": fw.z_merge_tol,
            "roof_pitch_deg": fw.roof_pitch_deg,
            "post_section": [fw.post_section[0], fw.post_section[1]],
        },
        "constraints": c_out,
    }


def _attach_policy_trace_artifact(structure: StructurePlan, trace) -> None:
    structure.notes["policy_trace"] = {
        "schema": trace.schema,
        "layers": [
            {
                "layer_id": layer.layer_id,
                "ops": [{"key": op.key, "value": op.value} for op in layer.ops],
            }
            for layer in trace.layers
        ],
    }


def _attach_resolved_policy_artifact(structure: StructurePlan, pol: ResolvedPolicy) -> None:
    set_domain_artifact(
        structure.notes,
        domain="core",
        artifact="resolved_policy",
        payload=_policy_to_dict(pol),
        legacy_aliases=("resolved_policy", "core.resolved_policy", "policy"),
    )


def _require_constraint(pol: ResolvedPolicy, name: str) -> ConstraintSpec:
    spec = pol.constraints.get(name)
    if spec is None:
        raise SchemaError(f"ResolvedPolicy missing required constraint: {name}")
    return spec


def _require_soft(spec: ConstraintSpec, name: str) -> RangeSoft:
    soft = _soft_from_spec(spec.soft)
    if soft is None:
        raise SchemaError(f"Constraint {name} requires soft spec for sampling/targeting.")
    return soft


def _attach_house_params_artifact(structure: StructurePlan, pol: ResolvedPolicy) -> None:
    """
    Renderer-facing parameters that must be present downstream (no Blender defaults).

    ARC-001A:
    - No setdefault / no magic defaults in Blender.
    - Derive geometric heights deterministically from StructurePlan.walls.
    - Pull policy-driven knobs from ResolvedPolicy.fachwerk.
    """
    fw = pol.fachwerk
    fp = structure.footprint

    # ---- derive z0 / z_plate deterministically from walls ----
    z0_min: float | None = None
    z1_max: float | None = None

    walls = getattr(structure, "walls", None)
    if not isinstance(walls, (list, tuple)) or not walls:
        raise SchemaError("Cannot derive z0/z_plate: StructurePlan.walls missing/invalid.")

    for w in walls:
        try:
            zr = getattr(w, "z_range", None)
            if not (isinstance(zr, (list, tuple)) and len(zr) == 2):
                continue
            z0w = float(zr[0])
            z1w = float(zr[1])
        except Exception:
            continue

        z0_min = z0w if z0_min is None else min(z0_min, z0w)
        z1_max = z1w if z1_max is None else max(z1_max, z1w)

    if z0_min is None or z1_max is None:
        raise SchemaError("Cannot derive z0/z_plate: no valid wall.z_range entries found.")

    if not (z1_max > z0_min):
        raise SchemaError(f"Invalid derived heights: z0={z0_min} z_plate={z1_max}.")

    # ---- policy-driven knobs ----
    roof_pitch_deg = float(getattr(fw, "roof_pitch_deg"))
    post_w, post_d = fw.post_section

    # plate_section tuple (for Blender convenience) derived from policy scalars
    plate_section = (float(fw.plate_section_width), float(fw.plate_section_depth))

    # roof_overhang: deterministic geometric heuristic (NOT a hidden constant default in Blender)
    # Tuned so W≈6.9m -> ~0.35m, and clamped to sane bounds.
    W = float(fp.width)
    roof_overhang = max(0.25, min(0.45, 0.05 * W))

    payload = {
        "schema": 1,
        # geometry
        "L": float(fp.length),
        "W": float(fp.width),
        "z0": float(z0_min),
        "z_plate": float(z1_max),
        # policy-driven / renderer-facing
        "roof_pitch_deg": roof_pitch_deg,
        "roof_overhang": float(roof_overhang),
        "post_section": [float(post_w), float(post_d)],
        "plate_section": [float(plate_section[0]), float(plate_section[1])],
    }

    set_domain_artifact(
        structure.notes,
        domain="core",
        artifact="house_params",
        payload=payload,
        legacy_aliases=("house_params", "core.house_params"),
    )


def _attach_constraints_artifact(ctx: Context, structure: StructurePlan, pol: ResolvedPolicy) -> None:
    """
    Attach constraint-derived parameters and penalty summaries.

    ARC-001A hardening:
    - Required constraints must exist.
    - If we sample/derive from ideal, the constraint must define soft.
    - No local fallback constants.
    """
    out_params: Dict[str, Any] = {}

    # Fully-qualified sampling namespace (RNG label only; constraint keys remain un-prefixed)
    ns = f"{ctx.house_type}."

    # ---- brustriegel_z (sampled) ----
    spec = _require_constraint(pol, "brustriegel_z")
    soft = _require_soft(spec, "brustriegel_z")
    hard = _hard_from_spec(spec.hard)

    z_brust = sample_soft(ctx, key=f"{ns}brustriegel_z", soft=soft)

    ev = eval_range(
        ctx,
        name="brustriegel_z",
        value=z_brust,
        hard=hard,
        soft=soft,
        profiles=_DEFAULT_COST_PROFILES,
        unit=spec.unit,
        code_prefix=spec.code_prefix,
    )

    out_params["brustriegel_z"] = {
        "value": float(ev.value),
        "penalties": dict(ev.penalties),
        "issues": [_issue_to_dict(x) for x in ev.issues],
        "range_hard": None if hard is None else [hard.min_v, hard.max_v],
        "range_soft": {
            "ideal": [soft.ideal[0], soft.ideal[1]],
            "allowed": [soft.allowed[0], soft.allowed[1]],
            "weight": soft.weight,
        },
        "key": f"{ns}brustriegel_z",
    }

    # ---- gefach_width_target (sampled) ----
    spec = _require_constraint(pol, "gefach_width_target")
    soft = _require_soft(spec, "gefach_width_target")
    hard = _hard_from_spec(spec.hard)

    target = sample_soft(ctx, key=f"{ns}gefach_width_target", soft=soft)

    ev = eval_range(
        ctx,
        name="gefach_width_target",
        value=target,
        hard=hard,
        soft=soft,
        profiles=_DEFAULT_COST_PROFILES,
        unit=spec.unit,
        code_prefix=spec.code_prefix,
    )

    out_params["gefach_width_target"] = {
        "value": float(ev.value),
        "penalties": dict(ev.penalties),
        "issues": [_issue_to_dict(x) for x in ev.issues],
        "range_hard": None if hard is None else [hard.min_v, hard.max_v],
        "range_soft": {
            "ideal": [soft.ideal[0], soft.ideal[1]],
            "allowed": [soft.allowed[0], soft.allowed[1]],
            "weight": soft.weight,
        },
        "key": f"{ns}gefach_width_target",
    }

    payload = {
        "schema": 2,
        "profiles": [p.name for p in _DEFAULT_COST_PROFILES],
        "params": out_params,
    }

    set_domain_artifact(
        structure.notes,
        domain="core",
        artifact="constraints",
        payload=payload,
        legacy_aliases=("constraints", "core.constraints"),
    )


# ============================================================
# Structure (semantic)
# ============================================================

def plan_structure(ctx: Context, *, dims: HallenhausDims = DEFAULT_DIMS) -> StructurePlan:
    L = float(dims.L)
    W = float(dims.W)
    H_e = float(dims.H_e)
    z0 = float(dims.z0)

    grid = build_rect_grid(L, W, bays_x=8, bays_y=2)

    frames = tuple(
        BayFrame(id=f"BINDER_{i}", bay_index=i, tags=("PRIMARY_FRAME",))
        for i in range(len(grid.axes_u))
    )

    half_L = L / 2.0
    half_W = W / 2.0

    walls = (
        WallSegment("W_N_0", "N", (-half_L, half_L), (z0, H_e), ("EXTERIOR", "WINDOW_OK")),
        WallSegment("W_S_0", "S", (-half_L, half_L), (z0, H_e), ("EXTERIOR", "WINDOW_OK", "GATE_OK")),
        WallSegment("W_E_0", "E", (-half_W, half_W), (z0, H_e), ("EXTERIOR",)),
        WallSegment("W_W_0", "W", (-half_W, half_W), (z0, H_e), ("EXTERIOR",)),
    )

    reserved = (ReservedSlot("HEARTH_ZONE", "F_2_1", ("HEARTH_ZONE",)),)

    footprint = Footprint(length=L, width=W, orientation_deg=0.0)

    return StructurePlan(
        footprint=footprint,
        stories=1,
        grid=grid,
        frames=frames,
        walls=walls,
        reserved_slots=reserved,
        notes={},
    )


# ============================================================
# Domain hookup (fachwerk)
# ============================================================

def _frame_policy_from_resolved(pol: ResolvedPolicy) -> FramePolicy:
    """
    Map ResolvedPolicy.fachwerk -> fachwerk FramePolicy.

    ARC-001A hardening:
    - no defaults here; this is a pure mapping.
    """
    fw = pol.fachwerk
    return FramePolicy(
        binder_max=float(fw.binder_max),
        default_jamb_thickness=float(fw.default_jamb_thickness),
        post_section_width=float(fw.post_section_width),
        post_section_depth=float(fw.post_section_depth),
        plate_section_width=float(fw.plate_section_width),
        plate_section_depth=float(fw.plate_section_depth),
        opening_jamb_width=float(fw.opening_jamb_width),
        opening_jamb_depth=float(fw.opening_jamb_depth),
        braces_enable=bool(fw.braces_enable),
        brace_section_width=float(fw.brace_section_width),
        brace_section_depth=float(fw.brace_section_depth),
        brace_min_cell_width=float(fw.brace_min_cell_width),
        brace_min_cell_height=float(fw.brace_min_cell_height),
        target_gefach_width=float(fw.target_gefach_width),
        target_gefach_jitter=float(fw.target_gefach_jitter),
        z_merge_tol=float(fw.z_merge_tol),
    )


def derive_frameplan(
    ctx: Context,
    structure: StructurePlan,
    openings,
    resolved: ResolvedPolicy,
) -> None:
    frame_policy = _frame_policy_from_resolved(resolved)

    fp = build_frameplan(
        structure=structure,
        openings=openings,
        policy=frame_policy,
        seed=int(ctx.seed.derive("fachwerk.frameplan.jitter")),
    )

    payload = frameplan_to_dict(fp)

    set_domain_artifact(
        structure.notes,
        domain="fachwerk",
        artifact="frameplan",
        payload=payload,
        legacy_aliases=("frameplan", "fachwerk.frameplan"),
    )

    logger.info("%s", frameplan_report(fp))


# ============================================================
# Orchestration
# ============================================================

def orchestrate_house(ctx: Context):
    logger.debug(
        "Hallenhaus.orchestrate_house() start (seed=%s wealth=%s)",
        getattr(ctx, "seed", None),
        getattr(ctx, "wealth", None),
    )

    # 1) Resolve policy stack (mandatory)
    resolved, trace = resolve_policy_stack_with_trace(ctx)

    # 2) Semantic structure plan
    structure = plan_structure(ctx)

    # 3) Persist policy artifacts
    _attach_resolved_policy_artifact(structure, resolved)
    _attach_policy_trace_artifact(structure, trace)

    # 4) Persist renderer-facing params (policy-driven)
    _attach_house_params_artifact(structure, resolved)

    # 5) Persist constraints-derived sampled values (policy-driven)
    _attach_constraints_artifact(ctx, structure, resolved)

    # 6) Semantic planning
    interior = plan_interior(ctx, structure)
    openings = plan_openings(ctx, structure, interior)

    # 7) Domain frameplan (constructive truth) from resolved policy
    derive_frameplan(ctx, structure, openings, resolved)

    logger.debug("Hallenhaus.orchestrate_house() done")
    return structure, interior, openings
