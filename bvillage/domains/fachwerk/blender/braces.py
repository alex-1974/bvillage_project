# bvillage/domains/fachwerk/blender/braces.py

import logging
from typing import Any, Iterable

import bpy
from mathutils import Vector

from bvillage.core.errors import SchemaError
from .materials_assign import assign_member_material

__all__ = ["build_braces_corner_band"]

LOG = logging.getLogger("bvillage.domains.fachwerk.blender.braces")


def _require_basis(fp: dict[str, Any], *, house: dict[str, Any]) -> dict[str, float]:
    basis = fp.get("basis")
    if isinstance(basis, dict) and all(k in basis for k in ("x_min", "x_max", "center_x", "halfW")):
        return {
            "x_min": float(basis["x_min"]),
            "x_max": float(basis["x_max"]),
            "center_x": float(basis["center_x"]),
            "halfW": float(basis["halfW"]),
        }

    # Derive renderer basis from required house params (NO magic defaults)
    try:
        L = float(house["L"])
        W = float(house["W"])
    except Exception:
        raise SchemaError("Braces: missing required house keys 'L'/'W' for basis derivation")

    if not (L > 0.0 and W > 0.0):
        raise SchemaError("Braces: invalid house dims for basis derivation (L/W must be > 0)")

    x_min = 0.0
    x_max = L
    center_x = 0.5 * L
    halfW = 0.5 * W
    return {"x_min": x_min, "x_max": x_max, "center_x": center_x, "halfW": halfW}


def _map_wall_uvz_to_world(*, wall: str, u: float, z: float, basis: dict[str, float]) -> Vector:
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
    raise SchemaError(f"Braces: unknown wall '{wall}'")


def _iter_braces(fp: dict[str, Any]) -> Iterable[dict[str, Any]]:
    members = fp.get("members")
    if not isinstance(members, dict):
        raise SchemaError("Braces: schema requires fp['members'] dict")
    braces = members.get("braces")
    if braces is None:
        return []
    if not isinstance(braces, list):
        raise SchemaError("Braces: schema requires fp['members']['braces'] list")
    return (b for b in braces if isinstance(b, dict))


def _resolve_brace_profile(*, brace: dict[str, Any], house: dict[str, Any]) -> tuple[float, float]:
    prof = brace.get("profile")
    if isinstance(prof, dict) and "w" in prof and "d" in prof:
        return float(prof["w"]), float(prof["d"])

    # Fallback only via house artifact (policy-driven), NOT magic constants
    hs = house.get("brace_section")
    if isinstance(hs, (list, tuple)) and len(hs) == 2:
        return float(hs[0]), float(hs[1])

    raise SchemaError("Braces: missing brace profile (brace.profile[w,d] or house.brace_section)")


def build_braces_corner_band(
    *,
    fp: dict[str, Any],
    house: dict[str, Any],
    collection: bpy.types.Collection,
    ctx_view: Any = None,
    debug: bool = False,
) -> int:
    from .timber import make_beam_rect

    basis = _require_basis(fp, house=house)

    built = 0
    for i, b in enumerate(_iter_braces(fp)):
        if b.get("role") != "BRACE_DIAG":
            continue

        wall = b.get("wall")
        if wall not in ("N", "S", "E", "W"):
            raise SchemaError(f"Braces: brace[{i}] invalid/missing wall")

        # required geometry
        try:
            u0 = float(b["u0"])
            z0 = float(b["z0"])
            u1 = float(b["u1"])
            z1 = float(b["z1"])
        except Exception:
            raise SchemaError(f"Braces: brace[{i}] missing required numeric fields u0/u1/z0/z1")

        p0 = _map_wall_uvz_to_world(wall=str(wall), u=u0, z=z0, basis=basis)
        p1 = _map_wall_uvz_to_world(wall=str(wall), u=u1, z=z1, basis=basis)

        w, d = _resolve_brace_profile(brace=b, house=house)

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
