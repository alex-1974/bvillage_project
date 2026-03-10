# bvillage/domains/timber_frame/blender/opening_frames.py

from __future__ import annotations

from typing import Any

from bvillage.core.errors import SchemaError


def build_opening_frames(frameplan: dict, *, blender_api: Any) -> None:
    """
    Render opening frames from members-first FramePlan.

    Renderer must not infer missing data.
    """

    openings = frameplan.get("openings")

    if openings is None:
        raise SchemaError("FramePlan missing 'openings' field")

    if not openings:
        return

    members = frameplan.get("members")

    if members is None:
        raise SchemaError("FramePlan missing 'members' section")

    posts = members.get("posts", [])
    rails = members.get("rails", [])

    for opening in openings:

        opening_id = opening.get("id")
        role = opening.get("role")

        if role not in ("gate", "door", "window"):
            raise SchemaError(f"Unknown opening role: {role}")

        p0 = opening.get("p0")
        p1 = opening.get("p1")

        if p0 is None or p1 is None:
            raise SchemaError(f"Opening {opening_id} missing geometry")

        blender_api.create_beam(
            start=p0,
            end=p1,
            role=role,
            metadata={"opening": opening_id},
        )
