# bvillage/domains/fachwerk/blender/opening_frames.py
from __future__ import annotations

import logging
from typing import Any

import bpy
from mathutils import Vector

from bvillage.core.errors import SchemaError
from bvillage.core.ontology.structural_terms import (
    POST_OPENING_JAMB,
    BEAM_OPENING_LINTEL,
    BEAM_WINDOW_SILL,
)

from .materials_assign import assign_member_material
from .opening_profiles import OpeningProfilePolicy
from .timber import make_beam_rect

__all__ = ["build_opening_frames"]

LOG = logging.getLogger(__name__)


def _assign_member_material_local(
    *,
    collection: bpy.types.Collection | None,
    obj_name: str,
    member: dict[str, Any],
    ctx_view: Any | None,
    default_material_id: str,
) -> None:
    if ctx_view is None or collection is None:
        return

    obj = collection.objects.get(obj_name)
    if obj is None:
        return

    mm = dict(member) if isinstance(member, dict) else {"role": "OPENING_FRAME"}
    if "id" not in mm or not mm["id"]:
        mm["id"] = obj_name

    try:
        assign_member_material(
            obj=obj,
            member=mm,
            ctx_view=ctx_view,
            default_material_id=default_material_id,
            name_hint=f"BV_{obj_name}",
        )
    except Exception:
        LOG.exception("OpeningFrames: material assignment failed for %s member=%s", obj_name, mm)


def _vec3(value: Any, *, ctx: str) -> Vector:
    if not isinstance(value, (list, tuple)) or len(value) != 3:
        raise SchemaError(f"{ctx}: expected vec3")
    try:
        return Vector((float(value[0]), float(value[1]), float(value[2])))
    except Exception as exc:
        raise SchemaError(f"{ctx}: invalid vec3 values") from exc


def _suffix_for_opening_member(member: dict[str, Any]) -> str:
    tid = member.get("tid")
    if tid == POST_OPENING_JAMB:
        side = member.get("side")
        return f"JAMB_{side}" if side in ("L", "R") else "JAMB"
    if tid == BEAM_OPENING_LINTEL:
        return "LINTEL"
    if tid == BEAM_WINDOW_SILL:
        return "SILL"
    return "MEMBER"


def build_opening_frames(
    *,
    fp: dict[str, Any],
    collection: bpy.types.Collection | None,
    policy: OpeningProfilePolicy | None = None,
    ctx_view: Any | None = None,
    debug: bool = False,
) -> None:
    """
    Build structural opening frames strictly from members-first FramePlan.

    Contract
    --------
    - posts with tid == POST_OPENING_JAMB are rendered here
    - rails with tid in {BEAM_OPENING_LINTEL, BEAM_WINDOW_SILL} are rendered here
    - p0/p1 must already be world-space coordinates
    - no house dependency
    - no legacy fallback to fp["openings"]
    """
    _ = debug

    if policy is None:
        policy = OpeningProfilePolicy()

    members = fp.get("members")
    if not isinstance(members, dict):
        raise SchemaError("opening_frames: frameplan missing members dict")

    posts = members.get("posts") or []
    rails = members.get("rails") or []

    if not isinstance(posts, list):
        raise SchemaError("opening_frames: members.posts must be a list")
    if not isinstance(rails, list):
        raise SchemaError("opening_frames: members.rails must be a list")

    # Posts: opening jambs only
    for i, member in enumerate(posts):
        tid = member.get("tid")
        if not isinstance(tid, str) or not tid:
            raise SchemaError("opening_frames: post member missing required string field 'tid'")
        if tid != POST_OPENING_JAMB:
            continue

        p0 = _vec3(member.get("p0"), ctx=f"opening_frames.posts[{i}].p0")
        p1 = _vec3(member.get("p1"), ctx=f"opening_frames.posts[{i}].p1")

        prof = member.get("profile") or {}
        w = float(prof.get("w", policy.jamb_post[0]))
        d = float(prof.get("d", policy.jamb_post[1]))

        opening = member.get("opening")
        suffix = _suffix_for_opening_member(member)
        if isinstance(opening, str) and opening:
            name = f"{opening}_{suffix}"
        else:
            mid = member.get("id") if isinstance(member.get("id"), str) and member.get("id") else f"opening_post_{i:04d}"
            name = f"{mid}_{suffix}"

        make_beam_rect(name, p0, p1, width=w, depth=d, collection=collection)
        _assign_member_material_local(
            collection=collection,
            obj_name=name,
            member=member,
            ctx_view=ctx_view,
            default_material_id="timber.oak",
        )

    # Rails: lintel / sill only
    for i, member in enumerate(rails):
        tid = member.get("tid")
        if not isinstance(tid, str) or not tid:
            raise SchemaError("opening_frames: rail member missing required string field 'tid'")
        if tid not in (BEAM_OPENING_LINTEL, BEAM_WINDOW_SILL):
            continue

        p0 = _vec3(member.get("p0"), ctx=f"opening_frames.rails[{i}].p0")
        p1 = _vec3(member.get("p1"), ctx=f"opening_frames.rails[{i}].p1")

        prof = member.get("profile") or {}
        if tid == BEAM_WINDOW_SILL:
            w = float(prof.get("w", policy.window_sill[0]))
            d = float(prof.get("d", policy.window_sill[1]))
        else:
            w = float(prof.get("w", policy.window_lintel[0]))
            d = float(prof.get("d", policy.window_lintel[1]))

        opening = member.get("opening")
        suffix = _suffix_for_opening_member(member)
        if isinstance(opening, str) and opening:
            name = f"{opening}_{suffix}"
        else:
            mid = member.get("id") if isinstance(member.get("id"), str) and member.get("id") else f"opening_rail_{i:04d}"
            name = f"{mid}_{suffix}"

        make_beam_rect(name, p0, p1, width=w, depth=d, collection=collection)
        _assign_member_material_local(
            collection=collection,
            obj_name=name,
            member=member,
            ctx_view=ctx_view,
            default_material_id="timber.oak",
        )

    LOG.info("OpeningFrames: done | built_from=members")
