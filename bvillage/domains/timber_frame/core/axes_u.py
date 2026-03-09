# bvillage/domains/fachwerk/core/axes_u.py

"""
bvillage.domains.timber_frame.core.axes_u
====================================

Compute *vertical stud axes along each wall* (u-axes in wall-local coordinates).

Each wall produces three axis sets:
- primary:   wall endpoints and opening edges (structurally mandatory)
- secondary: subdivision axes filling spans wider than binder_max
- all:       union of primary, opening, and secondary (used by frame builders)

Secondary axes are rejected if they fall inside an opening interior.
Rejection uses a precomputed interval union per wall — not a per-axis scan.

Units: meters.
"""

from __future__ import annotations

import bisect
import math

from bvillage.core.geom_eps import EPS_EQ, EPS_INSIDE, sorted_unique
from bvillage.domains.timber_frame.core.openings_norm import OpeningFinal

__all__ = [
    "interval_intersects",
    "wall_run_len",
    "wall_u_range",
    "axis_inside_any_opening",
    "compute_vertical_axes",
]

_WALLS: tuple[str, ...] = ("N", "S", "E", "W")


# ---------------------------------------------------------------------------
# Geometric primitives
# ---------------------------------------------------------------------------

def interval_intersects(
    a0: float, a1: float,
    b0: float, b1: float,
    eps: float = EPS_EQ,
) -> bool:
    """Returns True if intervals [a0, a1] and [b0, b1] overlap by more than eps."""
    if a0 > a1:
        a0, a1 = a1, a0
    if b0 > b1:
        b0, b1 = b1, b0
    return not (a1 <= b0 + eps or b1 <= a0 + eps)


def wall_run_len(L: float, W: float, wall: str) -> float:
    """Returns the run length of a wall in meters (L for N/S, W for E/W)."""
    return float(L if wall in ("N", "S") else W)


def wall_u_range(L: float, W: float, wall: str) -> tuple[float, float]:
    """Returns the symmetric u-coordinate range (umin, umax) for a wall."""
    run = wall_run_len(L, W, wall)
    return (-run / 2.0, +run / 2.0)


# ---------------------------------------------------------------------------
# Opening interior check
# ---------------------------------------------------------------------------

def _build_opening_union(wall: str, openings: list[OpeningFinal]) -> tuple[float, ...]:
    """Builds a flat sorted sequence of interval endpoints for all openings on wall.

    Returns a tuple (u0_a, u1_a, u0_b, u1_b, ...) — pairs of (start, end).
    The intervals are non-overlapping and sorted by start, enabling O(log n) lookup.

    # WHY: precomputing per-wall avoids rescanning all openings for every candidate
    # stud. axis_inside_any_opening is called inside the inner subdivision loop —
    # O(n_studs × n_openings) becomes O(n_studs × log n_openings).
    """
    intervals: list[tuple[float, float]] = [
        (op.u0, op.u1) for op in openings if op.wall == wall
    ]
    if not intervals:
        return ()

    intervals.sort()

    # Merge overlapping intervals so bisect lookup is unambiguous
    merged: list[tuple[float, float]] = [intervals[0]]
    for start, end in intervals[1:]:
        prev_start, prev_end = merged[-1]
        if start <= prev_end + EPS_EQ:
            merged[-1] = (prev_start, max(prev_end, end))
        else:
            merged.append((start, end))

    return tuple(v for lo, hi in merged for v in (lo, hi))


def axis_inside_any_opening(
    wall: str,
    u: float,
    openings: list[OpeningFinal],
) -> bool:
    """Returns True if u falls strictly inside any opening on wall.

    Note: this function rescans openings on every call.
    Inside compute_vertical_axes the union is precomputed once per wall —
    _axis_inside_union handles the hot path.
    """
    for op in openings:
        if op.wall == wall and (u > op.u0 + EPS_INSIDE) and (u < op.u1 - EPS_INSIDE):
            return True
    return False


def _axis_inside_union(u: float, union: tuple[float, ...]) -> bool:
    """Returns True if u falls strictly inside any interval in the precomputed union.

    union is a flat sorted tuple: (u0_a, u1_a, u0_b, u1_b, ...).
    bisect_right locates the insertion point; even indices are interval starts,
    odd indices are interval ends.

    # HOT PATH — no allocation, O(log n)
    """
    if not union:
        return False
    idx = bisect.bisect_right(union, u) - 1
    if idx < 0 or idx % 2 == 1:
        return False
    # idx is even: u sits inside interval [union[idx], union[idx+1]]
    return u > union[idx] + EPS_INSIDE and u < union[idx + 1] - EPS_INSIDE


# ---------------------------------------------------------------------------
# Main computation
# ---------------------------------------------------------------------------

def compute_vertical_axes(
    *,
    L: float,
    W: float,
    binder_max: float,
    openings: list[OpeningFinal],
) -> dict[str, dict[str, list[float]]]:
    """Computes vertical stud axes for all four walls.

    Args:
        L: Building length in meters (N/S wall run).
        W: Building width in meters (E/W wall run).
        binder_max: Maximum allowed bay width in meters.
        openings: Normalized openings from OpeningsPlan.

    Returns:
        Mapping wall → {primary, opening, secondary, all} axis sets.
        Each set is a sorted list of u-coordinates in wall-local space.

        # DEFERRED: sets use list[float] to preserve the existing contract with
        # frameplan.py and tests. Migrate to tuple[float, ...] when those callers
        # are updated alongside sorted_unique's return type change.

    Preconditions:
        - L > 0, W > 0, binder_max > 0
        - openings contains only OpeningFinal instances with valid wall labels

    Postconditions:
        - All axis sets are sorted and deduplicated
        - No secondary axis falls strictly inside any opening
        - Every span in "all" is ≤ binder_max + EPS_EQ
    """
    out: dict[str, dict[str, list[float]]] = {}

    for wall in _WALLS:
        umin, umax = wall_u_range(L, W, wall)

        # Opening edges are mandatory primary axes
        opening_axes = list(sorted_unique(
            [op.u0 for op in openings if op.wall == wall]
            + [op.u1 for op in openings if op.wall == wall]
        ))

        fixed = list(sorted_unique([umin, umax, *opening_axes]))

        # Precompute opening union once — used for all secondary candidates on this wall
        opening_union = _build_opening_union(wall, openings)

        secondary: list[float] = []
        for a, b in zip(fixed, fixed[1:]):
            span = b - a
            if span <= binder_max + EPS_EQ:
                continue

            n_seg = math.ceil(span / binder_max)
            step = span / n_seg

            secondary.extend(
                a + step * k
                for k in range(1, n_seg)
                if not _axis_inside_union(a + step * k, opening_union)
            )

        secondary_axes = list(sorted_unique(secondary))

        out[wall] = {
            "primary":   [umin, umax],
            "opening":   opening_axes,
            "secondary": secondary_axes,
            "all":       list(sorted_unique([*fixed, *secondary_axes])),
        }

    return out
