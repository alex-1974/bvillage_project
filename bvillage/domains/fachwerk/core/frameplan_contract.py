# bvillage/domains/fachwerk/core/frameplan_contract.py
#
# Fachwerk FramePlan Contract Audit
#
# Purpose:
#   Pre-flight quality gate for FramePlan + house data.
#   Ensures geometric, topological and semantic consistency
#   BEFORE Blender build is executed.
#
# This module:
#   - does NOT import Blender
#   - does NOT inspect scene objects
#   - only inspects pure data (fp + house)
#
# Philosophy:
#   audit_*  -> evaluates and reports
#   assert_* -> hard failure wrapper around audit

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

LOG = logging.getLogger("bvillage.domains.fachwerk.core.frameplan_contract")


# ------------------------------------------------------------
# Report model
# ------------------------------------------------------------

@dataclass(slots=True)
class ContractReport:
    ok: bool
    hard: List[str]
    soft: List[str]
    stats: Dict[str, Any]


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def _is_monotonic(values: List[float]) -> bool:
    return all(values[i] < values[i + 1] for i in range(len(values) - 1))


def _abs(x: float) -> float:
    return x if x >= 0.0 else -x


# ------------------------------------------------------------
# Main audit
# ------------------------------------------------------------

def audit_frameplan_contract(
    fp: Dict[str, Any],
    house: Dict[str, Any],
    *,
    strict: bool = False,
) -> ContractReport:
    """
    Pre-flight contract audit for FramePlan.

    Checks:
      - axis monotonicity
      - dimension consistency
      - opening bounds inside walls
      - minimal geometric plausibility
    """

    hard: List[str] = []
    soft: List[str] = []

    axis_x = house.get("axis_x") or []
    axis_y = house.get("axis_y") or []
    z0 = float(house.get("z0", 0.0))
    z_plate = float(house.get("z_plate", 0.0))

    axes_u = fp.get("axes_u") or {}
    axes_z = fp.get("axes_z") or []
    openings = fp.get("openings") or []

    stats = {
        "axis_x": len(axis_x),
        "axis_y": len(axis_y),
        "axes_z": len(axes_z),
        "openings": len(openings),
    }

    LOG.info(
        "FRAMEPLAN AUDIT start | axis_x=%d axis_y=%d z_axes=%d openings=%d",
        len(axis_x), len(axis_y), len(axes_z), len(openings),
    )

    # --------------------------------------------------------
    # 1) Axis sanity
    # --------------------------------------------------------

    if len(axis_x) < 2:
        hard.append("axis_x must contain at least 2 values")

    if len(axis_y) < 2:
        hard.append("axis_y must contain at least 2 values")

    if not _is_monotonic(axis_x):
        hard.append("axis_x must be strictly increasing")

    if not _is_monotonic(axis_y):
        hard.append("axis_y must be strictly increasing")

    if len(axes_z) < 2:
        hard.append("axes_z must contain at least 2 values")

    elif not _is_monotonic(axes_z):
        hard.append("axes_z must be strictly increasing")

    # --------------------------------------------------------
    # 2) Dimension consistency
    # --------------------------------------------------------

    if axis_x:
        L = axis_x[-1] - axis_x[0]
        if L <= 0.0:
            hard.append("computed length L <= 0")

    if axis_y:
        W = axis_y[-1] - axis_y[0]
        if W <= 0.0:
            hard.append("computed width W <= 0")

    if z_plate <= z0:
        hard.append("z_plate must be greater than z0")

    # --------------------------------------------------------
    # 3) Opening bounds
    # --------------------------------------------------------

    for o in openings:
        name = o.get("name", "?")
        wall = o.get("wall")
        u0 = float(o.get("u0", 0.0))
        u1 = float(o.get("u1", 0.0))
        z0o = float(o.get("z0", 0.0))
        z1o = float(o.get("z1", 0.0))

        if u0 >= u1:
            hard.append(f"opening {name}: u0 >= u1")

        if z0o >= z1o:
            hard.append(f"opening {name}: z0 >= z1")

        # Wall must exist in axes_u
        if wall not in axes_u:
            hard.append(f"opening {name}: wall '{wall}' not in axes_u")
            continue

        u_all = axes_u.get(wall, {}).get("all") or []
        if len(u_all) < 2:
            hard.append(f"opening {name}: wall '{wall}' has insufficient u-axes")
            continue

        wall_u_min = min(u_all)
        wall_u_max = max(u_all)

        if u0 < wall_u_min or u1 > wall_u_max:
            hard.append(
                f"opening {name}: u-range [{u0:.3f}..{u1:.3f}] outside wall range [{wall_u_min:.3f}..{wall_u_max:.3f}]"
            )

        if z0o < z0 or z1o > axes_z[-1]:
            hard.append(
                f"opening {name}: z-range [{z0o:.3f}..{z1o:.3f}] outside building vertical range"
            )

        # Soft plausibility checks
        if (u1 - u0) < 0.5:
            soft.append(f"opening {name}: unusually small width")

        if (z1o - z0o) < 0.5:
            soft.append(f"opening {name}: unusually small height")

    # --------------------------------------------------------
    # 4) Report
    # --------------------------------------------------------

    ok = len(hard) == 0

    for msg in hard:
        LOG.error("FRAMEPLAN FAIL | %s", msg)

    for msg in soft:
        LOG.warning("FRAMEPLAN warn | %s", msg)

    LOG.info(
        "FRAMEPLAN AUDIT done | ok=%s hard=%d soft=%d",
        ok, len(hard), len(soft),
    )

    report = ContractReport(
        ok=ok,
        hard=hard,
        soft=soft,
        stats=stats,
    )

    if strict and not ok:
        raise RuntimeError(f"FramePlan contract failed: hard={len(hard)}")

    return report


# ------------------------------------------------------------
# Hard assertion wrapper
# ------------------------------------------------------------

def assert_frameplan_contract(fp: Dict[str, Any], house: Dict[str, Any]) -> None:
    report = audit_frameplan_contract(fp, house, strict=False)
    if not report.ok:
        raise RuntimeError("FramePlan contract assertion failed")
