# bvillage/domains/fachwerk/core/axes_z.py

"""
bvillage.domains.fachwerk.core.axes_z
====================================

Compute horizontal Z axes for Fachwerk framing.

Starting candidates are the floor level (z0), eaves height (H_e), caller-provided
style levels, and all opening z-edges. Candidates are clamped to [z0, H_e] and
deduplicated. A repair loop then removes axes that produce bands below the hard or
soft minimum, preferring to drop axes with the least structural support.

Units: meters.
"""

from __future__ import annotations

import bisect

from bvillage.core.geom_eps import EPS_EQ, EPS_MERGE, clamp, sorted_unique
from bvillage.domains.fachwerk.core.openings_norm import OpeningFinal

__all__ = ["compute_z_axes"]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _nearest_index(z_axes: list[float], v: float) -> int:
    """Returns the index of the z_axis value nearest to v.

    Uses bisect for O(log n) lookup on a sorted list.

    # WHY: the original used min(range(len(...)), key=...) — O(n) per call,
    # called once per candidate in two cluster-assignment passes. bisect reduces
    # this to O(log n) with no change in behavior.
    """
    if len(z_axes) == 1:
        return 0
    idx = bisect.bisect_left(z_axes, v)
    if idx == 0:
        return 0
    if idx == len(z_axes):
        return len(z_axes) - 1
    # Compare the two neighbours around the insertion point
    return idx if abs(z_axes[idx] - v) <= abs(z_axes[idx - 1] - v) else idx - 1


def _assign_clusters(z_axes: list[float], cand: list[float]) -> list[list[float]]:
    """Assigns each candidate value to the nearest z_axis bucket."""
    clusters: list[list[float]] = [[] for _ in z_axes]
    for v in cand:
        clusters[_nearest_index(z_axes, v)].append(v)
    return clusters


# ---------------------------------------------------------------------------
# Main computation
# ---------------------------------------------------------------------------

def compute_z_axes(
    *,
    z0: float,
    H_e: float,
    style_z_levels: list[float],
    z_merge_tol: float,
    z_band_min: float,
    z_band_target_min: float,
    openings: list[OpeningFinal],
) -> tuple[list[float], list[list[float]], list[str]]:
    """Computes the horizontal Z axes for a Fachwerk wall frame.

    Args:
        z0:                Floor level in meters.
        H_e:               Eaves height in meters.
        style_z_levels:    Caller-requested intermediate Z levels (e.g. rail heights).
        z_merge_tol:       Merge tolerance for deduplication (floored at EPS_MERGE).
        z_band_min:        Hard minimum band height. Violations trigger axis removal,
                           preferring to drop style axes over opening-edge axes.
        z_band_target_min: Soft minimum band height. Violations trigger preferential
                           removal, keeping style and opening-edge axes where possible.
        openings:          Normalized openings whose z-edges become mandatory axes.

    Returns:
        (z_axes, clusters, repair_log)
        - z_axes:     Sorted, deduplicated list of Z values in [z0, H_e].
        - clusters:   For each z_axis, the candidate values assigned to it.
        - repair_log: Human-readable record of every axis dropped during repair.

        # DEFERRED: return type uses list[float] to preserve the existing contract
        # with frameplan.py. Migrate to tuple[float, ...] when that caller is updated.

    Preconditions:
        - z_band_min <= z_band_target_min
        - z0 and H_e are finite floats; order is normalized internally

    Postconditions:
        - z_axes[0] == z0 and z_axes[-1] == H_e
        - All bands are >= z_band_min (unless an unrepairable band is logged)
        - Every drop is recorded in repair_log
    """
    z0  = float(z0)
    H_e = float(H_e)
    if H_e < z0:
        z0, H_e = H_e, z0

    # Prefer caller-provided merge tol, but ensure it's not tighter than global EPS_MERGE
    merge_tol = float(max(z_merge_tol, EPS_MERGE))

    # Collect all candidate Z values and clamp to [z0, H_e]
    cand: list[float] = (
        [float(x) for x in style_z_levels]
        + [float(op.z0) for op in openings]
        + [float(op.z1) for op in openings]
        + [z0, H_e]
    )
    cand = [clamp(v, z0, H_e) for v in cand]

    z_axes   = list(sorted_unique(cand, merge_tol))
    clusters = _assign_clusters(z_axes, cand)

    # Support predicates — defined once outside the loop.
    # Tolerance-based comparison is required; set equality would silently miss
    # near-equal floats at merge_tol boundaries.
    def is_supported_by_opening_edge(z: float) -> bool:
        for op in openings:
            if abs(op.z0 - z) <= merge_tol or abs(op.z1 - z) <= merge_tol:
                return True
        return False

    def is_style_axis(z: float) -> bool:
        for s in style_z_levels:
            if abs(float(s) - z) <= merge_tol:
                return True
        return False

    def drop_score(z: float, *, prefer_keeping_style: bool) -> tuple[int, int]:
        """Returns a (supported, style_cost) sort key. Lower = preferred drop target.

        prefer_keeping_style=True  (soft repair): keep style axes, drop others first.
        prefer_keeping_style=False (hard repair): drop style axes before opening edges.

        # WHY: the original defined score() and hard_score() as separate closures
        # inside the while-loop body, recreating them on every iteration. A single
        # parametric function outside the loop eliminates both the duplication and
        # the per-iteration closure allocation.
        """
        supported = 1 if is_supported_by_opening_edge(z) else 0
        style     = (1 if is_style_axis(z) else 0) if prefer_keeping_style else \
                    (0 if is_style_axis(z) else 1)
        return (supported, style)

    repair_log: list[str] = []

    # -------------------------------------------------------------------------
    # Repair loop — iteratively remove axes that produce bands below the minimums.
    # Hard violations (< z_band_min) are addressed first; style axes are preferred
    # drop targets. Soft violations (< z_band_target_min) drop the least-supported
    # axis while keeping style and opening-edge axes where possible.
    # -------------------------------------------------------------------------
    changed = True
    while changed and len(z_axes) >= 2:
        changed = False
        bands = [(a, b, b - a) for a, b in zip(z_axes, z_axes[1:])]

        thin_hard = [band for band in bands if band[2] < float(z_band_min) - EPS_EQ]
        if not thin_hard:
            thin_soft = [band for band in bands if band[2] < float(z_band_target_min) - EPS_EQ]
            if not thin_soft:
                break

            z_lo, z_hi, dz = min(thin_soft, key=lambda x: x[2])
            dc = [z for z in (z_lo, z_hi) if z != z0 and z != H_e]
            if not dc:
                break

            drop = min(dc, key=lambda z: drop_score(z, prefer_keeping_style=True))
            z_axes.remove(drop)
            repair_log.append(f"drop style z={drop:.3f} (FAST_DROP thin band {dz:.3f})")
            changed = True
            continue

        z_lo, z_hi, dz = min(thin_hard, key=lambda x: x[2])
        ca = [z for z in (z_lo, z_hi) if z != z0 and z != H_e]

        if not ca:
            repair_log.append(f"unrepairable thin band dz={dz:.3f} at [{z_lo:.3f},{z_hi:.3f}]")
            break

        drop = min(ca, key=lambda z: drop_score(z, prefer_keeping_style=False))
        z_axes.remove(drop)
        repair_log.append(f"drop z={drop:.3f} (HARD thin band {dz:.3f})")
        changed = True

    z_axes   = list(sorted_unique(z_axes, merge_tol))
    clusters = _assign_clusters(z_axes, cand)

    return z_axes, clusters, repair_log
