# bvillage/types/fachwerkhaus/hallenhaus/openings.py

from __future__ import annotations
import random
from typing import List

from bvillage.core.model import Context, StructurePlan, InteriorPlan, OpeningsPlan, Opening


def generate_openings(ctx: Context, structure: StructurePlan, interior: InteriorPlan) -> OpeningsPlan:
    rng = random.Random(ctx.seed ^ 0xA17C)

    openings: List[Opening] = []

    # --- Gate (match your previous Op01 MVP) ---
    openings.append(
        Opening(
            id="O_GATE_01",
            type="gate",
            wall_id="W_S_0",
            u_axis=(-4.3, -1.3),
            z_range=(0.0, 2.2),
            tags=("MAIN_GATE",),
            animation={
                "style": "double_swing",
                "pivots": ["LEFT_POST", "RIGHT_POST"],
                "default_open_deg": 0.0,
            },
        )
    )

    # --- Window for stube demand (MVP: 1 window) ---
    # pick a WINDOW_OK wall: prefer N
    wall_candidates = [w for w in structure.walls if "WINDOW_OK" in w.tags]
    wall_n = next((w for w in wall_candidates if w.side == "N"), None)
    wall = wall_n if wall_n is not None else (wall_candidates[0] if wall_candidates else None)

    if wall is not None:
        win_w = 1.2
        u_min, u_max = wall.u_axis
        # pick center away from ends
        margin = 1.5
        c = rng.uniform(u_min + margin, u_max - margin)
        openings.append(
            Opening(
                id="O_WIN_01",
                type="window",
                wall_id=wall.id,
                u_axis=(c - win_w / 2.0, c + win_w / 2.0),
                z_range=(0.9, 1.6),
                tags=("DAYLIGHT", "STUBE_PREF",),
                animation={
                    "style": "shutter_pair",
                    "default_open_deg": 15.0,
                },
            )
        )

    return OpeningsPlan(openings=tuple(openings))
