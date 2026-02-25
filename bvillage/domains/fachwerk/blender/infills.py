# bvillage/domains/fachwerk/blender/infills.py

#
# Phase 4A: Gefache als eigenständige Mesh-Panels
# - Keine Booleans, kein durchgehendes Wand-Mesh
# - Deterministisch (Sortierung, Naming)
# - Logging + Debug Hooks
#
# Input: FramePlan-Dict (frameplan_to_dict Schema)
#   fp["dims"]      -> {L,W,H_e,z0}
#   fp["axes_u"]    -> per wall: {"all":[...], ...}
#   fp["axes_z"]    -> [z0,...,H_e]
#   fp["openings"]  -> list of {wall,u0,u1,z0,z1,...}
#
# Units: meters.
#
# IMPORTANT (Coord System):
# - In BVILLAGE reports, axis_x is typically [0 .. L] (not centered).
# - FramePlan u for N/S walls is centered around 0 ([-L/2 .. +L/2]).
# - Therefore N/S mapping is: x_world = center_x + u
# - E/W walls are at x = x_min (W) and x = x_max (E), and u maps to world y.

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import bpy
import bmesh
from mathutils import Vector

from bvillage.core.geom_eps import EPS_INSIDE

LOG = logging.getLogger("bvillage.domains.fachwerk.blender.infills")


@dataclass(frozen=True, slots=True)
class InfillConfig:
    """
    Configuration for infill panels.

    thickness:
        Panel thickness (normal direction).
    inset:
        Shrink panel within its cell to avoid z-fighting with timbers.
    face_clearance:
        Push panel slightly inward from the wall plane (in addition to half thickness).
    min_cell_w:
        Skip cells narrower than this.
    min_cell_h:
        Skip cells shorter than this.
    debug:
        Enable debug hooks (empties + custom props).
    """
    thickness: float = 0.08
    inset: float = 0.02
    face_clearance: float = 0.005
    min_cell_w: float = 0.12
    min_cell_h: float = 0.12
    debug: bool = False

    # Debug: show wall-plane empties (N/S/E/W) once per call
    debug_wall_markers: bool = True


# ---------------------------------------------------------------------
# Low-level mesh (no bpy.ops; context-free)
# ---------------------------------------------------------------------

def _make_box_mesh(name: str, hx: float, hy: float, hz: float) -> bpy.types.Mesh:
    """
    Create a box mesh centered at origin with half extents (hx, hy, hz).
    """
    mesh = bpy.data.meshes.new(name + "_M")
    bm = bmesh.new()

    # 8 verts (x,y,z) in (-1,+1) cube, scaled by half-extents
    verts = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                verts.append(bm.verts.new((sx * hx, sy * hy, sz * hz)))
    bm.verts.ensure_lookup_table()

    # face indices based on verts order above:
    # 0(-,-,-),1(-,-,+),2(-,+,-),3(-,+,+),4(+,-,-),5(+,-,+),6(+,+,-),7(+,+,+)
    faces = [
        (0, 1, 3, 2),  # -X
        (4, 6, 7, 5),  # +X
        (0, 4, 5, 1),  # -Y
        (2, 3, 7, 6),  # +Y
        (0, 2, 6, 4),  # -Z
        (1, 5, 7, 3),  # +Z
    ]
    for f in faces:
        bm.faces.new([bm.verts[i] for i in f])

    bm.normal_update()
    bm.to_mesh(mesh)
    bm.free()
    return mesh


def _link_object(obj: bpy.types.Object, collection: Optional[bpy.types.Collection]) -> None:
    if collection is None:
        bpy.context.collection.objects.link(obj)
    else:
        collection.objects.link(obj)


# ---------------------------------------------------------------------
# Coordinate mapping: wall-local u -> world (x,y) and inward normal
# ---------------------------------------------------------------------

def _wall_plane_and_normal(
    wall: str,
    *,
    x_min: float,
    x_max: float,
    center_x: float,
    halfW: float,
) -> Tuple[Vector, Vector]:
    """
    Return (origin_on_wall_plane, inward_normal).
    Inward means pointing toward building center.
    """
    wall = wall.upper()
    if wall == "N":
        return Vector((center_x, -halfW, 0.0)), Vector((0.0, +1.0, 0.0))
    if wall == "S":
        return Vector((center_x, +halfW, 0.0)), Vector((0.0, -1.0, 0.0))
    if wall == "E":
        return Vector((x_max, 0.0, 0.0)), Vector((-1.0, 0.0, 0.0))
    if wall == "W":
        return Vector((x_min, 0.0, 0.0)), Vector((+1.0, 0.0, 0.0))
    raise ValueError(f"Unknown wall '{wall}' (expected N/S/E/W)")


def _u_to_xy(
    wall: str,
    u: float,
    *,
    x_min: float,
    x_max: float,
    center_x: float,
    halfW: float,
) -> Tuple[float, float]:
    """
    Map wall-local u coordinate to world XY on that wall plane.

    BVILLAGE coord convention (typical):
      - world x runs [x_min .. x_max] ~ [0 .. L]
      - world y runs [-halfW .. +halfW]
      - FramePlan u for N/S walls is centered around 0: u in [-L/2..+L/2]
        -> world x = center_x + u
      - For E/W walls, u runs along y:
        -> world y = u, world x fixed at x_min/x_max
    """
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


# ---------------------------------------------------------------------
# Opening checks
# ---------------------------------------------------------------------

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
    """
    True if the cell lies strictly inside any opening on that wall.
    Uses EPS_INSIDE margin to avoid boundary ambiguity.
    """
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

        # cell fully inside opening
        if lo_u >= o_lo_u and hi_u <= o_hi_u and lo_z >= o_lo_z and hi_z <= o_hi_z:
            return True

    return False


# ---------------------------------------------------------------------
# Debug helpers
# ---------------------------------------------------------------------

def _debug_empty(
    *,
    name: str,
    location: Vector,
    collection: Optional[bpy.types.Collection],
    payload: Optional[Dict[str, Any]] = None,
    size: float = 0.18,
) -> None:
    """
    Create an Empty at location with custom props. Never breaks build.
    """
    try:
        empty = bpy.data.objects.new(name, None)
        empty.empty_display_type = "PLAIN_AXES"
        empty.empty_display_size = float(size)
        empty.location = Vector(location)
        _link_object(empty, collection)
        if payload:
            for k, v in payload.items():
                empty[f"bv_{k}"] = v
    except Exception:
        LOG.exception("debug empty failed: %s", name)


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def build_infills(
    *,
    fp: Dict[str, Any],
    house: Dict[str, Any],
    collection: Optional[bpy.types.Collection],
    config: Optional[InfillConfig] = None,
    debug_collection: Optional[bpy.types.Collection] = None,
) -> Dict[str, Any]:
    """
    Build infill panels for all walls using FramePlan dict + house dict.

    Parameters
    ----------
    fp:
        FramePlan dict payload (frameplan_to_dict schema).
    house:
        Blender builder house dict (from build_frame._coerce_house()).
        Must provide axis_x and axis_y.
    collection:
        Target Blender collection for infill objects.
    config:
        InfillConfig.
    debug_collection:
        Optional collection for debug helpers (empties).
    """
    cfg = config or InfillConfig()

    axis_x = house.get("axis_x") or []
    axis_y = house.get("axis_y") or []
    if not axis_x or not axis_y:
        raise ValueError("build_infills: house must provide axis_x and axis_y")

    x_min = float(min(axis_x))
    x_max = float(max(axis_x))
    center_x = 0.5 * (x_min + x_max)

    # y is expected symmetric in BVILLAGE reports, but compute robustly anyway
    y_min = float(min(axis_y))
    y_max = float(max(axis_y))
    halfW = 0.5 * (y_max - y_min)

    z_axes = list(fp.get("axes_z") or [])
    if len(z_axes) < 2:
        raise ValueError("build_infills: fp['axes_z'] must contain at least 2 values")

    axes_u = fp.get("axes_u") or {}
    if not isinstance(axes_u, dict):
        raise ValueError("build_infills: fp['axes_u'] must be a dict")

    stats: Dict[str, Any] = {
        "panels_built": 0,
        "panels_skipped_opening": 0,
        "panels_skipped_small": 0,
        "walls": {},
        "coord": {
            "x_min": x_min,
            "x_max": x_max,
            "center_x": center_x,
            "halfW": halfW,
        },
    }

    LOG.info(
        "Phase4A infills: start (x=[%.3f..%.3f] center_x=%.3f halfW=%.3f z_axes=%d thickness=%.3f inset=%.3f)",
        x_min, x_max, center_x, halfW, len(z_axes), cfg.thickness, cfg.inset
    )

    # optional wall-plane markers
    if cfg.debug and cfg.debug_wall_markers:
        for wall in ("N", "S", "E", "W"):
            origin, n_in = _wall_plane_and_normal(
                wall,
                x_min=x_min,
                x_max=x_max,
                center_x=center_x,
                halfW=halfW,
            )
            _debug_empty(
                name=f"DBG_WALL_{wall}",
                location=origin + n_in.normalized() * 0.25,
                collection=debug_collection or collection,
                payload={"wall": wall, "nx": float(n_in.x), "ny": float(n_in.y)},
                size=0.25,
            )

    for wall in ("N", "S", "E", "W"):
        w_axes = axes_u.get(wall, {})
        u_all = list(w_axes.get("all") or [])
        u_all = sorted(float(u) for u in u_all)

        if len(u_all) < 2:
            LOG.warning("infills: wall=%s has <2 u-axes, skipping", wall)
            continue

        openings_wall = _collect_openings_for_wall(fp, wall)

        built_wall = 0
        skip_open = 0
        skip_small = 0

        origin, n_in = _wall_plane_and_normal(
            wall,
            x_min=x_min,
            x_max=x_max,
            center_x=center_x,
            halfW=halfW,
        )
        n_in = n_in.normalized()

        for iu in range(len(u_all) - 1):
            u0 = u_all[iu]
            u1 = u_all[iu + 1]

            raw_w = abs(u1 - u0)
            cell_w = raw_w - cfg.inset
            if cell_w < cfg.min_cell_w:
                # skip entire z-stack for this narrow span
                skip_small += (len(z_axes) - 1)
                continue

            for iz in range(len(z_axes) - 1):
                z0 = float(z_axes[iz])
                z1 = float(z_axes[iz + 1])

                raw_h = abs(z1 - z0)
                cell_h = raw_h - cfg.inset
                if cell_h < cfg.min_cell_h:
                    skip_small += 1
                    continue

                if _cell_is_inside_any_opening(
                    u0=u0, u1=u1, z0=z0, z1=z1, openings_wall=openings_wall
                ):
                    skip_open += 1
                    continue

                name = f"Gefach_{wall}_{iu:02d}_{iz:02d}"

                # panel center in wall coords
                cu = 0.5 * (u0 + u1)
                cz = 0.5 * (z0 + z1)

                x, y = _u_to_xy(
                    wall,
                    cu,
                    x_min=x_min,
                    x_max=x_max,
                    center_x=center_x,
                    halfW=halfW,
                )

                # dimensions (half extents)
                hx = 0.5 * max(1e-9, raw_w - cfg.inset)
                hz = 0.5 * max(1e-9, raw_h - cfg.inset)
                hy = 0.5 * max(1e-9, cfg.thickness)

                mesh = _make_box_mesh(name, hx=hx, hy=hy, hz=hz)
                obj = bpy.data.objects.new(name, mesh)

                # place slightly inward (avoid z-fighting and ensure inside face)
                obj.location = Vector((x, y, cz)) + n_in * (cfg.face_clearance + hy)

                # For E/W walls: local X should span world Y (u direction), so rotate 90° around Z
                if wall in ("E", "W"):
                    obj.rotation_euler = (0.0, 0.0, 1.5707963267948966)

                _link_object(obj, collection)

                # Custom props
                obj["bv_domain"] = "fachwerk"
                obj["bv_kind"] = "infill"
                obj["bv_wall"] = wall
                obj["bv_u0"] = float(u0)
                obj["bv_u1"] = float(u1)
                obj["bv_z0"] = float(z0)
                obj["bv_z1"] = float(z1)

                if cfg.debug:
                    _debug_empty(
                        name=f"DBG_{name}",
                        location=obj.location,
                        collection=debug_collection or collection,
                        payload={
                            "wall": wall,
                            "iu": iu,
                            "iz": iz,
                            "u0": float(u0),
                            "u1": float(u1),
                            "z0": float(z0),
                            "z1": float(z1),
                        },
                        size=0.15,
                    )

                built_wall += 1
                stats["panels_built"] += 1

        stats["panels_skipped_opening"] += skip_open
        stats["panels_skipped_small"] += skip_small
        stats["walls"][wall] = {
            "built": built_wall,
            "skipped_opening": skip_open,
            "skipped_small": skip_small,
            "u_axes": len(u_all),
            "openings": len(openings_wall),
        }

        LOG.info(
            "infills wall=%s u_axes=%d openings=%d -> built=%d skipped_opening=%d skipped_small=%d",
            wall, len(u_all), len(openings_wall), built_wall, skip_open, skip_small
        )

    LOG.info(
        "Phase4A infills: done built=%d skipped_opening=%d skipped_small=%d",
        stats["panels_built"], stats["panels_skipped_opening"], stats["panels_skipped_small"]
    )
    return stats
