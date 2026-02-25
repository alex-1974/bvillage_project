# bvillage/domains/fachwerk/core/axes_u.py

"""
bvillage.domains.fachwerk.core.axes_u
====================================

Compute *vertical stud axes along each wall* (u-axes in wall-local coordinates).
(See earlier docstring for full details.)

Units: meters.
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

from bvillage.core.geom_eps import EPS_EQ, EPS_INSIDE
from bvillage.domains.fachwerk.core.openings_norm import OpeningFinal


def interval_intersects(a0: float, a1: float, b0: float, b1: float, eps: float = EPS_EQ) -> bool:
    a0, a1 = (a0, a1) if a0 <= a1 else (a1, a0)
    b0, b1 = (b0, b1) if b0 <= b1 else (b1, b0)
    return not (a1 <= b0 + eps or b1 <= a0 + eps)


def sorted_unique(xs: List[float], eps: float = EPS_EQ) -> List[float]:
    ys = sorted(float(x) for x in xs)
    out: List[float] = []
    for v in ys:
        if not out or abs(v - out[-1]) > eps:
            out.append(v)
    return out


def wall_run_len(L: float, W: float, wall: str) -> float:
    return float(L if wall in ("N", "S") else W)


def wall_u_range(L: float, W: float, wall: str) -> Tuple[float, float]:
    run = wall_run_len(L, W, wall)
    return (-run / 2.0, +run / 2.0)


def axis_inside_any_opening(wall: str, u: float, openings: List[OpeningFinal]) -> bool:
    for op in openings:
        if op.wall != wall:
            continue
        if (u > op.u0 + EPS_INSIDE) and (u < op.u1 - EPS_INSIDE):
            return True
    return False


def compute_vertical_axes(
    *,
    L: float,
    W: float,
    b_max: float,
    openings: List[OpeningFinal],
) -> Dict[str, Dict[str, List[float]]]:
    out: Dict[str, Dict[str, List[float]]] = {}

    for wall in ("N", "S", "E", "W"):
        umin, umax = wall_u_range(L, W, wall)
        primary = [umin, umax]

        opening_axes: List[float] = []
        for op in openings:
            if op.wall != wall:
                continue
            opening_axes += [op.u0, op.u1]
        opening_axes = sorted_unique(opening_axes)

        fixed = sorted_unique(primary + opening_axes)

        secondary: List[float] = []
        for i in range(len(fixed) - 1):
            a, b = fixed[i], fixed[i + 1]
            span = b - a
            if span <= b_max + EPS_EQ:
                continue

            n_seg = int(math.ceil(span / b_max))
            step = span / n_seg

            for k in range(1, n_seg):
                u = a + step * k
                if axis_inside_any_opening(wall, u, openings):
                    continue
                secondary.append(u)

        secondary = sorted_unique(secondary)

        out[wall] = {
            "primary": primary,
            "opening": opening_axes,
            "secondary": secondary,
            "all": sorted_unique(fixed + secondary),
        }

    return out
