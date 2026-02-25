# bvillage/domains/fachwerk/blender/opening_frames.py

import logging
from typing import Dict, Any, Optional, Tuple

import bpy
from mathutils import Vector

from .timber import make_beam_rect
from .opening_profiles import OpeningProfilePolicy

LOG = logging.getLogger("bvillage.domains.fachwerk.blender.opening_frames")


def _house_basis(house: Dict[str, Any]) -> Tuple[float, float, float, float, float, float]:
    axis_x = house["axis_x"]
    axis_y = house["axis_y"]

    x_min = min(axis_x)
    x_max = max(axis_x)
    center_x = 0.5 * (x_min + x_max)

    y_min = min(axis_y)
    y_max = max(axis_y)
    halfW = 0.5 * (y_max - y_min)

    return x_min, x_max, center_x, y_min, y_max, halfW


def _map_post(member: Dict[str, Any], *, house: Dict[str, Any]) -> Tuple[Vector, Vector]:
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


def _map_rail(member: Dict[str, Any], *, house: Dict[str, Any]) -> Tuple[Vector, Vector]:
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


def build_opening_frames(
    *,
    fp: Dict[str, Any],
    house: Dict[str, Any],
    collection: Optional[bpy.types.Collection],
    policy: Optional[OpeningProfilePolicy] = None,
    debug: bool = False,
):
    """
    Build structural opening frames (no window meshes yet).

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

        # members-first iff we actually have structural members
        if isinstance(posts, list) and isinstance(rails, list) and (len(posts) + len(rails) > 0):
            x_min, x_max, center_x, _, _, halfW = _house_basis(house)

            LOG.info(
                "OpeningFrames: members-first | x=[%.3f..%.3f] center_x=%.3f halfW=%.3f posts=%d rails=%d",
                x_min, x_max, center_x, halfW, len(posts), len(rails)
            )

            # IMPORTANT: keep legacy naming so integrity checks keep working
            role_suffix = {
                "OPENING_JAMB_L": "JAMB_L",
                "OPENING_JAMB_R": "JAMB_R",
                "OPENING_LINTEL": "LINTEL",
                "OPENING_SILL": "SILL",
            }

            # Posts
            for m in posts:
                try:
                    p0, p1 = _map_post(m, house=house)
                except Exception:
                    LOG.exception("OpeningFrames: invalid post member: %s", m)
                    continue

                prof = m.get("profile") or {}
                w = float(prof.get("w", policy.jamb_post[0]))
                d = float(prof.get("d", policy.jamb_post[1]))

                opening = m.get("opening", "OPEN")
                suffix = role_suffix.get(m.get("role"), m.get("role", "PART"))
                nm = f"{opening}_{suffix}"

                make_beam_rect(nm, p0, p1, width=w, depth=d, collection=collection)

            # Rails
            for m in rails:
                try:
                    p0, p1 = _map_rail(m, house=house)
                except Exception:
                    LOG.exception("OpeningFrames: invalid rail member: %s", m)
                    continue

                prof = m.get("profile") or {}
                # default fallback, members usually provide profile anyway
                w = float(prof.get("w", policy.window_lintel[0]))
                d = float(prof.get("d", policy.window_lintel[1]))

                opening = m.get("opening", "OPEN")
                suffix = role_suffix.get(m.get("role"), m.get("role", "PART"))
                nm = f"{opening}_{suffix}"

                make_beam_rect(nm, p0, p1, width=w, depth=d, collection=collection)

            LOG.info("OpeningFrames: done | built_from=members")
            return

    # ==========================================================
    # LEGACY FALLBACK
    # ==========================================================
    axis_x = house["axis_x"]
    axis_y = house["axis_y"]

    x_min = min(axis_x)
    x_max = max(axis_x)
    center_x = 0.5 * (x_min + x_max)

    y_min = min(axis_y)
    y_max = max(axis_y)
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
            LOG.warning("Opening %s has unknown wall '%s'", o["name"], wall)
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

        make_beam_rect(f"{o['name']}_JAMB_L", pL0, pL1, width=w, depth=d, collection=collection)
        make_beam_rect(f"{o['name']}_JAMB_R", pR0, pR1, width=w, depth=d, collection=collection)

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

        make_beam_rect(f"{o['name']}_LINTEL", p0, p1, width=w_l, depth=d_l, collection=collection)

        # Brüstung (nur Fenster)
        if typ == "window":
            w_s, d_s = policy.window_sill

            if wall in ("N", "S"):
                p0 = Vector((x0, y, z0))
                p1 = Vector((x1, y, z0))
            else:
                p0 = Vector((x0, y0, z0))
                p1 = Vector((x1, y1, z0))

            make_beam_rect(f"{o['name']}_SILL", p0, p1, width=w_s, depth=d_s, collection=collection)

        built_total += 1

        LOG.info(
            "OpeningFrame built: %s (%s) | jamb=(%.2f,%.2f) lintel=(%.2f,%.2f)",
            o["name"], typ,
            policy.jamb_post[0], policy.jamb_post[1],
            w_l, d_l,
        )

    LOG.info("OpeningFrames: done | built=%d (legacy)", built_total)
