# bvillage/types/fachwerkhaus/hallenhaus/architect.py

from __future__ import annotations

import logging
from dataclasses import is_dataclass
from typing import Any, Dict, List, Tuple

from bvillage.core.errors import SchemaError
from bvillage.core.notes import set_domain_artifact, get_domain_artifact
from bvillage.core.model import (
    StructurePlan,
    Footprint,
    Grid,
    BayFrame,
    WallSegment,
    ReservedSlot,
)

from bvillage.core.policy_stack import resolve_policy_stack_with_trace
from bvillage.types.fachwerkhaus.hallenhaus.contracts.schema_frameplan_langhaus import (
    SCHEMA_VERSION_LANGHAUS,
)
from bvillage.domains.fachwerk.contracts.validate_frameplan_fachwerk import (
    validate_frameplan_fachwerk_schema,
    validate_frameplan_fachwerk_domain,
)
from bvillage.types.fachwerkhaus.hallenhaus.contracts.validate_frameplan_type import (
    validate_frameplan_langhaus_type,
)

from bvillage.domains.fachwerk.validation.frameplan_checks import (
    run_arch_checks,
    log_arch_checks,
)

from bvillage.core.ontology.structural_terms import (
    POST_OPENING_JAMB,
    BEAM_OPENING_LINTEL,
    BRACE_KNEE,
)

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Small helpers (no guessing, no signature drift)
# -----------------------------------------------------------------------------

def _safe_to_payload(obj: Any) -> Any:
    """
    Convert policy objects (often slots-based) into JSON-ish payloads without
    relying on __dict__ / vars().
    """
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, (list, tuple)):
        return [ _safe_to_payload(x) for x in obj ]
    if isinstance(obj, dict):
        return { str(k): _safe_to_payload(v) for k, v in obj.items() }

    # dataclass(slots=True) or similar
    if is_dataclass(obj):
        out: Dict[str, Any] = {}
        for f in getattr(obj, "__dataclass_fields__", {}).keys():
            try:
                out[f] = _safe_to_payload(getattr(obj, f))
            except Exception:
                out[f] = "<unreadable>"
        return out

    # slots objects
    slots = getattr(obj, "__slots__", None)
    if slots:
        out = {}
        for s in slots:
            try:
                out[str(s)] = _safe_to_payload(getattr(obj, s))
            except Exception:
                out[str(s)] = "<unreadable>"
        return out

    # last resort: repr
    return repr(obj)


def _member_id(prefix: str, *parts: object) -> str:
    return prefix + "_" + "_".join(str(p) for p in parts)


# -----------------------------------------------------------------------------
# Zimmermannslogik (type-level planning inputs)
# -----------------------------------------------------------------------------

def _build_frame_sequence(seed: int) -> Tuple[str, ...]:
    """
    Returns frame roles along the longitudinal axis (x).
    v0.4.0 MVP: 6 frames, gable ends exist, gate is gable-end (opening),
    so all interior frames are structural.
    """
    # Deterministic MVP (seed currently unused; kept for later jitter/variants)
    return ("GABLE_END", "STRUCTURAL", "STRUCTURAL", "STRUCTURAL", "STRUCTURAL", "GABLE_END")


def _frame_x_positions_centered(seq: Tuple[str, ...]) -> Tuple[float, ...]:
    """
    Returns x positions for each frame, centered around x=0 (building center).
    """
    bay_m = 3.645  # DEBUG constant for v0.4.0 (replaced by policy ranges later)

    xs: List[float] = []
    x = 0.0
    for _ in seq:
        xs.append(x)
        x += bay_m

    # center at 0: midpoint between first and last frame
    center = 0.5 * (xs[0] + xs[-1])
    xs = [v - center for v in xs]
    return tuple(float(v) for v in xs)


def _build_cross_section() -> Dict[str, Any]:
    """
    Cross section specification for a 3-row (3-aisled) Hallenhaus skeleton.
    """
    width_m = 7.2
    z_plate_m = 2.6
    halfW = 0.5 * width_m

    # Option B: explicit row_kind + y coordinate
    rows = (
        {"row_kind": "WALL", "y": -halfW},
        {"row_kind": "HALL", "y": 0.0},
        {"row_kind": "WALL", "y": +halfW},
    )

    return {
        "width": float(width_m),
        "plate_height": float(z_plate_m),
        "rows": rows,
    }


def _zimmermann_payload(seq: Tuple[str, ...], xs: Tuple[float, ...], cs: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema": 1,
        "x_frames": tuple(float(x) for x in xs),
        "cross_section_rows": tuple({"row_kind": r["row_kind"], "y": float(r["y"])} for r in cs["rows"]),
        "frame_roles": tuple({"bay_index": int(i), "role": str(role)} for i, role in enumerate(seq)),
    }


# -----------------------------------------------------------------------------
# Semantic StructurePlan shell (type-level output)
# -----------------------------------------------------------------------------

def plan_structure(ctx: Any, seq: Tuple[str, ...], xs: Tuple[float, ...], cs: Dict[str, Any]) -> StructurePlan:
    halfW = 0.5 * float(cs["width"])
    z_plate = float(cs["plate_height"])

    # Frames
    frames: List[BayFrame] = []
    for i, role in enumerate(seq):
        tags = ("PRIMARY_FRAME", f"FrameRole.{role}")
        frames.append(BayFrame(id=f"F_{i+1}", bay_index=i, tags=tags))

    frames_val = tuple(frames)

    # Minimal grid (v0.4.0: builder derives axes from frameplan.zimmermann; grid may be empty)
    grid = Grid(axes_u=(), axes_v=(), fields=())

    # Walls: long sides N/S (run along x), gable ends E/W (run along y)
    umin = float(min(xs))
    umax = float(max(xs))

    walls = (
        WallSegment(id="W_N_0", side="N", u_range=(umin, umax), z_range=(0.0, z_plate), tags=("EXTERIOR", "WINDOW_OK")),
        WallSegment(id="W_S_0", side="S", u_range=(umin, umax), z_range=(0.0, z_plate), tags=("EXTERIOR", "WINDOW_OK")),
        WallSegment(id="W_E_0", side="E", u_range=(-halfW, +halfW), z_range=(0.0, z_plate), tags=("EXTERIOR", "GABLE_END")),
        WallSegment(id="W_W_0", side="W", u_range=(-halfW, +halfW), z_range=(0.0, z_plate), tags=("EXTERIOR", "GABLE_END")),
    )

    # Reserved slots (keep one consistent placeholder for planner/debug)
    reserved = (
        ReservedSlot(id="HEARTH_ZONE", field_id="F_2_1", tags=("HEARTH_ZONE",)),
    )

    length = float(abs(xs[-1] - xs[0]))
    footprint = Footprint(length=length, width=float(cs["width"]), orientation_deg=0.0)

    return StructurePlan(
        footprint=footprint,
        stories=1,
        grid=grid,
        frames=frames_val,
        walls=walls,
        reserved_slots=reserved,
        notes={},  # artifacts attached via notes.py
    )


# -----------------------------------------------------------------------------
# FramePlan v4: members-first XYZ skeleton (writes artifact)
# -----------------------------------------------------------------------------

def derive_frameplan_rohskelett(
    ctx: Any,
    structure: StructurePlan,
    seq: Tuple[str, ...],
    xs: Tuple[float, ...],
    cs: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Emits:
      - fachwerk.frameplan artifact
      - includes zimmermann block required by downstream builders
    """
    width = float(cs["width"])
    z_plate = float(cs["plate_height"])
    halfW = 0.5 * width
    z0 = 0.0

    posts: List[Dict[str, Any]] = []
    rails: List[Dict[str, Any]] = []
    braces: List[Dict[str, Any]] = []

    # --- Primary posts (3 rows per frame: S wall, hall, N wall) ---
    for i, x in enumerate(xs):
        role = seq[i]

        posts.append(
            {
                "id": _member_id("P", i, "S"),
                "tid": "post.primary",
                "role": "post.outer",
                "p0": (float(x), -halfW, z0),
                "p1": (float(x), -halfW, z_plate),
                "tags": ("ROW_WALL", f"FRAME_{i}", f"FrameRole.{role}"),
            }
        )
        posts.append(
            {
                "id": _member_id("P", i, "H"),
                "tid": "post.hall",
                "role": "post.hall",
                "p0": (float(x), 0.0, z0),
                "p1": (float(x), 0.0, z_plate),
                "tags": ("ROW_HALL", f"FRAME_{i}", f"FrameRole.{role}"),
            }
        )
        posts.append(
            {
                "id": _member_id("P", i, "N"),
                "tid": "post.primary",
                "role": "post.outer",
                "p0": (float(x), +halfW, z0),
                "p1": (float(x), +halfW, z_plate),
                "tags": ("ROW_WALL", f"FRAME_{i}", f"FrameRole.{role}"),
            }
        )

    # --- Eaves plates along long walls (N/S) ---
    for i in range(len(xs) - 1):
        x0 = float(xs[i])
        x1 = float(xs[i + 1])

        rails.append(
            {
                "id": _member_id("PL", "S", i),
                "tid": "beam.plate",
                "role": "plate.eaves",
                "p0": (x0, -halfW, z_plate),
                "p1": (x1, -halfW, z_plate),
                "tags": ("WALL_S",),
            }
        )
        rails.append(
            {
                "id": _member_id("PL", "N", i),
                "tid": "beam.plate",
                "role": "plate.eaves",
                "p0": (x0, +halfW, z_plate),
                "p1": (x1, +halfW, z_plate),
                "tags": ("WALL_N",),
            }
        )

    # --- Minimal primary knee braces (debug baseline) ---
    # (Later: proper bracing per bay, gate frame reinforcement, gable-specific bracing)
    bid = 0
    for i in range(len(xs) - 1):
        x0 = float(xs[i])
        x1 = float(xs[i + 1])
        braces.append(
            {
                "id": _member_id("BR", bid),
                "tid": BRACE_KNEE,
                "role": "brace.knee",
                "p0": (x0, -halfW, z_plate * 0.30),
                "p1": (x1, -halfW, z_plate * 0.80),
                "tags": ("WALL_S",),
            }
        )
        bid += 1

    # --- Gate on gable end (MVP): jamb posts + lintel on W_E_0 ---
    # Convention: gable end wall "E" is at x = max(xs) (positive x end).
    # Opening runs along y (local transverse axis).
    gate_x = float(max(xs))
    gate_clear_w = 3.0
    gate_half = 0.5 * gate_clear_w
    gate_z1 = 2.2

    posts.append(
        {
            "id": _member_id("OJ", "GATE", "L"),
            "tid": POST_OPENING_JAMB,
            "role": "opening.jamb",
            "p0": (gate_x, -gate_half, z0),
            "p1": (gate_x, -gate_half, gate_z1),
            "tags": ("OPENING_GATE", "GABLE_END", "WALL_E"),
        }
    )
    posts.append(
        {
            "id": _member_id("OJ", "GATE", "R"),
            "tid": POST_OPENING_JAMB,
            "role": "opening.jamb",
            "p0": (gate_x, +gate_half, z0),
            "p1": (gate_x, +gate_half, gate_z1),
            "tags": ("OPENING_GATE", "GABLE_END", "WALL_E"),
        }
    )
    rails.append(
        {
            "id": _member_id("OL", "GATE"),
            "tid": BEAM_OPENING_LINTEL,
            "role": "opening.lintel",
            "p0": (gate_x, -gate_half, gate_z1),
            "p1": (gate_x, +gate_half, gate_z1),
            "tags": ("OPENING_GATE", "GABLE_END", "WALL_E"),
        }
    )
    
    frame_layout = {
        "x_frames": [float(x) for x in xs],
        "y_rows": [float(r["y"]) for r in cs["rows"]],
        "frame_roles": [str(role) for role in seq],
    }

    frameplan: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION_LANGHAUS,

        "coordinate_system": {
            "origin": "building_center_ground",
            "axes": {
                "x": "longitudinal_forward",
                "y": "right_when_facing_positive_x",
                "z": "up",
            },
            "units": "meters",
        },

        "basis": {
            "z0": float(z0),
            "z_plate": float(z_plate),
        },

        "frame_layout": frame_layout,

        "zimmermann": _zimmermann_payload(seq, xs, cs),

        "members": {
            "posts": posts,
            "rails": rails,
            "braces": braces,
            "infills": [],
        },

        "openings": [],

        "notes": {
            "mvp": True,
            "gate": {"placement": "gable_end", "wall": "W_E_0"},
        },
}

    set_domain_artifact(structure.notes, domain="fachwerk", artifact="frameplan", payload=frameplan)
    set_domain_artifact(structure.notes, domain="fachwerk", artifact="zimmermann", payload=frameplan["zimmermann"])

    return frameplan


# -----------------------------------------------------------------------------
# Orchestrator (type entry point)
# -----------------------------------------------------------------------------

def orchestrate_house(ctx: Any):
    # Grammar guard
    if getattr(ctx, "grammar", None) != "hall":
        raise SchemaError(f"Hallenhaus requires grammar='hall', got '{getattr(ctx, 'grammar', None)}'.")

    logger.debug("Hallenhaus.orchestrate_house() start (seed=%s)", getattr(ctx, "seed", None))

    # 1) Resolve policy stack (kept for pipeline integrity / artifacts)
    resolved, trace = resolve_policy_stack_with_trace(ctx)

    # 2) Zimmermannslogik: frame sequence + cross section
    seq = _build_frame_sequence(seed=int(getattr(getattr(ctx, "seed", None), "derive")("hallenhaus.bays") if getattr(ctx, "seed", None) else 0))
    xs = _frame_x_positions_centered(seq)
    cs = _build_cross_section()

    # 3) Semantic structure shell
    structure = plan_structure(ctx, seq, xs, cs)

    # 4) Persist policy artifacts (debuggable; no vars()/__dict__ assumptions)
    set_domain_artifact(
        structure.notes,
        domain="core",
        artifact="resolved_policy",
        payload={"schema": 1, "resolved": _safe_to_payload(resolved)},
    )
    set_domain_artifact(
        structure.notes,
        domain="core",
        artifact="policy_trace",
        payload={"schema": 1, "trace": _safe_to_payload(trace)},
    )

    # 5) Emit v4 roh-skeleton frameplan (members-first + zimmermann payload)
    frameplan = derive_frameplan_rohskelett(ctx, structure, seq, xs, cs)

    # 6) ARCH CHECKS
    issues = run_arch_checks(frameplan)
    log_arch_checks(logger, frameplan, issues)
    if any(i.severity == "HARD" for i in issues):
        raise SchemaError("Architect checks failed (hard issues).")

    # 6b) Canonical full validation
    validate_frameplan_fachwerk_schema(frameplan)
    validate_frameplan_fachwerk_domain(frameplan)
    validate_frameplan_langhaus_type(frameplan)

    # 7) Keep return shape stable
    from bvillage.types.fachwerkhaus.hallenhaus.planner import plan_interior
    from bvillage.types.fachwerkhaus.hallenhaus.openings import plan_openings

    interior = plan_interior(ctx, structure)
    openings = plan_openings(ctx, structure, interior)

    return structure, interior, openings
