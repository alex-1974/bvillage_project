# bvillage/domains/fachwerk/blender/integrity.py

import logging
from typing import Dict, Any

LOG = logging.getLogger("bvillage.domains.fachwerk.blender.integrity")


def _basis_from_fp_or_house(fp: Dict[str, Any], house: Dict[str, Any]):
    dims = fp.get("dims") or {}
    L = dims.get("L")
    W = dims.get("W")

    if L is not None and W is not None:
        x_min = 0.0
        x_max = float(L)
        center_x = 0.5 * x_max
        halfW = 0.5 * float(W)
        return x_min, x_max, center_x, halfW

    axis_x = house.get("axis_x") or []
    axis_y = house.get("axis_y") or []
    if not axis_x or not axis_y:
        raise ValueError("Need fp['dims'] or house axis")

    x_min = float(min(axis_x))
    x_max = float(max(axis_x))
    center_x = 0.5 * (x_min + x_max)
    halfW = 0.5 * (float(max(axis_y)) - float(min(axis_y)))
    return x_min, x_max, center_x, halfW


def check_integrity(
    *,
    fp: Dict[str, Any],
    house: Dict[str, Any],
    collections: Dict[str, Any],
) -> bool:
    """
    Lightweight sanity checks.
    """

    ok = True

    try:
        _basis_from_fp_or_house(fp, house)
    except Exception:
        LOG.error("INTEGRITY FAIL: cannot derive basis")
        return False

    if not fp.get("axes_z"):
        LOG.error("INTEGRITY FAIL: axes_z missing")
        ok = False

    if not fp.get("axes_u"):
        LOG.error("INTEGRITY FAIL: axes_u missing")
        ok = False

    LOG.info("INTEGRITY done | ok=%s", ok)
    return ok
