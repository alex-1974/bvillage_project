# bvillage/domains/timber_frame/blender/braces.py
from __future__ import annotations

import logging
from typing import Any, Iterable

import bpy
from mathutils import Vector

from bvillage.core.errors import SchemaError
from bvillage.core.ontology.structural_terms import BRACE_DIAGONAL

from .materials_assign import assign_member_material
from .timber import make_beam_rect

__all__ = ["build_braces_corner_band"]

LOG = logging.getLogger(__name__)


def _require_basis(fp: dict[str, Any]) -> dict[str, float]:
    """
    Require canonical members-first FramePlan basis.

    Expected keys
    -------------
    - z0
    - z_plate

    Optional keys
    -------------
    - x_min
    - x_max
    - center_x
    - halfW
    """
    basis = fp.get("basis")
    if not isinstance(basis, dict):
        raise SchemaError("Braces: missing canonical frameplan basis")

    out: dict[str, float] = {}

    for key in ("z0", "z_plate"):
        if key not in basis:
            raise SchemaError(f"Braces: basis missing required key '{key}'")
        try:
            out[key] = float(basis[key])
        except Exception as exc:
            raise SchemaError(f"Braces: invalid basis value for '{key}'") from exc

    for key in ("x_min", "x_max", "center_x", "halfW"):
        if key in basis:
            try:
                out[key] = float(basis[key])
            except Exception as exc:
                raise SchemaError(f"Braces: invalid basis value for '{key}'") from exc

    return out


def _iter_braces(fp: dict[str, Any]) -> Iterable[dict[str, Any]]:
    """
    Members-first only.
    """
    members = fp.get("members")
    if not isinstance(members, dict):
        raise SchemaError("Braces: frameplan missing members dict")

    arr = members.get("braces")
    if arr is None:
        return ()

    if not isinstance(arr, list):
        raise SchemaError("Braces: members.braces must be a list")

    return (x for x in arr if isinstance(x, dict))


def _resolve_brace_profile(*, brace: dict[str, Any]) -> tuple[float, float]:
    prof = brace.get("profile")
    if isinstance(prof, dict):
        try:
            w = float(prof.get("w"))
            d = float(prof.get("d"))
            if w > 0.0 and d > 0.0:
                return w, d
        except Exception:
            pass

    return 0.08, 0.08


def _vec3(value: Any, *, ctx: str) -> Vector:
    if not isinstance(value, (list, tuple)) or len(value) != 3:
        raise SchemaError(f"{ctx}: expected vec3")
    try:
        return Vector((float(value[0]), float(value[1]), float(value[2])))
    except Exception as exc:
        raise SchemaError(f"{ctx}: invalid vec3 values") from exc


def build_braces_corner_band(
    *,
    fp: dict[str, Any],
    collection: bpy.types.Collection,
    ctx_view: Any = None,
    debug: bool = False,
) -> int:
    """
    Build braces strictly from FramePlan.members.braces.

    Contract
    --------
    - only tid == BRACE_DIAGONAL is handled here
    - p0/p1 must already be present in world coordinates
    - no house dependency
    - no wall/u/z reconstruction
    """
    _ = debug
    _require_basis(fp)

    built = 0
    for i, brace in enumerate(_iter_braces(fp)):
        if brace.get("tid") != BRACE_DIAGONAL:
            continue

        p0 = _vec3(brace.get("p0"), ctx=f"Braces: brace[{i}].p0")
        p1 = _vec3(brace.get("p1"), ctx=f"Braces: brace[{i}].p1")

        w, d = _resolve_brace_profile(brace=brace)

        name = brace.get("id") if isinstance(brace.get("id"), str) and brace.get("id") else f"Brace_{i:04d}"
        make_beam_rect(name, p0, p1, width=w, depth=d, collection=collection)

        if ctx_view is not None:
            obj = collection.objects.get(name)
            try:
                assign_member_material(
                    obj=obj,
                    member=brace,
                    ctx_view=ctx_view,
                    default_material_id="timber.spruce",
                    name_hint=f"BV_{name}",
                )
            except Exception:
                LOG.exception("Braces: material assignment failed for %s member=%s", name, brace)

        built += 1

    return built
