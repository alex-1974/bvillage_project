# bvillage/domains/fachwerk/blender/braces.py

import logging
from typing import Any, Dict, Tuple

import bpy
from mathutils import Vector
from .materials_assign import assign_member_material

LOG = logging.getLogger("bvillage.domains.fachwerk.blender.braces")


def _get_basis(fp: Dict[str, Any]) -> Dict[str, float]:
    basis = fp.get("basis")
    if isinstance(basis, dict):
        return {
            "x_min": float(basis["x_min"]),
            "x_max": float(basis["x_max"]),
            "center_x": float(basis["center_x"]),
            "halfW": float(basis["halfW"]),
        }

    # fallback from dims
    dims = fp.get("dims") or {}
    L = float(dims.get("L", 0.0))
    W = float(dims.get("W", 0.0))
    return {
        "x_min": 0.0,
        "x_max": L,
        "center_x": 0.5 * L,
        "halfW": 0.5 * W,
    }


def _map_wall_uvz_to_world(
    *,
    wall: str,
    u: float,
    z: float,
    basis: Dict[str, float],
) -> Vector:
    x_min = basis["x_min"]
    x_max = basis["x_max"]
    center_x = basis["center_x"]
    halfW = basis["halfW"]

    if wall == "N":
        return Vector((center_x + u, -halfW, z))
    if wall == "S":
        return Vector((center_x + u, +halfW, z))
    if wall == "E":
        return Vector((x_max, u, z))
    if wall == "W":
        return Vector((x_min, u, z))
    raise ValueError(f"Unknown wall '{wall}'")


def build_braces_corner_band(
    *,
    fp,
    house,
    collection,
    ctx_view=None,
    debug=False,
):
    from .timber import make_beam_rect

    members = fp.get("members")
    braces = members.get("braces", [])

    basis = _get_basis(fp)

    built = 0
    for i, b in enumerate(braces):
        if b.get("role") != "BRACE_DIAG":
            continue

        wall = str(b["wall"])
        u0 = float(b["u0"]); z0 = float(b["z0"])
        u1 = float(b["u1"]); z1 = float(b["z1"])

        p0 = _map_wall_uvz_to_world(wall=wall, u=u0, z=z0, basis=basis)
        p1 = _map_wall_uvz_to_world(wall=wall, u=u1, z=z1, basis=basis)

        prof = b.get("profile") or {}
        w = float(prof.get("w", 0.12))
        d = float(prof.get("d", 0.12))

        name = f"Brace_{wall}_{i:04d}"
        make_beam_rect(name, p0, p1, width=w, depth=d, collection=collection)

        if ctx_view:
            obj = collection.objects.get(name)
            try:
                assign_member_material(
                    obj=obj,
                    member=b,
                    ctx_view=ctx_view,
                    default_material_id="timber.spruce",
                    name_hint=f"BV_{name}",
                )
            except Exception:
                LOG.exception("Braces: material assignment failed for %s member=%s", name, b)

        built += 1

    return built
