# bvillage/domains/fachwerk/blender/infills.py

import logging
from typing import Any

import bpy
from mathutils import Vector

from .materials_assign import assign_member_material

__all__ = ['build_infills']

LOG = logging.getLogger("bvillage.domains.fachwerk.blender.infills")

# ---------------------------------------------------------------------
# Canonical FramePlan-first helpers
# ---------------------------------------------------------------------

def _get_basis(fp: dict[str, Any]) -> dict[str, float]:
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

def _flatten_numeric(x: Any) -> list[float]:
    """Collect numeric values from nested lists/dicts; return sorted unique floats."""
    vals: list[float] = []

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

def _get_axes_z(fp: dict[str, Any]) -> list[float]:
    # Prefer canonical
    z = fp.get("axes_z_flat")
    if isinstance(z, list) and z:
        return [float(v) for v in z]
    # Fallback: flatten anything
    return _flatten_numeric(fp.get("axes_z"))

def _get_axes_u_flat(fp: dict[str, Any]) -> dict[str, list[float]]:
    # Prefer canonical
    axes = fp.get("axes_u_flat")
    if isinstance(axes, dict) and axes:
        out: dict[str, list[float]] = {}
        for wall in ("N", "S", "E", "W"):
            v = axes.get(wall, [])
            out[wall] = [float(x) for x in _flatten_numeric(v)]
        return out

    # Fallback: flatten fp["axes_u"]
    axes_u = fp.get("axes_u") or {}
    out: dict[str, list[float]] = {}
    if not isinstance(axes_u, dict):
        return {w: [] for w in ("N", "S", "E", "W")}

    for wall in ("N", "S", "E", "W"):
        w = axes_u.get(wall)
        if isinstance(w, dict) and "all" in w:
            out[wall] = _flatten_numeric(w.get("all"))
        else:
            out[wall] = _flatten_numeric(w)

    return out

def _get_openings(fp: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Prefer canonical fp["openings_norm"] (u0/u1/z0/z1 floats).
    Fallback: normalize fp["openings"] best-effort.
    """
    on = fp.get("openings_norm")
    if isinstance(on, list):
        out = []
        for op in on:
            if not isinstance(op, dict):
                continue
            if all(k in op for k in ("wall", "u0", "u1", "z0", "z1")):
                o2 = dict(op)
                o2["u0"] = float(o2["u0"])
                o2["u1"] = float(o2["u1"])
                o2["z0"] = float(o2["z0"])
                o2["z1"] = float(o2["z1"])
                out.append(o2)
        return out

    openings = fp.get("openings") or []
    if isinstance(openings, dict):
        openings_list = list(openings.values())
    elif isinstance(openings, list):
        openings_list = openings
    else:
        openings_list = []

    out = []
    for op in openings_list:
        if not isinstance(op, dict):
            continue
        wall = op.get("wall")
        if wall is None:
            continue

        u0 = op.get("u0")
        u1 = op.get("u1")
        if u0 is None or u1 is None:
            ur = op.get("u")
            if isinstance(ur, (list, tuple)) and len(ur) == 2:
                u0, u1 = ur[0], ur[1]

        z0 = op.get("z0")
        z1 = op.get("z1")
        if z0 is None or z1 is None:
            zr = op.get("z")
            if isinstance(zr, (list, tuple)) and len(zr) == 2:
                z0, z1 = zr[0], zr[1]

        if u0 is None or u1 is None or z0 is None or z1 is None:
            continue

        o2 = dict(op)
        o2["u0"] = float(u0)
        o2["u1"] = float(u1)
        o2["z0"] = float(z0)
        o2["z1"] = float(z1)
        out.append(o2)

    return out

def _cell_hits_opening(wall: str, u0: float, u1: float, z0: float, z1: float, openings: list[dict[str, Any]]) -> bool:
    for op in openings:
        if op.get("wall") != wall:
            continue
        ou0 = float(op["u0"])
        ou1 = float(op["u1"])
        oz0 = float(op["z0"])
        oz1 = float(op["z1"])

        if not (u1 <= ou0 or u0 >= ou1):
            if not (z1 <= oz0 or z0 >= oz1):
                return True
    return False

# ---------------------------------------------------------------------
# Materials (local, deterministic)
# ---------------------------------------------------------------------

def _make_infill_quad(
    collection: bpy.types.Collection,
    name: str,
    v00: Vector,
    v10: Vector,
    v11: Vector,
    v01: Vector,
    *,
    member_for_material: dict[str, Any] | None = None,
    ctx_view: Any = None,
) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(mesh.name, mesh)
    collection.objects.link(obj)

    verts = [
        (v00.x, v00.y, v00.z),
        (v10.x, v10.y, v10.z),
        (v11.x, v11.y, v11.z),
        (v01.x, v01.y, v01.z),
    ]
    mesh.from_pydata(verts, [], [(0, 1, 2, 3)])
    mesh.update()

    if member_for_material is not None and ctx_view is not None:
        try:
            assign_member_material(
                obj=obj,
                member=member_for_material,
                ctx_view=ctx_view,
                default_material_id="brick.historic_mid",
                name_hint=f"BV_{name}",
            )
        except Exception:
            LOG.exception("Infills: material assignment failed for %s member=%s", name, member_for_material)

    return obj

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def build_infills(
    *,
    fp: dict[str, Any],
    house: dict[str, Any],  # kept for signature compatibility
    collection: bpy.types.Collection,
    ctx_view: Any = None,   # optional (dict view, preferred; ctx may be frozen)
):
    basis = _get_basis(fp)
    x_min = basis["x_min"]
    x_max = basis["x_max"]
    center_x = basis["center_x"]
    halfW = basis["halfW"]

    members = fp.get("members")
    if not isinstance(members, dict):
        raise ValueError("Infills: schema requires fp['members']")

    cells = members.get("infills")
    if not isinstance(cells, list):
        raise ValueError("Infills: schema requires fp['members']['infills'] list")

    built = 0
    for c in cells:
        if not isinstance(c, dict):
            continue
        if c.get("role") != "INFILL_CELL":
            continue

        wall = c.get("wall")
        if wall not in ("N", "S", "E", "W"):
            continue

        u0 = float(c["u0"])
        u1 = float(c["u1"])
        z0 = float(c["z0"])
        z1 = float(c["z1"])

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
        else:  # "W"
            v00 = Vector((x_min, u0, z0))
            v10 = Vector((x_min, u1, z0))
            v11 = Vector((x_min, u1, z1))
            v01 = Vector((x_min, u0, z1))

        name = f"Infill_{wall}_{built:04d}"

        # For material resolution, we create a lightweight "material role" wrapper
        # so ctx_view.role defaults can target infill materials.
        mat_member = dict(c)
        mat_member["id"] = mat_member.get("id", name)
        # This role is what ctx_view.material_id_default_by_role should map.
        # (If absent, it falls back to default_material_id above.)
        mat_member["role"] = mat_member.get("material_role", "INFILL_BRICK")

        _make_infill_quad(
            collection,
            name,
            v00,
            v10,
            v11,
            v01,
            member_for_material=mat_member,
            ctx_view=ctx_view,
        )

        built += 1

    LOG.info("Phase4A infills: members-first done built=%d", built)
