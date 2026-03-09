# bvillage/domains/timber_frame/blender/roof.py
from __future__ import annotations

from typing import Any

from mathutils import Vector

from bvillage.core.errors import SchemaError
from .timber import make_beam_rect

__all__ = ["build_roof_from_plan"]


def _member_profile(member: dict[str, Any], *, default_width: float, default_depth: float) -> tuple[float, float]:
    profile = member.get("profile")
    if isinstance(profile, dict):
        try:
            return float(profile["width"]), float(profile["depth"])
        except Exception:
            pass
    return default_width, default_depth


def _iter_roof_members(roofplan: dict[str, Any]):
    members = roofplan.get("members")
    if not isinstance(members, dict):
        raise SchemaError("RoofPlan missing 'members' dict")

    for group in ("ridge", "rafters", "collar_ties"):
        arr = members.get(group, [])
        if not isinstance(arr, list):
            raise SchemaError(f"RoofPlan.members.{group} must be a list")
        for m in arr:
            yield group, m


def build_roof_from_plan(
    *,
    roofplan: dict[str, Any],
    col_roof=None,
) -> None:
    """
    Render roof geometry strictly from RoofPlan.

    HARD RULE:
    - no derivation from axes_u / half_width / z_plate
    - Roof Producer already wrote the structural truth
    """
    for group, member in _iter_roof_members(roofplan):
        p0 = member.get("p0")
        p1 = member.get("p1")
        if p0 is None or p1 is None:
            raise SchemaError(f"Roof member in group {group!r} missing p0/p1")

        if not (isinstance(p0, (list, tuple)) and len(p0) == 3):
            raise SchemaError(f"Roof member in group {group!r} has invalid p0")
        if not (isinstance(p1, (list, tuple)) and len(p1) == 3):
            raise SchemaError(f"Roof member in group {group!r} has invalid p1")

        if group == "ridge":
            width, depth = _member_profile(member, default_width=0.18, default_depth=0.22)
        elif group == "rafters":
            width, depth = _member_profile(member, default_width=0.10, default_depth=0.16)
        elif group == "collar_ties":
            width, depth = _member_profile(member, default_width=0.12, default_depth=0.16)
        else:
            raise SchemaError(f"Unknown roof member group: {group}")

        name = str(member.get("id") or f"{group}_member")

        make_beam_rect(
            name,
            Vector((float(p0[0]), float(p0[1]), float(p0[2]))),
            Vector((float(p1[0]), float(p1[1]), float(p1[2]))),
            width=width,
            depth=depth,
            collection=col_roof,
        )
