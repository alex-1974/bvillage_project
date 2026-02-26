# bvillage/domains/fachwerk/blender/braces.py

import logging
from typing import Any, Dict, List

import bpy
from mathutils import Vector

from .timber import make_beam_rect

LOG = logging.getLogger("bvillage.domains.fachwerk.blender.braces")


# ---------------------------------------------------------------------
# Canonical FramePlan-first helpers
# ---------------------------------------------------------------------

def _get_basis(fp: Dict[str, Any]) -> Dict[str, float]:
    """
    Prefer canonical fp["basis"].
    Fallback: derive from fp["dims"] (L,W).
    """
    basis = fp.get("basis")
    if isinstance(basis, dict) and all(k in basis for k in ("x_min", "x_max", "center_x", "halfW")):
        return {
            "x_min": float(basis["x_min"]),
            "x_max": float(basis["x_max"]),
            "center_x": float(basis["center_x"]),
            "halfW": float(basis["halfW"]),
        }

    dims = fp.get("dims") or {}
    L = dims.get("L")
    W = dims.get("W")
    if L is None or W is None:
        raise ValueError("Missing basis and dims.L/dims.W in frameplan dict")

    Lf = float(L)
    Wf = float(W)
    return {"x_min": 0.0, "x_max": Lf, "center_x": 0.5 * Lf, "halfW": 0.5 * Wf}


def _flatten_numeric(x: Any) -> List[float]:
    """Collect numeric values from nested lists/dicts; return sorted unique floats."""
    vals: List[float] = []

    def _collect(v: Any) -> None:
        if v is None:
            return
        if isinstance(v, (int, float)):
            vals.append(float(v))
            return
        if isinstance(v, str):
            try:
                vals.append(float(v))
            except Exception:
                return
            return
        if isinstance(v, (list, tuple)):
            for it in v:
                _collect(it)
            return
        if isinstance(v, dict):
            for it in v.values():
                _collect(it)
            return

    _collect(x)
    return sorted(set(vals))


def _get_axes_z(fp: Dict[str, Any]) -> List[float]:
    z = fp.get("axes_z_flat")
    if isinstance(z, list) and z:
        return [float(v) for v in z]
    return _flatten_numeric(fp.get("axes_z"))


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def build_braces_corner_band(
    *,
    fp: Dict[str, Any],
    house: Dict[str, Any],  # kept for signature compatibility; not required if fp canonical
    collection: bpy.types.Collection,
):
    """
    Corner-only knee braces in the upper band (FramePlan-first).

    Uses:
      - fp["basis"] for extents (fallback: dims)
      - fp["axes_z_flat"] for z band (fallback: axes_z)
    """
    basis = _get_basis(fp)
    x_min = basis["x_min"]
    x_max = basis["x_max"]
    halfW = basis["halfW"]

    axes_z = _get_axes_z(fp)
    if len(axes_z) < 2:
        LOG.warning("Phase4C braces: axes_z too short -> nothing built")
        return

    # Use top band (second last -> last)
    z0 = float(axes_z[-2])
    z1 = float(axes_z[-1])

    profile = (0.12, 0.12)
    built = 0
    brace_len = 0.6  # meters

    # N/S walls: braces along X direction at corners
    for wall in ("N", "S"):
        y = -halfW if wall == "N" else halfW

        # left corner
        p0 = Vector((x_min, y, z0))
        p1 = Vector((x_min + brace_len, y, z1))
        make_beam_rect(
            f"Brace_{wall}_L",
            p0,
            p1,
            width=profile[0],
            depth=profile[1],
            collection=collection,
        )
        built += 1

        # right corner
        p0 = Vector((x_max, y, z0))
        p1 = Vector((x_max - brace_len, y, z1))
        make_beam_rect(
            f"Brace_{wall}_R",
            p0,
            p1,
            width=profile[0],
            depth=profile[1],
            collection=collection,
        )
        built += 1

    # E/W walls: braces along Y direction at corners
    for wall in ("E", "W"):
        x = x_max if wall == "E" else x_min

        # near -halfW
        p0 = Vector((x, -halfW, z0))
        p1 = Vector((x, -halfW + brace_len, z1))
        make_beam_rect(
            f"Brace_{wall}_L",
            p0,
            p1,
            width=profile[0],
            depth=profile[1],
            collection=collection,
        )
        built += 1

        # near +halfW
        p0 = Vector((x, halfW, z0))
        p1 = Vector((x, halfW - brace_len, z1))
        make_beam_rect(
            f"Brace_{wall}_R",
            p0,
            p1,
            width=profile[0],
            depth=profile[1],
            collection=collection,
        )
        built += 1

    LOG.info("Phase4C braces: done built=%d", built)
