# tests/conftest.py

"""
tests.conftest
==============

Shared fixtures/helpers for bvillage tests.

Goals
-----
- Keep tests Blender-free (no bpy imports).
- Produce minimal valid core model objects (StructurePlan, OpeningsPlan, InteriorPlan).
- Ensure deterministic, readable test setup.

Units: meters.
"""

from __future__ import annotations

import pytest

from bvillage.core.seed import Seed
from bvillage.core.model import (
    Context,
    Footprint,
    Grid,
    FieldCell,
    BayFrame,
    WallSegment,
    ReservedSlot,
    StructurePlan,
    Opening,
    OpeningsPlan,
    InteriorPlan,
    Room,
    Door,
)


@pytest.fixture
def ctx() -> Context:
    return Context(
        seed=Seed(123),
        region="north",
        epoch_band="late_medieval",
        settlement_type="village",
        wealth=0.6,
        occupants=4,
        climate_hint="temperate",
        house_type="fachwerkhaus.hallenhaus",
    )


def make_structure(
    *,
    L: float = 10.0,
    W: float = 4.0,
    z0: float = 0.0,
    H_e: float = 2.5,
) -> StructurePlan:
    """
    Minimal StructurePlan with:
    - rectangular footprint
    - minimal grid
    - 4 exterior wall segments with consistent IDs
    """
    fp = Footprint(length=L, width=W, orientation_deg=0.0)

    # Minimal grid: two axes each, one field cell
    axes_u = (-L / 2.0, L / 2.0)
    axes_v = (-W / 2.0, W / 2.0)
    fields = (FieldCell(id="F_0_0", bbox=(-L / 2.0, -W / 2.0, L / 2.0, W / 2.0), tags=()),)
    grid = Grid(axes_u=axes_u, axes_v=axes_v, fields=fields)

    frames = (BayFrame(id="BINDER_0", bay_index=0, tags=("PRIMARY_FRAME",)),)

    walls = (
        WallSegment("W_N_0", "N", (-L / 2.0, L / 2.0), (z0, H_e), ("EXTERIOR", "WINDOW_OK")),
        WallSegment("W_S_0", "S", (-L / 2.0, L / 2.0), (z0, H_e), ("EXTERIOR", "WINDOW_OK", "GATE_OK")),
        WallSegment("W_E_0", "E", (-W / 2.0, W / 2.0), (z0, H_e), ("EXTERIOR",)),
        WallSegment("W_W_0", "W", (-W / 2.0, W / 2.0), (z0, H_e), ("EXTERIOR",)),
    )

    return StructurePlan(
        footprint=fp,
        stories=1,
        grid=grid,
        frames=frames,
        walls=walls,
        reserved_slots=(ReservedSlot("HEARTH_ZONE", "F_0_0", ("HEARTH_ZONE",)),),
        notes={},
    )


def make_openings_plan(*openings: Opening) -> OpeningsPlan:
    return OpeningsPlan(openings=tuple(openings), notes={})


def opening(
    *,
    oid: str,
    typ: str,
    wall_id: str,
    u0: float,
    u1: float,
    z0: float,
    z1: float,
) -> Opening:
    return Opening(
        id=oid,
        type=typ,  # Literal in model, but tests keep it simple
        wall_id=wall_id,
        u_range=(u0, u1),
        z_range=(z0, z1),
        tags=(),
        animation={},
    )


def make_interior_plan(*, room_ids: tuple[str, ...] = ("R0",), connected: bool = True) -> InteriorPlan:
    rooms = tuple(Room(id=rid, type="generic", field_ids=("F_0_0",), story=0, tags=()) for rid in room_ids)
    doors: tuple[Door, ...] = ()
    if connected and len(room_ids) >= 2:
        doors = (
            Door(id="D0", between=(room_ids[0], room_ids[1]), wall_ref="W_S_0", width=0.9, z_range=(0.0, 2.0), tags=("INTERIOR_DOOR",)),
        )
    return InteriorPlan(rooms=rooms, doors=doors, zones=(), opening_demands=(), notes={})
