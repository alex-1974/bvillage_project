# bvillage/types/fachwerkhaus/hallenhaus/openings.py
from __future__ import annotations

import hashlib
from random import Random
from typing import Any, List

from bvillage.core.errors import SchemaError
from bvillage.core.model import (
    Context,
    InteriorPlan,
    OpeningsPlan,
    Opening,
    StructurePlan,
)

__all__ = ["plan_openings"]


def _derive_seed(seed: object, component: str) -> int:
    """Derive a deterministic child seed from either an int seed or a Seed object."""
    derive = getattr(seed, "derive", None)
    if callable(derive):
        return int(derive(component))

    base = int(seed)
    key = f"{base}:{component}".encode("utf-8")
    return int.from_bytes(hashlib.blake2s(key, digest_size=4).digest(), "big")


def _select_window_wall(structure: StructurePlan) -> Any | None:
    wall_candidates = sorted(
        (w for w in structure.walls if "WINDOW_OK" in w.tags),
        key=lambda w: w.id,
    )
    wall_n = next((w for w in wall_candidates if w.side == "N"), None)
    if wall_n is not None:
        return wall_n
    return wall_candidates[0] if wall_candidates else None


def _has_daylight_demand(interior: InteriorPlan) -> bool:
    return any(
        d.min_count > 0 and ("DAYLIGHT" in d.tags or d.wall_preference == "EXTERIOR")
        for d in interior.opening_demands
    )


def plan_openings(
    ctx: Context,
    *,
    structure: StructurePlan,
    interior: InteriorPlan,
    frameplan: dict[str, Any],
) -> OpeningsPlan:
    """
    Derive Hallenhaus openings from:
    - explicit FramePlan
    - InteriorPlan opening demands
    - deterministic local RNG

    WHY:
    Gate placement must not diverge between FramePlan and OpeningsPlan.
    """
    rng = Random(_derive_seed(ctx.seed, "openings.windows"))
    openings: List[Opening] = []

    fp_notes = frameplan.get("notes", {})
    gate_meta = fp_notes.get("gate", {})
    gate_wall_id = str(gate_meta.get("wall", "W_E_0"))

    gate_wall = next((w for w in structure.walls if w.id == gate_wall_id), None)
    if gate_wall is None:
        raise SchemaError(f"Gate wall {gate_wall_id!r} not present in StructurePlan.walls")

    gate_clear_w = 3.0
    gate_half = 0.5 * gate_clear_w
    gate_z1 = 2.2

    openings.append(
        Opening(
            id="O_GATE_01",
            type="gate",
            wall_id=gate_wall.id,
            u_range=(-gate_half, +gate_half),
            z_range=(0.0, gate_z1),
            tags=("MAIN_GATE",),
            animation={
                "style": "double_swing",
                "pivots": ["LEFT_POST", "RIGHT_POST"],
                "default_open_deg": 0.0,
            },
        )
    )

    if _has_daylight_demand(interior):
        wall = _select_window_wall(structure)

        if wall is not None:
            win_w = 1.2
            u_min, u_max = wall.u_range

            margin = 1.5
            lo = u_min + margin
            hi = u_max - margin
            center_u = rng.uniform(lo, hi) if hi > lo else (u_min + u_max) / 2.0

            openings.append(
                Opening(
                    id="O_WIN_01",
                    type="window",
                    wall_id=wall.id,
                    u_range=(center_u - win_w / 2.0, center_u + win_w / 2.0),
                    z_range=(0.9, 1.6),
                    tags=("DAYLIGHT", "STUBE_PREF"),
                    animation={
                        "style": "shutter_pair",
                        "default_open_deg": 15.0,
                    },
                )
            )

    return OpeningsPlan(openings=tuple(openings))
