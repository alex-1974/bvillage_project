# bvillage/domains/fachwerk/blender/braces.py

import logging
from typing import Dict, Any

import bpy
from mathutils import Vector

from .timber import make_beam_rect

LOG = logging.getLogger("bvillage.domains.fachwerk.blender.braces")


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

    # fallback legacy
    axis_x = house.get("axis_x") or []
    axis_y = house.get("axis_y") or []
    if not axis_x or not axis_y:
        raise ValueError("Need fp['dims'] (L,W) or house axis_x/axis_y")

    x_min = float(min(axis_x))
    x_max = float(max(axis_x))
    center_x = 0.5 * (x_min + x_max)
    halfW = 0.5 * (float(max(axis_y)) - float(min(axis_y)))
    return x_min, x_max, center_x, halfW


def build_braces_corner_band(
    *,
    fp: Dict[str, Any],
    house: Dict[str, Any],
    collection: bpy.types.Collection,
):
    """
    Corner-only knee braces in the upper band (members-first ready).
    """

    x_min, x_max, center_x, halfW = _basis_from_fp_or_house(fp, house)

    z_axes = fp.get("axes_z") or []
    if len(z_axes) < 2:
        return

    z0 = float(z_axes[-2])
    z1 = float(z_axes[-1])

    profile = (0.12, 0.12)
    built = 0

    for wall in ("N", "S", "E", "W"):

        if wall in ("N", "S"):
            y = -halfW if wall == "N" else halfW
            p0 = Vector((x_min, y, z0))
            p1 = Vector((x_min + 0.6, y, z1))
            make_beam_rect(f"Brace_{wall}_L", p0, p1,
                           width=profile[0], depth=profile[1],
                           collection=collection)
            built += 1

            p0 = Vector((x_max, y, z0))
            p1 = Vector((x_max - 0.6, y, z1))
            make_beam_rect(f"Brace_{wall}_R", p0, p1,
                           width=profile[0], depth=profile[1],
                           collection=collection)
            built += 1

        else:
            x = x_max if wall == "E" else x_min
            p0 = Vector((x, -halfW, z0))
            p1 = Vector((x, -halfW + 0.6, z1))
            make_beam_rect(f"Brace_{wall}_L", p0, p1,
                           width=profile[0], depth=profile[1],
                           collection=collection)
            built += 1

            p0 = Vector((x, halfW, z0))
            p1 = Vector((x, halfW - 0.6, z1))
            make_beam_rect(f"Brace_{wall}_R", p0, p1,
                           width=profile[0], depth=profile[1],
                           collection=collection)
            built += 1

    LOG.info("Phase4C braces: done built=%d", built)
