# bvillage/domains/fachwerk/blender/braces.py

#
# Phase 4C: Kopfband (knee brace) – corner-only
# - Deterministisch
# - Opening-safe (skip if cell lies inside opening)
# - Logging + Debug hooks
#
# Coord system: matches infills.py
#   - world x in [x_min..x_max] (typically 0..L)
#   - world y in [-halfW..+halfW]
#   - FramePlan u for N/S is centered around 0 -> x = center_x + u
#   - For E/W, u maps to world y -> y = u, x fixed at x_min/x_max

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import bpy
from mathutils import Vector

from bvillage.core.geom_eps import EPS_INSIDE
from .timber import make_beam_rect

LOG = logging.getLogger("bvillage.domains.fachwerk.blender.braces")


@dataclass(frozen=True, slots=True)
class BraceConfig:
    # timber profile (meters)
    profile: Tuple[float, float] = (0.12, 0.12)

    # place brace inside the cell, away from edges (meters)
    inset_u: float = 0.03
    inset_z: float = 0.03

    # if a cell is too small, skip
    min_cell_w: float = 0.40
    min_cell_h: float = 0.40

    # debug empties
    debug: bool = False
    debug_empty_size: float = 0.18


# ----------------------------
# Openings helpers (same logic as infills)
# ----------------------------

def _collect_openings_for_wall(fp: Dict[str, Any], wall: str) -> List[Dict[str, Any]]:
    wall = wall.upper()
    out: List[Dict[str, Any]] = []
    for o in fp.get("openings", []) or []:
        if str(o.get("wall", "")).upper() == wall:
            out.append(o)
    return out


def _cell_is_inside_any_opening(
    *,
    u0: float,
    u1: float,
    z0: float,
    z1: float,
    openings_wall: List[Dict[str, Any]],
) -> bool:
    lo_u = min(u0, u1) + EPS_INSIDE
    hi_u = max(u0, u1) - EPS_INSIDE
    lo_z = min(z0, z1) + EPS_INSIDE
    hi_z = max(z0, z1) - EPS_INSIDE

    if hi_u <= lo_u or hi_z <= lo_z:
        return False

    for o in openings_wall:
        ou0 = float(o["u0"])
        ou1 = float(o["u1"])
        oz0 = float(o["z0"])
        oz1 = float(o["z1"])
        o_lo_u = min(ou0, ou1) + EPS_INSIDE
        o_hi_u = max(ou0, ou1) - EPS_INSIDE
        o_lo_z = min(oz0, oz1) + EPS_INSIDE
        o_hi_z = max(oz0, oz1) - EPS_INSIDE

        if lo_u >= o_lo_u and hi_u <= o_hi_u and lo_z >= o_lo_z and hi_z <= o_hi_z:
            return True

    return False


# ----------------------------
# Coord mapping (same as infills)
# ----------------------------

def _u_to_xy(
    wall: str,
    u: float,
    *,
    x_min: float,
    x_max: float,
    center_x: float,
    halfW: float,
) -> Tuple[float, float]:
    wall = wall.upper()
    if wall == "N":
        return center_x + float(u), -halfW
    if wall == "S":
        return center_x + float(u), +halfW
    if wall == "E":
        return x_max, float(u)
    if wall == "W":
        return x_min, float(u)
    raise ValueError(f"Unknown wall '{wall}'")


def _wall_inward_normal(wall: str) -> Vector:
    wall = wall.upper()
    if wall == "N":
        return Vector((0.0, +1.0, 0.0))
    if wall == "S":
        return Vector((0.0, -1.0, 0.0))
    if wall == "E":
        return Vector((-1.0, 0.0, 0.0))
    if wall == "W":
        return Vector((+1.0, 0.0, 0.0))
    raise ValueError(f"Unknown wall '{wall}'")


def _link_object(obj: bpy.types.Object, collection: Optional[bpy.types.Collection]) -> None:
    if collection is None:
        bpy.context.collection.objects.link(obj)
    else:
        collection.objects.link(obj)


def _debug_empty(
    *,
    name: str,
    location: Vector,
    collection: Optional[bpy.types.Collection],
    payload: Dict[str, Any],
    size: float,
) -> None:
    try:
        empty = bpy.data.objects.new(name, None)
        empty.empty_display_type = "PLAIN_AXES"
        empty.empty_display_size = float(size)
        empty.location = Vector(location)
        _link_object(empty, collection)
        for k, v in payload.items():
            empty[f"bv_{k}"] = v
    except Exception:
        LOG.exception("debug empty failed: %s", name)


# ----------------------------
# Public API
# ----------------------------

def build_knee_braces_corner_only(
    *,
    fp: Dict[str, Any],
    house: Dict[str, Any],
    collection: Optional[bpy.types.Collection],
    config: Optional[BraceConfig] = None,
    debug_collection: Optional[bpy.types.Collection] = None,
) -> Dict[str, Any]:
    """
    Build knee braces for the four exterior walls, corner-only (leftmost + rightmost cell).
    Uses top wall band just under z_plate (derived from fp.axes_z + house.z_plate).

    Returns stats dict.
    """
    cfg = config or BraceConfig()

    axis_x = house.get("axis_x") or []
    axis_y = house.get("axis_y") or []
    if not axis_x or not axis_y:
        raise ValueError("build_knee_braces_corner_only: house must provide axis_x and axis_y")

    x_min = float(min(axis_x))
    x_max = float(max(axis_x))
    center_x = 0.5 * (x_min + x_max)

    y_min = float(min(axis_y))
    y_max = float(max(axis_y))
    halfW = 0.5 * (y_max - y_min)

    z_axes = list(fp.get("axes_z") or [])
    if len(z_axes) < 2:
        raise ValueError("build_knee_braces_corner_only: fp['axes_z'] must contain at least 2 values")

    # choose top band under z_plate
    z_plate = float(house.get("z_plate", z_axes[-2]))
    # find highest z in axes_z strictly below z_plate
    z_low_candidates = [float(z) for z in z_axes if float(z) < z_plate]
    z_low = max(z_low_candidates) if z_low_candidates else float(z_axes[-2])
    z_high = z_plate

    stats: Dict[str, Any] = {
        "built": 0,
        "skipped_opening": 0,
        "skipped_small": 0,
        "walls": {},
        "band": {"z_low": z_low, "z_high": z_high},
    }

    LOG.info(
        "Phase4C braces: start corner-only band z=[%.3f..%.3f] profile=(%.3f,%.3f)",
        z_low, z_high, cfg.profile[0], cfg.profile[1]
    )

    axes_u = fp.get("axes_u") or {}
    for wall in ("N", "S", "E", "W"):
        w_axes = axes_u.get(wall, {})
        u_all = sorted(float(u) for u in (w_axes.get("all") or []))
        openings_wall = _collect_openings_for_wall(fp, wall)

        built_wall = 0
        skip_open = 0
        skip_small = 0

        if len(u_all) < 2:
            LOG.warning("braces: wall=%s has <2 u-axes, skipping", wall)
            stats["walls"][wall] = {"built": 0, "skipped_opening": 0, "skipped_small": 0, "u_axes": len(u_all)}
            continue

        # corner cells: leftmost and rightmost
        spans = [(0, 1), (len(u_all) - 2, len(u_all) - 1)]

        n_in = _wall_inward_normal(wall).normalized()

        for (i0, i1) in spans:
            u0 = u_all[i0]
            u1 = u_all[i1]

            cell_w = abs(u1 - u0)
            cell_h = abs(z_high - z_low)
            if cell_w < cfg.min_cell_w or cell_h < cfg.min_cell_h:
                skip_small += 1
                continue

            if _cell_is_inside_any_opening(u0=u0, u1=u1, z0=z_low, z1=z_high, openings_wall=openings_wall):
                skip_open += 1
                continue

            # inset endpoints inside the cell
            u_lo = min(u0, u1) + cfg.inset_u
            u_hi = max(u0, u1) - cfg.inset_u
            z_lo = z_low + cfg.inset_z
            z_hi = z_high - cfg.inset_z

            if u_hi <= u_lo or z_hi <= z_lo:
                skip_small += 1
                continue

            # Deterministic orientation:
            # - left corner: descending (\) for N/S, ascending (/) for E/W (doesn't matter structurally)
            # - right corner: opposite
            left_corner = (i0 == 0)

            if wall in ("N", "S"):
                # u -> x
                if left_corner:
                    p0_u, p0_z = u_lo, z_hi
                    p1_u, p1_z = u_hi, z_lo
                else:
                    p0_u, p0_z = u_lo, z_lo
                    p1_u, p1_z = u_hi, z_hi

                x0, y0 = _u_to_xy(wall, p0_u, x_min=x_min, x_max=x_max, center_x=center_x, halfW=halfW)
                x1, y1 = _u_to_xy(wall, p1_u, x_min=x_min, x_max=x_max, center_x=center_x, halfW=halfW)

            else:
                # E/W: u -> y
                if left_corner:
                    p0_u, p0_z = u_lo, z_hi
                    p1_u, p1_z = u_hi, z_lo
                else:
                    p0_u, p0_z = u_lo, z_lo
                    p1_u, p1_z = u_hi, z_hi

                x0, y0 = _u_to_xy(wall, p0_u, x_min=x_min, x_max=x_max, center_x=center_x, halfW=halfW)
                x1, y1 = _u_to_xy(wall, p1_u, x_min=x_min, x_max=x_max, center_x=center_x, halfW=halfW)

            p0 = Vector((x0, y0, p0_z)) + n_in * 0.01  # tiny inward bias
            p1 = Vector((x1, y1, p1_z)) + n_in * 0.01

            name = f"Brace_K_{wall}_{i0:02d}_{i1:02d}"

            obj = make_beam_rect(
                name,
                p0,
                p1,
                width=float(cfg.profile[0]),
                depth=float(cfg.profile[1]),
                collection=collection,
            )

            # Custom props for tooling
            try:
                obj["bv_domain"] = "fachwerk"
                obj["bv_kind"] = "knee_brace"
                obj["bv_wall"] = wall
                obj["bv_u0"] = float(u0)
                obj["bv_u1"] = float(u1)
                obj["bv_z0"] = float(z_low)
                obj["bv_z1"] = float(z_high)
            except Exception:
                pass

            if cfg.debug:
                mid = (p0 + p1) * 0.5
                _debug_empty(
                    name=f"DBG_{name}",
                    location=mid,
                    collection=debug_collection or collection,
                    payload={"wall": wall, "u0": u0, "u1": u1, "z0": z_low, "z1": z_high},
                    size=cfg.debug_empty_size,
                )

            built_wall += 1
            stats["built"] += 1

        stats["skipped_opening"] += skip_open
        stats["skipped_small"] += skip_small
        stats["walls"][wall] = {
            "built": built_wall,
            "skipped_opening": skip_open,
            "skipped_small": skip_small,
            "u_axes": len(u_all),
            "openings": len(openings_wall),
        }

        LOG.info(
            "braces wall=%s u_axes=%d openings=%d -> built=%d skipped_opening=%d skipped_small=%d",
            wall, len(u_all), len(openings_wall), built_wall, skip_open, skip_small
        )

    LOG.info(
        "Phase4C braces: done built=%d skipped_opening=%d skipped_small=%d",
        stats["built"], stats["skipped_opening"], stats["skipped_small"]
    )
    return stats
