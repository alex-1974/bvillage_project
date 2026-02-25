# bvillage/domains/fachwerk/core/wall_tags.py

"""
bvillage.domains.fachwerk.core.wall_tags
=======================================

Purpose
-------
Compute per-wall metadata ("tags") derived from normalized openings and provide
simple heuristics such as suggesting a "front wall".

This is Fachwerk-domain logic:
- it operates on `OpeningFinal` (normalized opening representation)
- it returns small JSON-like dicts for easy consumption (reports, UI, notes)

Contracts
---------
compute_wall_tags(openings) -> dict[str, dict[str, Any]]
- openings: list[OpeningFinal]
- returns: mapping for each wall in {"N","S","E","W"} with counters/flags

suggest_front_wall(wall_tags) -> "N"|"S"|"E"|"W"
- heuristic for orienting reports / choosing entry side

Units
-----
Not applicable (categorical metadata only).

Performance
-----------
O(n) where n is number of openings. Deterministic order.

Future-proofing
---------------
- Keep returned keys stable; treat them as part of the domain API.
- Extend by adding new keys (backwards compatible), avoid renaming.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, Literal, Mapping, TypedDict

from bvillage.domains.fachwerk.core.openings_norm import OpeningFinal

WallSide = Literal["N", "S", "E", "W"]
_WALLS: tuple[WallSide, ...] = ("N", "S", "E", "W")


class WallTagRecord(TypedDict):
    has_door: bool
    has_gate: bool
    has_window: bool
    n_openings: int
    n_doors: int
    n_gates: int
    n_windows: int
    opening_names: list[str]
    has_primary_entry: bool
    op_signature: str


def compute_wall_tags(openings: Iterable[OpeningFinal]) -> Dict[WallSide, WallTagRecord]:
    """
    Compute wall tags from normalized openings.

    Parameters
    ----------
    openings:
        Iterable of `OpeningFinal`.

    Returns
    -------
    dict[WallSide, WallTagRecord]
        Always contains entries for all four walls ("N","S","E","W").

    Notes
    -----
    Opening types recognized:
      - "door"
      - "gate"
      - "window"
    All others are counted as openings but do not set the specific flags.
    """
    tags: Dict[WallSide, WallTagRecord] = {
        w: WallTagRecord(
            has_door=False,
            has_gate=False,
            has_window=False,
            n_openings=0,
            n_doors=0,
            n_gates=0,
            n_windows=0,
            opening_names=[],
            has_primary_entry=False,  # filled in later
            op_signature="---",       # filled in later
        )
        for w in _WALLS
    }

    for op in openings:
        wall = op.wall
        if wall not in tags:
            # Defensive: ignore unknown walls rather than crashing
            continue

        t = tags[wall]
        t["n_openings"] += 1
        t["opening_names"].append(op.name)

        if op.typ == "door":
            t["has_door"] = True
            t["n_doors"] += 1
        elif op.typ == "gate":
            t["has_gate"] = True
            t["n_gates"] += 1
        elif op.typ == "window":
            t["has_window"] = True
            t["n_windows"] += 1

    # Derive aggregate fields in a deterministic order
    for w in _WALLS:
        t = tags[w]
        t["has_primary_entry"] = bool(t["has_door"] or t["has_gate"])
        t["op_signature"] = (
            ("G" if t["has_gate"] else "-")
            + ("D" if t["has_door"] else "-")
            + ("W" if t["has_window"] else "-")
        )

    return tags


def suggest_front_wall(wall_tags: Mapping[str, Mapping[str, Any]]) -> WallSide:
    """
    Suggest a front wall based on wall tags.

    Heuristic (stable)
    ------------------
    1) Prefer a wall that has a gate (first in N,S,E,W order).
    2) Else prefer a wall that has a door (first in N,S,E,W order).
    3) Else choose wall with the highest number of openings.
       Ties are resolved deterministically by N,S,E,W order.

    Parameters
    ----------
    wall_tags:
        Mapping (typically output from compute_wall_tags).

    Returns
    -------
    WallSide
        One of "N","S","E","W".
    """
    for w in _WALLS:
        if bool(wall_tags.get(w, {}).get("has_gate", False)):
            return w

    for w in _WALLS:
        if bool(wall_tags.get(w, {}).get("has_door", False)):
            return w

    # deterministic argmax
    best = "N"
    best_n = int(wall_tags.get("N", {}).get("n_openings", 0))
    for w in ("S", "E", "W"):
        n = int(wall_tags.get(w, {}).get("n_openings", 0))
        if n > best_n:
            best, best_n = w, n
    return best  # type: ignore[return-value]
