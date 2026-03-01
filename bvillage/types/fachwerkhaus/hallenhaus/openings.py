# bvillage/types/fachwerkhaus/hallenhaus/openings.py

from __future__ import annotations

import hashlib
from typing import List
from random import Random

from bvillage.core.model import Context, StructurePlan, InteriorPlan, OpeningsPlan, Opening


def _derive_seed(seed: object, component: str) -> int:
    """Derive a deterministic child seed from either an int seed or a Seed object.

    Supports:
      - legacy: ctx.seed is int
      - future: ctx.seed has derive(str) -> int
    """
    # Preferred path: Seed wrapper API
    derive = getattr(seed, "derive", None)
    if callable(derive):
        return int(derive(component))

    # Legacy path: int seed (or int-like)
    base = int(seed)  # will raise if not int-like: good, fail fast
    key = f"{base}:{component}".encode("utf-8")
    # 32-bit seed is enough for random.Random
    return int.from_bytes(hashlib.blake2s(key, digest_size=4).digest(), "big")


def plan_openings(ctx: Context, structure: StructurePlan, interior: InteriorPlan) -> OpeningsPlan:
    rng = Random(ctx.seed.derive("openings.windows"))

    openings: List[Opening] = []

    openings.append(
        Opening(
            id="O_GATE_01",
            type="gate",
            wall_id="W_S_0",
            u_range=(-4.3, -1.3),
            z_range=(0.0, 2.2),
            tags=("MAIN_GATE",),
            animation={
                "style": "double_swing",
                "pivots": ["LEFT_POST", "RIGHT_POST"],
                "default_open_deg": 0.0,
            },
        )
    )

    wall_candidates = sorted(
        (w for w in structure.walls if "WINDOW_OK" in w.tags),
        key=lambda w: w.id,
    )
    wall_n = next((w for w in wall_candidates if w.side == "N"), None)
    wall = wall_n if wall_n is not None else (wall_candidates[0] if wall_candidates else None)

    if wall is not None:
        win_w = 1.2
        u_min, u_max = wall.u_range
        margin = 1.5
        lo = u_min + margin
        hi = u_max - margin
        c = rng.uniform(lo, hi) if hi > lo else (u_min + u_max) / 2.0

        openings.append(
            Opening(
                id="O_WIN_01",
                type="window",
                wall_id=wall.id,
                u_range=(c - win_w / 2.0, c + win_w / 2.0),
                z_range=(0.9, 1.6),
                tags=("DAYLIGHT", "STUBE_PREF"),
                animation={
                    "style": "shutter_pair",
                    "default_open_deg": 15.0,
                },
            )
        )

    return OpeningsPlan(openings=tuple(openings))
