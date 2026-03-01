# bvillage/types/fachwerkhaus/hallenhaus/planner.py

"""
bvillage.types.fachwerkhaus.hallenhaus.planner
==============================================

Type Orchestration: Fachwerkhaus – Hallenhaus

Responsibilities
----------------
- Generate type-specific StructurePlan (semantic)
- Generate interior + openings (semantic)
- Resolve policy stack (ctx -> ResolvedPolicy) and store as notes artifact
- Attach constraints-derived parameters + penalty info as notes artifact (core)
- Attach Fachwerk frameplan into structure.notes (fachwerk domain artifact)

Layer rules
-----------
- No Blender imports.
- Planner consumes ResolvedPolicy only (no hidden structural defaults).
- StructurePlan is frozen; only mutate structure.notes dict via notes schema helpers.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, Final, Tuple, Optional

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
from bvillage.core.policy_types import ResolvedPolicy, ConstraintSpec, RangeHardSpec, RangeSoftSpec

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
# NOTE:
# These are scoring "lenses" (auth/risk/complexity). They don't change geometry directly.
# If you want *zero* defaults in planners, move them into ResolvedPolicy later.
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
    # keep it explicit + stable for debugging; no dataclass.asdict to avoid surprises
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

    return {
        "schema": pol.schema,
        "fachwerk": {
            "binder_max": pol.fachwerk.binder_max,
            "default_jamb_thickness": pol.fachwerk.default_jamb_thickness,
        },
        "constraints": c_out,
    }

def _attach_policy_trace_artifact(structure, trace):
    structure.notes["policy_trace"] = {
        "schema": trace.schema,
        "layers": [
            {
                "layer_id": layer.layer_id,
                "keys": [op.key for op in layer.ops],
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


def _attach_constraints_artifact(ctx: Context, structure: StructurePlan, pol: ResolvedPolicy) -> None:
    """
    Attach constraint-derived parameters and penalty summaries into notes schema.

    We sample only when a soft range exists; otherwise we store a fixed value if the
    planner already chose it (future extension).
    """
    out_params: Dict[str, Any] = {}

    # ---- brustriegel_z (sampled) ----
    spec = pol.constraints.get("brustriegel_z")
    if spec is not None and spec.soft is not None:
        soft = _soft_from_spec(spec.soft)
        hard = _hard_from_spec(spec.hard)

        # deterministic sample
        z_brust = sample_soft(ctx, key="hallenhaus.brustriegel_z", soft=soft)

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
            "key": "hallenhaus.brustriegel_z",
        }

    # ---- gefach_width_target (sampled around ideal center, or fixed if no soft) ----
    spec = pol.constraints.get("gefach_width_target")
    if spec is not None:
        hard = _hard_from_spec(spec.hard)
        soft = _soft_from_spec(spec.soft)

        if soft is not None:
            # Sample within ideal most of the time.
            target = sample_soft(ctx, key="hallenhaus.gefach_width_target", soft=soft)
        else:
            # Fallback (should be avoided long-term): choose mid of hard if present, else 1.35.
            if hard is not None:
                target = 0.5 * (hard.min_v + hard.max_v)
            else:
                target = 1.35

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
            "range_soft": None if soft is None else {
                "ideal": [soft.ideal[0], soft.ideal[1]],
                "allowed": [soft.allowed[0], soft.allowed[1]],
                "weight": soft.weight,
            },
            "key": "hallenhaus.gefach_width_target" if soft is not None else None,
        }

    payload = {
        "schema": 1,
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

def _frame_policy_from_resolved(resolved_policy) -> FramePolicy:
    """
    Map ResolvedPolicy -> domain FramePolicy (fachwerk).
    Keep this mapping explicit to avoid defaults creeping into the domain.
    """
    # Try common layout: resolved_policy.fachwerk.* (dataclass or namespace)
    fw = getattr(resolved_policy, "fachwerk", resolved_policy)

    def g(name: str, default):
        v = getattr(fw, name, None)
        return default if v is None else v

    return FramePolicy(
        binder_max=float(g("binder_max", 2.40)),
        default_jamb_thickness=float(g("default_jamb_thickness", 0.20)),
        horizontal_axes_style=list(g("horizontal_axes_style", [0.0, 0.9, 1.6, 2.2])),

        z_merge_tol=float(g("z_merge_tol", FramePolicy(binder_max=0.0).z_merge_tol)),
        z_band_min=float(g("z_band_min", 0.15)),
        z_band_target_min=float(g("z_band_target_min", 0.25)),

        width_type=g("width_type", "axis"),

        profile_post_w=float(g("profile_post_w", 0.20)),
        profile_post_d=float(g("profile_post_d", 0.20)),
        profile_plate_w=float(g("profile_plate_w", 0.18)),
        profile_plate_d=float(g("profile_plate_d", 0.18)),

        profile_opening_jamb_w=float(g("profile_opening_jamb_w", 0.18)),
        profile_opening_jamb_d=float(g("profile_opening_jamb_d", 0.18)),

        profile_opening_lintel_gate_w=float(g("profile_opening_lintel_gate_w", 0.20)),
        profile_opening_lintel_gate_d=float(g("profile_opening_lintel_gate_d", 0.20)),
        profile_opening_lintel_window_w=float(g("profile_opening_lintel_window_w", 0.16)),
        profile_opening_lintel_window_d=float(g("profile_opening_lintel_window_d", 0.18)),
        profile_opening_sill_w=float(g("profile_opening_sill_w", 0.16)),
        profile_opening_sill_d=float(g("profile_opening_sill_d", 0.18)),

        braces_enable=bool(g("braces_enable", True)),
        brace_profile_w=float(g("brace_profile_w", 0.12)),
        brace_profile_d=float(g("brace_profile_d", 0.12)),
        brace_min_cell_w=float(g("brace_min_cell_w", 0.80)),
        brace_min_cell_h=float(g("brace_min_cell_h", 0.80)),

        target_gefach_w=float(g("target_gefach_w", 1.35)),
        target_gefach_jitter=float(g("target_gefach_jitter", 0.10)),
    )
    
def derive_frameplan(
    ctx: Context,
    structure: StructurePlan,
    openings,
    resolved: ResolvedPolicy,
) -> None:
    """
    Build and attach Fachwerk FramePlan domain artifact.

    No structural defaults allowed here.
    Mapping ResolvedPolicy → FramePolicy is explicit and centralized.
    """

    # 1) Map resolved policy → domain policy
    frame_policy = _frame_policy_from_resolved(resolved)

    # 2) Build deterministic frameplan
    fp = build_frameplan(
        structure=structure,
        openings=openings,
        policy=frame_policy,
        seed=int(ctx.seed.derive("fachwerk.frameplan.jitter")),
    )

    # 3) Persist artifact
    payload = frameplan_to_dict(fp)

    set_domain_artifact(
        structure.notes,
        domain="fachwerk",
        artifact="frameplan",
        payload=payload,
        legacy_aliases=("frameplan", "fachwerk.frameplan"),
    )

    # 4) Human-readable report
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

    structure = plan_structure(ctx)

    # 2) Persist resolved policy for debugging + downstream consumers
    _attach_resolved_policy_artifact(structure, resolved)
    _attach_policy_trace_artifact(structure, trace)

    # 3) Attach constraints-derived parameters early (independent of interior/openings)
    _attach_constraints_artifact(ctx, structure, resolved)

    # 4) Semantic planning
    interior = plan_interior(ctx, structure)
    openings = plan_openings(ctx, structure, interior)

    # 5) Domain frameplan (constructive truth) from resolved policy
    derive_frameplan(ctx, structure, openings, resolved)

    logger.debug("Hallenhaus.orchestrate_house() done")
    return structure, interior, openings
