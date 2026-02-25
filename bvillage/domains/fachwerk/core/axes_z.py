# bvillage/domains/fachwerk/core/axes_z.py

"""
bvillage.domains.fachwerk.core.axes_z
====================================

Compute horizontal Z axes for Fachwerk framing.

Units: meters.
"""

from __future__ import annotations

from typing import List, Tuple

from bvillage.core.geom_eps import EPS_EQ, EPS_MERGE, clamp
from bvillage.domains.fachwerk.core.openings_norm import OpeningFinal


def _sorted_unique(vals: List[float], eps: float) -> List[float]:
    vals2 = sorted(float(v) for v in vals)
    out: List[float] = []
    for v in vals2:
        if not out or abs(v - out[-1]) > eps:
            out.append(v)
    return out


def compute_z_axes(
    *,
    z0: float,
    H_e: float,
    horizontal_axes_style: List[float],
    z_merge_tol: float,
    z_band_min: float,
    z_band_target_min: float,
    openings: List[OpeningFinal],
) -> Tuple[List[float], List[List[float]], List[str]]:
    z0 = float(z0)
    H_e = float(H_e)
    if H_e < z0:
        z0, H_e = H_e, z0

    # Prefer caller-provided merge tol, but ensure it's not tighter than global EPS_MERGE
    merge_tol = float(max(z_merge_tol, EPS_MERGE))

    cand: List[float] = []
    cand.extend(float(x) for x in horizontal_axes_style)
    for op in openings:
        cand.append(float(op.z0))
        cand.append(float(op.z1))
    cand.append(z0)
    cand.append(H_e)

    cand = [clamp(v, z0, H_e) for v in cand]
    z_axes = _sorted_unique(cand, merge_tol)

    clusters: List[List[float]] = [[] for _ in z_axes]
    for v in cand:
        nearest_i = min(range(len(z_axes)), key=lambda i: abs(z_axes[i] - v))
        clusters[nearest_i].append(v)

    repair_log: List[str] = []

    def is_supported_by_opening_edge(z: float) -> bool:
        for op in openings:
            if abs(op.z0 - z) <= merge_tol or abs(op.z1 - z) <= merge_tol:
                return True
        return False

    def is_style_axis(z: float) -> bool:
        for s in horizontal_axes_style:
            if abs(float(s) - z) <= merge_tol:
                return True
        return False

    changed = True
    while changed and len(z_axes) >= 2:
        changed = False
        bands = [(z_axes[i], z_axes[i + 1], z_axes[i + 1] - z_axes[i]) for i in range(len(z_axes) - 1)]

        thin_hard = [b for b in bands if b[2] < float(z_band_min) - EPS_EQ]
        if not thin_hard:
            thin_soft = [b for b in bands if b[2] < float(z_band_target_min) - EPS_EQ]
            if not thin_soft:
                break

            z_lo, z_hi, dz = min(thin_soft, key=lambda x: x[2])
            drop_candidates: List[float] = []
            if z_lo != z0 and z_lo != H_e:
                drop_candidates.append(z_lo)
            if z_hi != z0 and z_hi != H_e:
                drop_candidates.append(z_hi)
            if not drop_candidates:
                break

            def score(z: float) -> tuple[int, int]:
                supported = 1 if is_supported_by_opening_edge(z) else 0
                style = 1 if is_style_axis(z) else 0
                return (supported, style)

            drop = sorted(drop_candidates, key=score)[0]
            z_axes.remove(drop)
            repair_log.append(f"drop style z={drop:.3f} (FAST_DROP thin band {dz:.3f})")
            changed = True
            continue

        z_lo, z_hi, dz = min(thin_hard, key=lambda x: x[2])
        candidates: List[float] = []
        if z_lo != z0 and z_lo != H_e:
            candidates.append(z_lo)
        if z_hi != z0 and z_hi != H_e:
            candidates.append(z_hi)

        if not candidates:
            repair_log.append(f"unrepairable thin band dz={dz:.3f} at [{z_lo:.3f},{z_hi:.3f}]")
            break

        def hard_score(z: float) -> tuple[int, int]:
            supported = 1 if is_supported_by_opening_edge(z) else 0
            style = 0 if is_style_axis(z) else 1
            return (supported, style)

        drop = sorted(candidates, key=hard_score)[0]
        z_axes.remove(drop)
        repair_log.append(f"drop z={drop:.3f} (HARD thin band {dz:.3f})")
        changed = True

    z_axes = _sorted_unique(z_axes, merge_tol)
    clusters = [[] for _ in z_axes]
    for v in cand:
        nearest_i = min(range(len(z_axes)), key=lambda i: abs(z_axes[i] - v))
        clusters[nearest_i].append(v)

    return z_axes, clusters, repair_log
