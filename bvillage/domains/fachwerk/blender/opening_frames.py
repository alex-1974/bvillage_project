# bvillage/domains/fachwerk/blender/opening_frames.py

import logging
from typing import Any

import bpy
from mathutils import Vector

from .timber import make_beam_rect
from .opening_profiles import OpeningProfilePolicy
from .materials_assign import assign_member_material
from bvillage.core.errors import SchemaError

__all__ = ['build_opening_frames']

LOG = logging.getLogger("bvillage.domains.fachwerk.blender.opening_frames")

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
        mm["id"] = obj_name  # deterministic, but explicit (no setdefault)

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
# Mapping
# ------------------------------------------------------------

def _house_basis(house: dict[str, Any]) -> tuple[float, float, float, float, float, float]:
    axes_u = house["axes_u"]
    axes_v = house["axes_v"]

    x_min = min(axes_u)
    x_max = max(axes_u)
    center_x = 0.5 * (x_min + x_max)

    y_min = min(axes_v)
    y_max = max(axes_v)
    halfW = 0.5 * (y_max - y_min)

    return x_min, x_max, center_x, y_min, y_max, halfW

def _map_post(member: dict[str, Any], *, house: dict[str, Any]) -> tuple[Vector, Vector]:
    x_min, x_max, center_x, _, _, halfW = _house_basis(house)
    wall = member["wall"]
    u = float(member["u"])
    z0 = float(member["z0"])
    z1 = float(member["z1"])

    if wall == "N":
        return Vector((center_x + u, -halfW, z0)), Vector((center_x + u, -halfW, z1))
    if wall == "S":
        return Vector((center_x + u, +halfW, z0)), Vector((center_x + u, +halfW, z1))
    if wall == "E":
        return Vector((x_max, u, z0)), Vector((x_max, u, z1))
    if wall == "W":
        return Vector((x_min, u, z0)), Vector((x_min, u, z1))
    raise ValueError(f"Unknown wall '{wall}'")

def _map_rail(member: dict[str, Any], *, house: dict[str, Any]) -> tuple[Vector, Vector]:
    x_min, x_max, center_x, _, _, halfW = _house_basis(house)
    wall = member["wall"]
    u0 = float(member["u0"])
    u1 = float(member["u1"])
    z = float(member["z"])

    if wall == "N":
        return Vector((center_x + u0, -halfW, z)), Vector((center_x + u1, -halfW, z))
    if wall == "S":
        return Vector((center_x + u0, +halfW, z)), Vector((center_x + u1, +halfW, z))
    if wall == "E":
        return Vector((x_max, u0, z)), Vector((x_max, u1, z))
    if wall == "W":
        return Vector((x_min, u0, z)), Vector((x_min, u1, z))
    raise ValueError(f"Unknown wall '{wall}'")

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
    Build structural opening frames (no window meshes yet).

    Members-first:
      - If fp["members"] contains posts/rails: build ONLY from members and return.

    Legacy fallback:
      - Build from fp["openings"] (old schema).

    Materials:
      - If ctx_view is provided, assign deterministic materials via MaterialRegistry
        (resolve_for_builder()) using role/defaults.
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
            x_min, x_max, center_x, _, _, halfW = _house_basis(house)

            LOG.info(
                "OpeningFrames: members-first | x=[%.3f..%.3f] center_x=%.3f halfW=%.3f posts=%d rails=%d",
                x_min, x_max, center_x, halfW, len(posts), len(rails)
            )

            role_suffix = {
                "OPENING_JAMB_L": "JAMB_L",
                "OPENING_JAMB_R": "JAMB_R",
                "OPENING_LINTEL": "LINTEL",
                "OPENING_SILL": "SILL",
            }

            # --------------------------
            # Posts (opening jambs only)
            # --------------------------
            for m in posts:
                role = m.get("role")
                if not isinstance(role, str) or not role:
                    raise SchemaError("opening_frames: member missing required string field 'role'")

                # Skip non-opening posts (e.g. PRIMARY_POST)
                if role not in ("OPENING_JAMB_L", "OPENING_JAMB_R"):
                    continue

                opening = m.get("opening")
                if not isinstance(opening, str) or not opening:
                    raise SchemaError("opening_frames: opening-post missing required string field 'opening'")

                try:
                    p0, p1 = _map_post(m, house=house)
                except Exception:
                    LOG.exception("OpeningFrames: invalid opening post member: %s", m)
                    continue

                prof = m.get("profile") or {}
                w = float(prof.get("w", policy.jamb_post[0]))
                d = float(prof.get("d", policy.jamb_post[1]))

                nm = f"{opening}_{role_suffix[role]}"

                make_beam_rect(nm, p0, p1, width=w, depth=d, collection=collection)
                _assign_member_material(
                    collection=collection,
                    obj_name=nm,
                    member=m,
                    ctx_view=ctx_view,
                    default_material_id="timber.oak",
                )

            # --------------------------
            # Rails (lintel/sill only)
            # --------------------------
            for m in rails:
                role = m.get("role")
                if not isinstance(role, str) or not role:
                    raise SchemaError("opening_frames: member missing required string field 'role'")

                # Skip non-opening rails
                if role not in ("OPENING_LINTEL", "OPENING_SILL"):
                    continue

                opening = m.get("opening")
                if not isinstance(opening, str) or not opening:
                    raise SchemaError("opening_frames: opening-rail missing required string field 'opening'")

                try:
                    p0, p1 = _map_rail(m, house=house)
                except Exception:
                    LOG.exception("OpeningFrames: invalid opening rail member: %s", m)
                    continue

                prof = m.get("profile") or {}
                w = float(prof.get("w", policy.window_lintel[0]))
                d = float(prof.get("d", policy.window_lintel[1]))

                nm = f"{opening}_{role_suffix[role]}"

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
    # LEGACY FALLBACK
    # ==========================================================
    axes_u = house["axes_u"]
    axes_v = house["axes_v"]

    x_min = min(axes_u)
    x_max = max(axes_u)
    center_x = 0.5 * (x_min + x_max)

    y_min = min(axes_v)
    y_max = max(axes_v)
    halfW = 0.5 * (y_max - y_min)

    openings = fp.get("openings") or []

    LOG.info(
        "OpeningFrames: legacy | x=[%.3f..%.3f] center_x=%.3f halfW=%.3f openings=%d",
        x_min, x_max, center_x, halfW, len(openings)
    )

    built_total = 0

    for o in openings:
        typ = o["type"]
        wall = o["wall"]

        u0 = float(o["u0"])
        u1 = float(o["u1"])
        z0 = float(o["z0"])
        z1 = float(o["z1"])

        # --- World Mapping ---
        if wall == "N":
            y = -halfW
            x0 = center_x + u0
            x1 = center_x + u1
        elif wall == "S":
            y = +halfW
            x0 = center_x + u0
            x1 = center_x + u1
        elif wall == "E":
            x0 = x1 = x_max
            y0 = u0
            y1 = u1
        elif wall == "W":
            x0 = x1 = x_min
            y0 = u0
            y1 = u1
        else:
            raise SchemaError(f"opening_frames: unknown wall '{wall}' for opening '{name}'")
            continue

        if debug:
            LOG.info(
                "Opening %s | wall=%s | u=[%.3f..%.3f] z=[%.3f..%.3f]",
                o["name"], wall, u0, u1, z0, z1
            )

        # Laibungsständer
        w, d = policy.jamb_post

        if wall in ("N", "S"):
            pL0 = Vector((x0, y, z0))
            pL1 = Vector((x0, y, z1))
            pR0 = Vector((x1, y, z0))
            pR1 = Vector((x1, y, z1))
        else:
            pL0 = Vector((x0, y0, z0))
            pL1 = Vector((x0, y0, z1))
            pR0 = Vector((x1, y1, z0))
            pR1 = Vector((x1, y1, z1))

        nmL = f"{o['name']}_JAMB_L"
        nmR = f"{o['name']}_JAMB_R"
        make_beam_rect(nmL, pL0, pL1, width=w, depth=d, collection=collection)
        make_beam_rect(nmR, pR0, pR1, width=w, depth=d, collection=collection)

        # synthetic member for legacy part
        name = o.get("name")
        if not isinstance(name, str) or not name:
            raise SchemaError("opening_frames: opening missing required string field 'name'")

        mem_base = {"role": "OPENING_FRAME", "opening": name, "wall": wall}
        
        _assign_member_material(collection=collection, obj_name=nmL, member={**mem_base, "id": nmL}, ctx_view=ctx_view, default_material_id="timber.oak")
        _assign_member_material(collection=collection, obj_name=nmR, member={**mem_base, "id": nmR}, ctx_view=ctx_view, default_material_id="timber.oak")

        # Sturz
        if typ == "gate":
            w_l, d_l = policy.gate_lintel
        else:
            w_l, d_l = policy.window_lintel

        if wall in ("N", "S"):
            p0 = Vector((x0, y, z1))
            p1 = Vector((x1, y, z1))
        else:
            p0 = Vector((x0, y0, z1))
            p1 = Vector((x1, y1, z1))

        nm = f"{o['name']}_LINTEL"
        make_beam_rect(nm, p0, p1, width=w_l, depth=d_l, collection=collection)
        _assign_member_material(collection=collection, obj_name=nm, member={**mem_base, "id": nm}, ctx_view=ctx_view, default_material_id="timber.oak")

        # Brüstung (nur Fenster)
        if typ == "window":
            w_s, d_s = policy.window_sill

            if wall in ("N", "S"):
                p0 = Vector((x0, y, z0))
                p1 = Vector((x1, y, z0))
            else:
                p0 = Vector((x0, y0, z0))
                p1 = Vector((x1, y1, z0))

            nm = f"{o['name']}_SILL"
            make_beam_rect(nm, p0, p1, width=w_s, depth=d_s, collection=collection)
            _assign_member_material(collection=collection, obj_name=nm, member={**mem_base, "id": nm}, ctx_view=ctx_view, default_material_id="timber.oak")

        built_total += 1

        LOG.info(
            "OpeningFrame built: %s (%s) | jamb=(%.2f,%.2f) lintel=(%.2f,%.2f)",
            o["name"], typ,
            policy.jamb_post[0], policy.jamb_post[1],
            w_l, d_l,
        )

    LOG.info("OpeningFrames: done | built=%d (legacy)", built_total)
