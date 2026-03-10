# bvillage/types/timber_frame/longhouse/planner.py

from __future__ import annotations
from typing import List, Tuple
from bvillage.core.model import (
    Context, StructurePlan, InteriorPlan,
    Zone, Room, Door, OpeningDemand
)


def _field_id(ix: int, iy: int) -> str:
    return f"F_{ix}_{iy}"


def _range_fields(ix0: int, ix1_excl: int, iy0: int, iy1_excl: int) -> List[str]:
    ids: List[str] = []
    for ix in range(ix0, ix1_excl):
        for iy in range(iy0, iy1_excl):
            ids.append(_field_id(ix, iy))
    return ids


def plan_interior(ctx: Context, structure: StructurePlan) -> InteriorPlan:
    """
    Hallenhaus MVP interior:
      - Diele dominates mid section
      - Stall at rear
      - Stube on one side near front
      - Simple door graph: Stube <-> Diele <-> Stall
    """

    bays_x = len(structure.grid.axes_u) - 1  # 8 in your current run
    bays_y = len(structure.grid.axes_v) - 1  # 2 in your current run

    # ---- Partition along length (x) ----
    # Choose proportions that satisfy typ signature:
    # diele >= 40%, stall >= 20%, remainder = front/service
    diele_len = max(3, int(round(0.45 * bays_x)))   # ~4 of 8
    stall_len = max(2, int(round(0.25 * bays_x)))   # ~2 of 8
    front_len = max(1, bays_x - diele_len - stall_len)

    # Indices
    ix_front0 = 0
    ix_front1 = front_len
    ix_diele0 = ix_front1
    ix_diele1 = ix_diele0 + diele_len
    ix_stall0 = ix_diele1
    ix_stall1 = bays_x

    # ---- Rooms ----
    # Diele spans both aisles (iy 0..bays_y)
    diele_fields = _range_fields(ix_diele0, ix_diele1, 0, bays_y)

    # Stall spans both aisles in rear
    stall_fields = _range_fields(ix_stall0, ix_stall1, 0, bays_y)

    # Stube: pick one side aisle near front: iy=1 is "north half" (depends on your mapping)
    # We'll use iy=1 if exists, else iy=0
    stube_iy = 1 if bays_y >= 2 else 0
    stube_fields = _range_fields(ix_front0, ix_front1, stube_iy, stube_iy + 1)

    rooms: List[Room] = [
        Room(id="R_DIELE", type="diele", field_ids=tuple(diele_fields), story=0),
        Room(id="R_STALL", type="stall", field_ids=tuple(stall_fields), story=0),
        Room(id="R_STUBE", type="stube", field_ids=tuple(stube_fields), story=0),
    ]

    # Zones (optional but useful later)
    zones: List[Zone] = [
        Zone(id="Z_PUBLIC", field_ids=tuple(diele_fields + stube_fields), tags=("PUBLIC",)),
        Zone(id="Z_SERVICE", field_ids=tuple(stall_fields), tags=("SERVICE",)),
    ]

    # ---- Doors (abstract connections; wall_ref is placeholder for now) ----
    doors: List[Door] = [
        Door(
            id="D_STUBE_DIELE",
            between=("R_STUBE", "R_DIELE"),
            wall_ref="INT_WALL_AUTO",
            width=0.9,
            z_range=(0.0, 2.0),
            tags=("INTERIOR_DOOR",),
        ),
        Door(
            id="D_DIELE_STALL",
            between=("R_DIELE", "R_STALL"),
            wall_ref="INT_WALL_AUTO",
            width=1.2,
            z_range=(0.0, 2.2),
            tags=("INTERIOR_DOOR",),
        ),
    ]

    # ---- Opening demands ----
    demands: List[OpeningDemand] = [
        OpeningDemand(room_id="R_STUBE", wall_preference="EXTERIOR", min_count=1, max_count=2, tags=("DAYLIGHT",)),
    ]

    return InteriorPlan(
        zones=tuple(zones),
        rooms=tuple(rooms),
        doors=tuple(doors),
        opening_demands=tuple(demands),
        notes={
            "partition": {
                "front_len": front_len,
                "diele_len": diele_len,
                "stall_len": stall_len,
                "bays_x": bays_x,
                "bays_y": bays_y,
            }
        },
    )
