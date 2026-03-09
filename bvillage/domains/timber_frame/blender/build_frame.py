# bvillage/domains/fachwerk/blender/build_frame.py

from __future__ import annotations

import hashlib
import inspect
import logging
from typing import Any, Optional, Tuple

import bpy
from mathutils import Vector

from bvillage.core.errors import SchemaError
from bvillage.core.notes import get_domain_artifact

LOG = logging.getLogger(__name__)

__all__ = [
    "build_fachwerk_frame",
    "build_fachwerk_frame_from_structure_notes",
]


# -----------------------------------------------------------------------------
# Compatibility helper (stable against signature drift)
# -----------------------------------------------------------------------------

def _call_compat(func: Any, /, **kwargs: Any) -> Any:
    sig = inspect.signature(func)
    for p in sig.parameters.values():
        if p.kind == inspect.Parameter.VAR_KEYWORD:
            return func(**kwargs)
    allowed = set(sig.parameters.keys())
    filtered = {k: v for k, v in kwargs.items() if k in allowed}
    return func(**filtered)


# -----------------------------------------------------------------------------
# Collections
# -----------------------------------------------------------------------------

def _ensure_subcollections(root: bpy.types.Collection) -> dict[str, bpy.types.Collection]:
    """
    Create / get a minimal BVILLAGE fachwerk subtree:

        root
          └ fachwerk
              └ frame
    """
    def _get_or_create(parent: bpy.types.Collection, name: str) -> bpy.types.Collection:
        for c in parent.children:
            if c.name == name:
                return c
        col = bpy.data.collections.new(name=name)
        parent.children.link(col)
        return col

    col_fachwerk = _get_or_create(root, "fachwerk")
    col_frame = _get_or_create(col_fachwerk, "frame")

    return {"fachwerk": col_fachwerk, "frame": col_frame}


def _clear_collection_recursive(col: bpy.types.Collection) -> int:
    removed = 0
    # remove objects
    for obj in list(col.objects):
        col.objects.unlink(obj)
        bpy.data.objects.remove(obj, do_unlink=True)
        removed += 1
    # recurse into children
    for child in list(col.children):
        removed += _clear_collection_recursive(child)
        col.children.unlink(child)
        bpy.data.collections.remove(child)
    return removed


def _clear_fachwerk_subtree(root: bpy.types.Collection) -> int:
    for c in list(root.children):
        if c.name == "fachwerk":
            return _clear_collection_recursive(c)
    return 0


# -----------------------------------------------------------------------------
# Materials (best-effort)
# -----------------------------------------------------------------------------

def _material_ctx_view(ctx: Any, *, house_name: str) -> dict[str, Any]:
    seed_any = getattr(ctx, "seed", None)
    if seed_any is None:
        seed_any = int.from_bytes(
            hashlib.blake2b(str(house_name).encode("utf-8"), digest_size=8).digest(),
            "big",
            signed=False,
        ) & 0x7FFFFFFF

    seed_val = getattr(seed_any, "base", seed_any)
    try:
        seed_int = int(seed_val)
    except Exception:
        seed_int = 0

    return {"seed": seed_int, "house_name": house_name}


def _assign_member_material(obj: bpy.types.Object, member: dict[str, Any], ctx_view: Any) -> None:
    """
    Best-effort material assignment. If your registry/policy is not ready yet,
    this should not block geometry output.
    """
    try:
        from .materials_assign import assign_member_material
        _call_compat(
            assign_member_material,
            obj=obj,
            member=member,
            ctx_view=ctx_view,
            default_material_id="",
            name_hint=str(member.get("id") or ""),
        )
    except Exception as exc:
        LOG.debug("material assign skipped: %s", exc)


# -----------------------------------------------------------------------------
# Geometry
# -----------------------------------------------------------------------------

def _vec3(v: Any, ctx: str) -> Vector:
    if not isinstance(v, (list, tuple)) or len(v) != 3:
        raise SchemaError(f"{ctx}: expected vec3")
    try:
        return Vector((float(v[0]), float(v[1]), float(v[2])))
    except Exception as exc:
        raise SchemaError(f"{ctx}: invalid vec3 values") from exc


def _add_member_edge(
    col: bpy.types.Collection,
    *,
    name: str,
    p0: Vector,
    p1: Vector,
) -> bpy.types.Object:
    """
    v0.4.0 rohskelett geometry: represent each timber as an edge (2-vertex mesh).
    Later, profiles will drive real beams.
    """
    mesh = bpy.data.meshes.new(name=name + "_mesh")
    obj = bpy.data.objects.new(name, mesh)
    col.objects.link(obj)

    mesh.from_pydata([p0, p1], [(0, 1)], [])
    mesh.update()
    return obj


def _iter_members(frameplan: dict[str, Any]) -> Tuple[str, dict[str, Any]]:
    members = frameplan["members"]
    for group in ("posts", "rails", "braces", "infills"):
        for m in members.get(group, []) or []:
            yield group, m


# -----------------------------------------------------------------------------
# Public API
# -----------------------------------------------------------------------------

def build_frame(
    *,
    ctx: Any,
    structure: Any,
    frameplan: dict[str, Any],
    root_collection: bpy.types.Collection,
    clear_previous: bool = True,
) -> bpy.types.Collection:
    """
    Render the canonical Langhaus FramePlan into Blender.

    HARD RULE:
      - Builder consumes the Architect's FramePlan as the only truth.
      - No legacy normalization, no inference from StructurePlan.grid/house_params.
      - Canonical full validation happens before the builder. The builder keeps
        only boundary guards required for safe rendering.
    """
    if clear_previous:
        removed = _clear_fachwerk_subtree(root_collection)
        LOG.info("clear_previous=True -> cleared fachwerk subtree, removed_objects=%d", removed)

    cols = _ensure_subcollections(root_collection)
    col_frame = cols["frame"]

    ctx_view = _material_ctx_view(ctx, house_name=getattr(structure, "name", "Structure"))

    built = 0
    for group, m in _iter_members(frameplan):
        mid = str(m.get("id") or f"{group}_{built}")
        tid = str(m.get("tid") or "unknown")
        name = f"{group.upper()}_{mid}_{tid}"

        p0 = _vec3(m.get("p0"), f"member[{mid}].p0")
        p1 = _vec3(m.get("p1"), f"member[{mid}].p1")

        obj = _add_member_edge(col_frame, name=name, p0=p0, p1=p1)
        _assign_member_material(obj, m, ctx_view)
        built += 1

    LOG.info("BUILD OK | rohskelett members=%d", built)
    return cols["fachwerk"]


def build_fachwerk_frame(
    *,
    ctx: Any,
    structure: Any,
    frameplan: dict[str, Any],
    root_collection: bpy.types.Collection,
    clear_previous: bool = True,
) -> bpy.types.Collection:
    return build_frame(
        ctx=ctx,
        structure=structure,
        frameplan=frameplan,
        root_collection=root_collection,
        clear_previous=clear_previous,
    )


def build_fachwerk_frame_from_structure_notes(
    *,
    ctx: Any,
    structure: Any,
    root_collection: bpy.types.Collection,
    clear_previous: bool = True,
) -> bpy.types.Collection:
    notes = getattr(structure, "notes", None)
    if not isinstance(notes, dict):
        raise SchemaError("StructurePlan.notes missing/invalid; cannot read fachwerk.frameplan")

    fp = get_domain_artifact(
        notes,
        domain="fachwerk",
        artifact="frameplan",
        legacy_aliases=("frameplan", "fachwerk.frameplan"),
    )
    if fp is None:
        raise SchemaError("Missing required artifact: fachwerk.frameplan")

    if not isinstance(fp, dict):
        raise SchemaError("fachwerk.frameplan must be a dict")

    return build_fachwerk_frame(
        ctx=ctx,
        structure=structure,
        frameplan=fp,
        root_collection=root_collection,
        clear_previous=clear_previous,
    )
