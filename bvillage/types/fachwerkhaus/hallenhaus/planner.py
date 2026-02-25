# bvillage/types/fachwerkhaus/hallenhaus/planner.py

"""
bvillage.types.fachwerkhaus.hallenhaus.planner
==============================================

Type Orchestration: Fachwerkhaus – Hallenhaus

Responsibilities
----------------
- Generate type-specific StructurePlan
- Generate interior + openings
- Attach Fachwerk frameplan into structure.notes (standardized notes schema)

Units: meters.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Final

from bvillage.core.model import (
    Context,
    StructurePlan,
    Footprint,
    Frame,
    WallSegment,
    ReservedSlot,
)
from bvillage.core.grid import build_rect_grid
from bvillage.core.notes import set_domain_artifact

from bvillage.domains.fachwerk.core.frameplan import (
    build_frameplan,
    FramePolicy,
    frameplan_to_dict,
    frameplan_report,
)

from bvillage.types.fachwerkhaus.hallenhaus.interior import generate_interior
from bvillage.types.fachwerkhaus.hallenhaus.openings import generate_openings

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class HallenhausDims:
    L: float = 19.9
    W: float = 6.9
    H_e: float = 2.58
    z0: float = 0.0


DEFAULT_DIMS: Final[HallenhausDims] = HallenhausDims()


def generate_structure(ctx: Context, *, dims: HallenhausDims = DEFAULT_DIMS) -> StructurePlan:
    L = float(dims.L)
    W = float(dims.W)
    H_e = float(dims.H_e)
    z0 = float(dims.z0)

    grid = build_rect_grid(L, W, bays_x=8, bays_y=2)

    frames = tuple(
        Frame(id=f"BINDER_{i}", axis_index=i, tags=("PRIMARY_FRAME",))
        for i in range(len(grid.axis_x))
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


def _hallenhaus_policy(ctx: Context) -> FramePolicy:
    wealth = float(getattr(ctx, "wealth", 0.5))

    base = 1.55
    span = 0.35
    b_max = base + span * (wealth - 0.3)
    b_max = max(1.45, min(1.85, b_max))

    return FramePolicy(
        b_max=b_max,
        default_jamb_t=0.20,
    )


def attach_frameplan(ctx: Context, structure: StructurePlan, openings: Any) -> None:
    policy = _hallenhaus_policy(ctx)

    fp = build_frameplan(
        structure=structure,
        openings=openings,
        policy=policy,
    )

    payload = frameplan_to_dict(fp)

    # ✅ canonical schema + legacy aliases
    set_domain_artifact(
        structure.notes,
        domain="fachwerk",
        name="frameplan",
        payload=payload,
        legacy_aliases=("frameplan", "fachwerk.frameplan"),
    )

    logger.info("%s", frameplan_report(fp))


def generate_house(ctx: Context):
    logger.debug("Hallenhaus.generate_house() start (seed=%s wealth=%s)", getattr(ctx, "seed", None), getattr(ctx, "wealth", None))

    structure = generate_structure(ctx)
    interior = generate_interior(ctx, structure)
    openings = generate_openings(ctx, structure, interior)
    attach_frameplan(ctx, structure, openings)

    logger.debug("Hallenhaus.generate_house() done")
    return structure, interior, openings
