# bvillage/domains/fachwerk/blender/timber.py

import bpy
import bmesh
from mathutils import Vector, Matrix


def _safe_frame_from_tangent(t: Vector, up_hint: Vector = Vector((0, 0, 1))) -> Matrix:
    """
    Build orthonormal frame from tangent vector.
    Returns 3x3 rotation matrix with columns (R, U, T).
    """
    T = t.normalized()

    # avoid degeneracy if tangent is near the up vector
    if abs(T.dot(up_hint.normalized())) > 0.98:
        up_hint = Vector((0, 1, 0))

    U = up_hint - T * T.dot(up_hint)
    if U.length < 1e-6:
        up_hint = Vector((1, 0, 0))
        U = up_hint - T * T.dot(up_hint)

    if U.length < 1e-6:
        # last resort
        U = Vector((0, 1, 0))

    U.normalize()
    R = T.cross(U).normalized()
    U = R.cross(T).normalized()

    # Matrix columns are X=R, Y=U, Z=T; Blender wants row-major for @ usage, so transpose.
    return Matrix((R, U, T)).transposed()


def make_beam_rect(
    name: str,
    start: Vector,
    end: Vector,
    width: float,
    depth: float,
    up_hint: Vector = Vector((0, 0, 1)),
    collection=None,
):
    """
    Create rectangular timber by extruding a rectangle profile from start to end.
    Units: meters.

    width -> local X
    depth -> local Y (vertical-ish if up_hint=Z)
    """
    start = Vector(start)
    end = Vector(end)
    direction = end - start
    length = direction.length

    if length < 1e-6:
        raise ValueError(f"{name}: start/end too close")

    rot = _safe_frame_from_tangent(direction, up_hint)

    hw = width * 0.5
    hd = depth * 0.5

    # rectangle profile in local XY plane at z=0
    profile = [
        Vector((-hw, -hd, 0)),
        Vector((+hw, -hd, 0)),
        Vector((+hw, +hd, 0)),
        Vector((-hw, +hd, 0)),
    ]

    mesh = bpy.data.meshes.new(name + "_M")
    obj = bpy.data.objects.new(name, mesh)

    # link object
    if collection is None:
        bpy.context.collection.objects.link(obj)
    else:
        collection.objects.link(obj)

    bm = bmesh.new()

    verts = [bm.verts.new(rot @ v + start) for v in profile]
    face = bm.faces.new(verts)

    res = bmesh.ops.extrude_face_region(bm, geom=[face])
    extruded_verts = [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]

    bmesh.ops.translate(bm, verts=extruded_verts, vec=direction.normalized() * length)

    bm.normal_update()
    bm.to_mesh(mesh)
    bm.free()

    return obj
