# bvillage/types/fachwerkhaus/hallenhaus/plan_topology.py
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from bvillage.core.errors import SchemaError
from bvillage.core.model import (
    StructurePlan,
    Footprint,
    Grid,
    FieldCell,
    BayFrame,
    WallSegment,
    ReservedSlot,
)

__all__ = ["plan_topology"]


def plan_topology(
    ctx: Any,
    resolved_policy: Any,
) -> StructurePlan:
    """
    Plan the semantic/topological Hallenhaus shell.

    Returns
    -------
    StructurePlan
        Canonical type-layer topology artifact.

    Notes
    -----
    This is intentionally a type-layer planner:
    - produces StructurePlan only
    - does not emit structural members
    """
    if getattr(ctx, "grammar", None) != "hall":
        raise SchemaError(
            f"Hallenhaus requires grammar='hall', got '{getattr(ctx, 'grammar', None)}'."
        )

    fachwerk = getattr(resolved_policy, "fachwerk", None)
    if fachwerk is None:
        raise SchemaError("plan_topology requires resolved_policy.fachwerk")

    seq = _build_frame_sequence(fachwerk)
    xs = _frame_x_positions_centered(
        seq,
        bay_width_m=float(fachwerk.bay_width),
    )
    cs = _build_cross_section(
        building_width_m=float(fachwerk.building_width),
        plate_height_m=float(fachwerk.plate_height),
    )

    return _plan_structure(seq, xs, cs)


def _build_frame_sequence(fachwerk: Any) -> Tuple[str, ...]:
    bay_count = int(getattr(fachwerk, "bay_count", 5))
    gable_mode = str(getattr(fachwerk, "gable_mode", "end_frame"))

    if bay_count < 1:
        raise SchemaError(f"Invalid fachwerk.bay_count={bay_count}; expected >= 1")

    if gable_mode != "end_frame":
        raise SchemaError(
            f"Unsupported fachwerk.gable_mode={gable_mode!r}; expected 'end_frame'"
        )

    seq: List[str] = ["GABLE_END"]
    for _ in range(bay_count - 1):
        seq.append("STRUCTURAL")
    seq.append("GABLE_END")

    return tuple(seq)


def _frame_x_positions_centered(
    seq: Tuple[str, ...],
    *,
    bay_width_m: float,
) -> Tuple[float, ...]:
    xs: List[float] = []
    x = 0.0
    for _ in seq:
        xs.append(x)
        x += bay_width_m

    center = 0.5 * (xs[0] + xs[-1])
    xs = [v - center for v in xs]
    return tuple(float(v) for v in xs)


def _build_cross_section(
    *,
    building_width_m: float,
    plate_height_m: float,
) -> Dict[str, Any]:
    half_w = 0.5 * building_width_m

    rows = (
        {"row_kind": "WALL", "y": -half_w},
        {"row_kind": "HALL", "y": 0.0},
        {"row_kind": "WALL", "y": +half_w},
    )

    return {
        "width": float(building_width_m),
        "plate_height": float(plate_height_m),
        "rows": rows,
    }


def _plan_structure(
    seq: Tuple[str, ...],
    xs: Tuple[float, ...],
    cs: Dict[str, Any],
) -> StructurePlan:
    half_w = 0.5 * float(cs["width"])
    z_plate = float(cs["plate_height"])

    frames: List[BayFrame] = []
    for i, role in enumerate(seq):
        tags = ("PRIMARY_FRAME", f"FrameRole.{role}")
        frames.append(BayFrame(id=f"F_{i+1}", bay_index=i, tags=tags))
    frames_val = tuple(frames)

    axes_u = tuple(float(x) for x in xs)
    axes_v = tuple(sorted(float(r["y"]) for r in cs["rows"]))

    fields: List[FieldCell] = []
    for ix in range(len(axes_u) - 1):
        x0 = float(axes_u[ix])
        x1 = float(axes_u[ix + 1])
        for iy in range(len(axes_v) - 1):
            y0 = float(axes_v[iy])
            y1 = float(axes_v[iy + 1])
            fields.append(
                FieldCell(
                    id=f"F_{ix}_{iy}",
                    bbox=(x0, y0, x1, y1),
                    tags=("TOPOLOGY_CELL",),
                )
            )

    grid = Grid(
        axes_u=axes_u,
        axes_v=axes_v,
        fields=tuple(fields),
    )

    umin = float(min(xs))
    umax = float(max(xs))

    walls = (
        WallSegment(
            id="W_N_0",
            side="N",
            u_range=(umin, umax),
            z_range=(0.0, z_plate),
            tags=("EXTERIOR", "WINDOW_OK"),
        ),
        WallSegment(
            id="W_S_0",
            side="S",
            u_range=(umin, umax),
            z_range=(0.0, z_plate),
            tags=("EXTERIOR", "WINDOW_OK"),
        ),
        WallSegment(
            id="W_E_0",
            side="E",
            u_range=(-half_w, +half_w),
            z_range=(0.0, z_plate),
            tags=("EXTERIOR", "GABLE_END"),
        ),
        WallSegment(
            id="W_W_0",
            side="W",
            u_range=(-half_w, +half_w),
            z_range=(0.0, z_plate),
            tags=("EXTERIOR", "GABLE_END"),
        ),
    )

    reserved = (
        ReservedSlot(id="HEARTH_ZONE", field_id="F_2_1", tags=("HEARTH_ZONE",)),
    )

    length = float(abs(xs[-1] - xs[0]))
    footprint = Footprint(
        length=length,
        width=float(cs["width"]),
        orientation_deg=0.0,
    )

    return StructurePlan(
        footprint=footprint,
        stories=1,
        grid=grid,
        frames=frames_val,
        walls=walls,
        reserved_slots=reserved,
        notes={},
    )
