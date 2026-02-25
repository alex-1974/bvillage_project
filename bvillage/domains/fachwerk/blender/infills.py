# bvillage/domains/fachwerk/blender/infills.py

import logging
from typing import Dict, Any

import bpy
from mathutils import Vector

LOG = logging.getLogger("bvillage.domains.fachwerk.blender.infills")


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
        raise ValueError("Need fp['dims'] (L,W) or house axis_x/axis_y")

    x_min = float(min(axis_x))
    x_max = float(max(axis_x))
    center_x = 0.5 * (x_min + x_max)
    halfW = 0.5 * (float(max(axis_y)) - float(min(axis_y)))
    return x_min, x_max, center_x, halfW


def _u_axes_as_sorted_list(u_axes_any):
    """
    Normalize u-axes to a sorted unique float list.

    Supported shapes:
      - list/tuple of numbers
      - dict: values are numbers OR list/tuple of numbers OR dict of lists
        e.g. {0: 1.2, 1: 2.4}
        e.g. {"primary":[...], "opening":[...], "secondary":[...]}
        e.g. {"bands": {"primary":[...], "opening":[...]}}
    """
    vals = []

    def _collect(x):
        if x is None:
            return
        if isinstance(x, (int, float)):
            vals.append(float(x))
            return
        if isinstance(x, str):
            # allow numeric strings
            try:
                vals.append(float(x))
            except Exception:
                pass
            return
        if isinstance(x, (list, tuple)):
            for it in x:
                _collect(it)
            return
        if isinstance(x, dict):
            for v in x.values():
                _collect(v)
            return
        # ignore unknown types

    _collect(u_axes_any)

    # unique + sort
    uniq = sorted(set(vals))
    return uniq

def _z_axes_as_sorted_list(z_axes_any):
    """
    Same as _u_axes_as_sorted_list but for z-axes.
    """
    return _u_axes_as_sorted_list(z_axes_any)


def _openings_as_list(openings_any):
    """
    Normalize openings to list of dicts.
    """
    if openings_any is None:
        return []
    if isinstance(openings_any, list):
        return openings_any
    if isinstance(openings_any, dict):
        # allow dict of {id: opening_dict}
        return list(openings_any.values())
    return []


def build_infills(
    *,
    fp: Dict[str, Any],
    house: Dict[str, Any],
    collection: bpy.types.Collection,
):
    """
    Build rectangular infill panels between u-axes and z-axes.

    FramePlan-first:
      - uses fp['dims'] (L,W) for basis whenever available
      - only falls back to house axis_x/axis_y
    """

    x_min, x_max, center_x, halfW = _basis_from_fp_or_house(fp, house)

    axes_u = fp.get("axes_u") or {}
    axes_z_any = fp.get("axes_z") or []
    axes_z = _z_axes_as_sorted_list(axes_z_any)

    openings = _openings_as_list(fp.get("openings"))

    if len(axes_z) < 2:
        return

    built = 0

    for wall, u_axes_any in axes_u.items():
        u_axes = _u_axes_as_sorted_list(u_axes_any)
        if len(u_axes) < 2:
            continue

        for i in range(len(u_axes) - 1):
            u0 = float(u_axes[i])
            u1 = float(u_axes[i + 1])

            for j in range(len(axes_z) - 1):
                z0 = float(axes_z[j])
                z1 = float(axes_z[j + 1])

                # skip cells intersecting an opening
                skip = False
                for op in openings:
                    try:
                        if op.get("wall") != wall:
                            continue

                        # support both key styles: u0/u1/z0/z1 OR u=[a,b], z=[c,d]
                        ou0 = op.get("u0")
                        ou1 = op.get("u1")
                        if ou0 is None or ou1 is None:
                            ur = op.get("u")
                            if isinstance(ur, (list, tuple)) and len(ur) == 2:
                                ou0, ou1 = ur
                        oz0 = op.get("z0")
                        oz1 = op.get("z1")
                        if oz0 is None or oz1 is None:
                            zr = op.get("z")
                            if isinstance(zr, (list, tuple)) and len(zr) == 2:
                                oz0, oz1 = zr

                        if ou0 is None or ou1 is None or oz0 is None or oz1 is None:
                            continue

                        ou0 = float(ou0)
                        ou1 = float(ou1)
                        oz0 = float(oz0)
                        oz1 = float(oz1)

                        if not (u1 <= ou0 or u0 >= ou1):
                            if not (z1 <= oz0 or z0 >= oz1):
                                skip = True
                                break
                    except Exception:
                        continue

                if skip:
                    continue

                # map (wall,u,z) to 3D
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

                mesh = bpy.data.meshes.new(f"Infill_{wall}_{i}_{j}")
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

                built += 1

    LOG.info("Phase4A infills: done built=%d", built)
