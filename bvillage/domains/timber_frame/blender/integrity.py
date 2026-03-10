# bvillage/domains/timber_frame/blender/integrity.py

from __future__ import annotations

from typing import Any


REQUIRED_MEMBER_FIELDS = ("tid", "p0", "p1")


def _validate_member(member: dict[str, Any]) -> None:
    if not isinstance(member, dict):
        raise RuntimeError("FramePlan member must be dict")

    for field in REQUIRED_MEMBER_FIELDS:
        if field not in member:
            raise RuntimeError(f"FramePlan member missing '{field}'")

    p0 = member["p0"]
    p1 = member["p1"]

    if not (isinstance(p0, (list, tuple)) and len(p0) == 3):
        raise RuntimeError("member.p0 must be 3D coordinate")

    if not (isinstance(p1, (list, tuple)) and len(p1) == 3):
        raise RuntimeError("member.p1 must be 3D coordinate")


def validate_frameplan(fp: dict[str, Any]) -> None:
    if not isinstance(fp, dict):
        raise RuntimeError("FramePlan must be dict")

    if "basis" not in fp:
        raise RuntimeError("FramePlan missing 'basis'")

    if "members" not in fp:
        raise RuntimeError("FramePlan missing 'members'")

    members = fp["members"]

    if not isinstance(members, dict):
        raise RuntimeError("FramePlan.members must be dict")

    for group_name, group in members.items():
        if not isinstance(group, (list, tuple)):
            raise RuntimeError(
                f"FramePlan.members.{group_name} must be list"
            )

        for member in group:
            _validate_member(member)
