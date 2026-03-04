# bvillage/domains/fachwerk/blender/opening_frames.py

import logging
from typing import Any

import bpy
from mathutils import Vector

from .timber import make_beam_rect
from .opening_profiles import OpeningProfilePolicy
from .materials_assign import assign_member_material
from bvillage.core.errors import SchemaError

from bvillage.core.ontology.structural_terms import (
    POST_JAMB,
    BEAM_LINTEL,
    BEAM_WINDOW_SILL,
)

__all__ = ['build_opening_frames']

LOG = logging.getLogger(__name__)


# ------------------------------------------------------------
# Materials (local, minimal)
# ------------------------------------------------------------

def _assign_member_material(
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


# ------------------------------------------------------------
# Geometry mapping helpers
# ------------------------------------------------------------

def _house_basis(house: dict[str, Any]) -> tuple[float, float, float, float]:
    axes_u = house["axes_u"]
    x_min = float(min(axes_u))
    x_max = float(max(axes_u))
    center_x = 0.5 * (x_min + x_max)
    halfW = 0.5 * float(house["W"])
    return x_min, x_max, center_x, halfW


def _map_post(m: dict[str, Any], *, house: dict[str, Any]) -> tuple[Vector, Vector]:
    wall = str(m.get("wall"))
    u = float(m["u"])
    z0 = float(m["z0"])
    z1 = float(m["z1"])

    x_min, x_max, center_x, halfW = _house_basis(house)

    if wall == "N":
        x = center_x + u
        y = -halfW
    elif wall == "S":
        x = center_x + u
        y = halfW
    elif wall == "E":
        x = x_max
        y = u
    elif wall == "W":
        x = x_min
        y = u
    else:
        raise SchemaError(f"opening_frames: invalid wall '{wall}' for post mapping")

    return Vector((x, y, z0)), Vector((x, y, z1))


def _map_rail(m: dict[str, Any], *, house: dict[str, Any]) -> tuple[Vector, Vector]:
    wall = str(m.get("wall"))
    u0 = float(m["u0"])
    u1 = float(m["u1"])
    z = float(m["z"])

    x_min, x_max, center_x, halfW = _house_basis(house)

    if wall == "N":
        return Vector((center_x + u0, -halfW, z)), Vector((center_x + u1, -halfW, z))
    if wall == "S":
        return Vector((center_x + u0, halfW, z)), Vector((center_x + u1, halfW, z))
    if wall == "E":
        return Vector((x_max, u0, z)), Vector((x_max, u1, z))
    if wall == "W":
        return Vector((x_min, u0, z)), Vector((x_min, u1, z))
    raise SchemaError(f"opening_frames: invalid wall '{wall}' for rail mapping")


def _suffix_for_opening_member(m: dict[str, Any]) -> str:
    tid = m.get("tid")
    if tid == POST_JAMB:
        side = m.get("side")
        return f"JAMB_{side}" if side in ("L", "R") else "JAMB"
    if tid == BEAM_LINTEL:
        return "LINTEL"
    if tid == BEAM_WINDOW_SILL:
        return "SILL"
    return "MEMBER"


# ------------------------------------------------------------
# Builder
# ------------------------------------------------------------

def build_opening_frames(
    *,
    fp: dict[str, Any],
    house: dict[str, Any],
    collection: bpy.types.Collection | None,
    policy: OpeningProfilePolicy | None = None,
    ctx_view: Any | None = None,
    debug: bool = False,
):
    """
    Build structural opening frames (posts jambs + rails lintel/sill).

    Members-first:
      - If fp["members"] contains posts/rails: build ONLY from members and return.

    Legacy fallback:
      - Build from fp["openings"] (old schema).
    """
    if policy is None:
        policy = OpeningProfilePolicy()

    # ==========================================================
    # MEMBERS-FIRST
    # ==========================================================
    members = fp.get("members")
    if isinstance(members, dict):
        posts = members.get("posts") or []
        rails = members.get("rails") or []

        if isinstance(posts, list) and isinstance(rails, list) and (len(posts) + len(rails) > 0):
            # Posts: opening jambs only
            for m in posts:
                tid = m.get("tid")
                if not isinstance(tid, str) or not tid:
                    raise SchemaError("opening_frames: member missing required string field 'tid'")
                if tid != POST_JAMB:
                    continue

                side = m.get("side")
                if side not in ("L", "R"):
                    raise SchemaError("opening_frames: opening-jamb missing required field side in {'L','R'}")

                opening = m.get("opening")
                if not isinstance(opening, str) or not opening:
                    raise SchemaError("opening_frames: opening-jamb missing required string field 'opening'")

                p0, p1 = _map_post(m, house=house)

                prof = m.get("profile") or {}
                w = float(prof.get("w", policy.jamb_post[0]))
                d = float(prof.get("d", policy.jamb_post[1]))

                nm = f"{opening}_{_suffix_for_opening_member(m)}"
                make_beam_rect(nm, p0, p1, width=w, depth=d, collection=collection)
                _assign_member_material(
                    collection=collection,
                    obj_name=nm,
                    member=m,
                    ctx_view=ctx_view,
                    default_material_id="timber.oak",
                )

            # Rails: lintel/sill only
            for m in rails:
                tid = m.get("tid")
                if not isinstance(tid, str) or not tid:
                    raise SchemaError("opening_frames: member missing required string field 'tid'")
                if tid not in (BEAM_LINTEL, BEAM_WINDOW_SILL):
                    continue

                opening = m.get("opening")
                if not isinstance(opening, str) or not opening:
                    raise SchemaError("opening_frames: opening-rail missing required string field 'opening'")

                p0, p1 = _map_rail(m, house=house)

                prof = m.get("profile") or {}
                w = float(prof.get("w", policy.window_lintel[0]))
                d = float(prof.get("d", policy.window_lintel[1]))

                nm = f"{opening}_{_suffix_for_opening_member(m)}"
                make_beam_rect(nm, p0, p1, width=w, depth=d, collection=collection)
                _assign_member_material(
                    collection=collection,
                    obj_name=nm,
                    member=m,
                    ctx_view=ctx_view,
                    default_material_id="timber.oak",
                )

            LOG.info("OpeningFrames: done | built_from=members")
            return

    # ==========================================================
    # LEGACY FALLBACK (unchanged behavior)
    # ==========================================================
    openings = fp.get("openings") or []
    if not isinstance(openings, list) or len(openings) <= 0:
        LOG.info("OpeningFrames: no openings (legacy) -> nothing to build")
        return

    LOG.warning("OpeningFrames: LEGACY fallback path in use (no members.*).")

    # NOTE: keep your existing legacy implementation below if you still need it.
    # If you want, paste your legacy block here unchanged.
    return
