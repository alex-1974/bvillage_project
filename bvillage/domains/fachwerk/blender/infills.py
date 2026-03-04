# bvillage/domains/fachwerk/blender/infills.py

import logging
from typing import Any

import bpy
from mathutils import Vector

from bvillage.core.errors import SchemaError
from .materials_assign import assign_member_material

from bvillage.core.ontology.structural_terms import INFILL_CELL

__all__ = ["build_infills"]

LOG = logging.getLogger(__name__)


def _require_basis(fp: dict[str, Any], *, house: dict[str, Any]) -> dict[str, float]:
    basis = fp.get("basis")
    if isinstance(basis, dict) and all(k in basis for k in ("x_min", "x_max", "center_x", "halfW")):
        return {
            "x_min": float(basis["x_min"]),
            "x_max": float(basis["x_max"]),
            "center_x": float(basis["center_x"]),
            "halfW": float(basis["halfW"]),
        }

    # deterministic fallback (should exist in emitted fp anyway)
    try:
        L = float(house["L"])
        W = float(house["W"])
    except Exception:
        raise SchemaError("Infills: missing required house keys 'L'/'W' for basis derivation")

    if not (L > 0.0 and W > 0.0):
        raise SchemaError("Infills: invalid house dims for basis derivation")

    return {"x_min": 0.0, "x_max": L, "center_x": 0.5 * L, "halfW": 0.5 * W}


def _make_infill_quad(collection: bpy.types.Collection, name: str, v00: Vector, v10: Vector, v11: Vector, v01: Vector) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(name + "_Mesh")
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    mesh.from_pydata([v00, v10, v11, v01], [], [(0, 1, 2, 3)])
    mesh.update()
    return obj


def _resolve_infill_material_role(*, cell: dict[str, Any], house: dict[str, Any]) -> str:
    mr = cell.get("material_role")
    if isinstance(mr, str) and mr:
        return mr
    dmr = house.get("default_infill_material_role")
    if isinstance(dmr, str) and dmr:
        return dmr
    return "INFILL"


def build_infills(
    *,
    fp: dict[str, Any],
    house: dict[str, Any],
    collection: bpy.types.Collection,
    ctx_view: Any = None,
    debug: bool = False,
) -> int:
    members = fp.get("members")
    if not isinstance(members, dict):
        LOG.info("Phase4A infills: no members dict -> nothing to build")
        return 0

    cells = members.get("infills") or []
    if not isinstance(cells, list) or not cells:
        LOG.info("Phase4A infills: members.infills empty -> nothing to build")
        return 0

    basis = _require_basis(fp, house=house)
    x_min = basis["x_min"]
    x_max = basis["x_max"]
    center_x = basis["center_x"]
    halfW = basis["halfW"]

    built = 0
    for i, c in enumerate(cells):
        if not isinstance(c, dict):
            continue
        if c.get("tid") != INFILL_CELL:
            continue

        wall = c.get("wall")
        if wall not in ("N", "S", "E", "W"):
            raise SchemaError(f"Infills: INFILL_CELL[{i}] missing/invalid wall")

        try:
            u0 = float(c["u0"])
            u1 = float(c["u1"])
            z0 = float(c["z0"])
            z1 = float(c["z1"])
        except Exception:
            raise SchemaError(f"Infills: INFILL_CELL[{i}] missing required numeric u0/u1/z0/z1")

        if wall == "N":
            v00 = Vector((center_x + u0, -halfW, z0))
            v10 = Vector((center_x + u1, -halfW, z0))
            v11 = Vector((center_x + u1, -halfW, z1))
            v01 = Vector((center_x + u0, -halfW, z1))
        elif wall == "S":
            v00 = Vector((center_x + u0, halfW, z0))
            v10 = Vector((center_x + u1, halfW, z0))
            v11 = Vector((center_x + u1, halfW, z1))
            v01 = Vector((center_x + u0, halfW, z1))
        elif wall == "E":
            v00 = Vector((x_max, u0, z0))
            v10 = Vector((x_max, u1, z0))
            v11 = Vector((x_max, u1, z1))
            v01 = Vector((x_max, u0, z1))
        else:  # W
            v00 = Vector((x_min, u0, z0))
            v10 = Vector((x_min, u1, z0))
            v11 = Vector((x_min, u1, z1))
            v01 = Vector((x_min, u0, z1))

        name = f"Infill_{wall}_{built:04d}"
        obj = _make_infill_quad(collection, name, v00, v10, v11, v01)

        if ctx_view:
            # Material role only (do not use for geometry)
            mat_member = dict(c)
            if "id" not in mat_member or not mat_member["id"]:
                mat_member["id"] = name
            mat_member["role"] = _resolve_infill_material_role(cell=c, house=house)
            try:
                assign_member_material(
                    obj=obj,
                    member=mat_member,
                    ctx_view=ctx_view,
                    default_material_id="mortar.lime_weak",
                    name_hint=f"BV_{name}",
                )
            except Exception:
                LOG.exception("Infills: material assignment failed for %s member=%s", name, mat_member)

        built += 1

    LOG.info("Phase4A infills: members-first done built=%d", built)
    return built
