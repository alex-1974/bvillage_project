# bvillage/domains/timber_frame/blender/infills.py

from __future__ import annotations

import logging
from typing import Any

import bpy
from mathutils import Vector

from bvillage.core.errors import SchemaError
from bvillage.core.ontology.structural_terms import INFILL_CELL

from .materials_assign import assign_member_material

__all__ = ["build_infills"]

LOG = logging.getLogger(__name__)


def _require_basis(fp: dict[str, Any]) -> dict[str, float]:
    """
    Require canonical basis for members-first rendering.

    Mandatory keys
    --------------
    - x_min
    - x_max
    - center_x
    - halfW
    """
    basis = fp.get("basis")
    if not isinstance(basis, dict):
        raise SchemaError("Infills: missing canonical frameplan basis")

    required = ("x_min", "x_max", "center_x", "halfW")
    out: dict[str, float] = {}

    for key in required:
        if key not in basis:
            raise SchemaError(f"Infills: basis missing required key '{key}'")
        try:
            out[key] = float(basis[key])
        except Exception as exc:
            raise SchemaError(f"Infills: invalid basis value for '{key}'") from exc

    return out


def _make_infill_quad(
    collection: bpy.types.Collection,
    name: str,
    v00: Vector,
    v10: Vector,
    v11: Vector,
    v01: Vector,
) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(name + "_Mesh")
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    mesh.from_pydata([v00, v10, v11, v01], [], [(0, 1, 2, 3)])
    mesh.update()
    return obj


def _resolve_infill_material_role(*, cell: dict[str, Any]) -> str:
    mr = cell.get("material_role")
    if isinstance(mr, str) and mr:
        return mr
    return "INFILL"


def build_infills(
    *,
    fp: dict[str, Any],
    collection: bpy.types.Collection,
    ctx_view: Any = None,
    debug: bool = False,
) -> int:
    """
    Build infills strictly from FramePlan.members.infills.

    Contract
    --------
    - canonical members-first only
    - no house dependency
    - no legacy schema path
    """
    _ = debug

    members = fp.get("members")
    if not isinstance(members, dict):
        raise SchemaError("Infills: missing members dict")

    cells = members.get("infills")
    if cells is None:
        return 0
    if not isinstance(cells, list):
        raise SchemaError("Infills: members.infills must be a list")
    if not cells:
        return 0

    basis = _require_basis(fp)
    x_min = basis["x_min"]
    x_max = basis["x_max"]
    center_x = basis["center_x"]
    half_w = basis["halfW"]

    built = 0
    for i, cell in enumerate(cells):
        if not isinstance(cell, dict):
            continue
        if cell.get("tid") != INFILL_CELL:
            continue

        wall = cell.get("wall")
        if wall not in ("N", "S", "E", "W"):
            raise SchemaError(f"Infills: INFILL_CELL[{i}] missing/invalid wall")

        try:
            u0 = float(cell["u0"])
            u1 = float(cell["u1"])
            z0 = float(cell["z0"])
            z1 = float(cell["z1"])
        except Exception as exc:
            raise SchemaError(
                f"Infills: INFILL_CELL[{i}] missing required numeric u0/u1/z0/z1"
            ) from exc

        if wall == "N":
            v00 = Vector((center_x + u0, -half_w, z0))
            v10 = Vector((center_x + u1, -half_w, z0))
            v11 = Vector((center_x + u1, -half_w, z1))
            v01 = Vector((center_x + u0, -half_w, z1))
        elif wall == "S":
            v00 = Vector((center_x + u0, half_w, z0))
            v10 = Vector((center_x + u1, half_w, z0))
            v11 = Vector((center_x + u1, half_w, z1))
            v01 = Vector((center_x + u0, half_w, z1))
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

        name = cell.get("id") if isinstance(cell.get("id"), str) and cell.get("id") else f"Infill_{wall}_{built:04d}"
        obj = _make_infill_quad(collection, name, v00, v10, v11, v01)

        if ctx_view is not None:
            mat_member = dict(cell)
            if "id" not in mat_member or not mat_member["id"]:
                mat_member["id"] = name
            mat_member["role"] = _resolve_infill_material_role(cell=cell)
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

    LOG.info("Infills: members-first built=%d", built)
    return built
