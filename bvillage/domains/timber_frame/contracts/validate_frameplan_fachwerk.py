# bvillage/domains/fachwerk/contracts/validate_frameplan_fachwerk.py
from __future__ import annotations

from typing import Any, Iterable, Tuple

from bvillage.core.errors import SchemaError
from bvillage.domains.timber_frame.contracts.schema_frameplan_fachwerk import (
    FramePlanFachwerk,
    SCHEMA_VERSION_FACHWERK,
)
from bvillage.domains.timber_frame.contracts.schema_member_tids_fachwerk import (
    ALLOWED_BRACE_TIDS,
    ALLOWED_POST_TIDS,
    ALLOWED_RAIL_TIDS,
)

__all__ = [
    "validate_frameplan_fachwerk_schema",
    "validate_frameplan_fachwerk_domain",
]


def _require_keys(obj: dict[str, Any], keys: Iterable[str], ctx: str) -> None:
    for k in keys:
        if k not in obj:
            raise SchemaError(f"{ctx}: missing required key '{k}'")


def _require_vec3(v: Any, ctx: str) -> None:
    if not isinstance(v, (list, tuple)) or len(v) != 3:
        raise SchemaError(f"{ctx}: expected [x,y,z] vector")
    for c in v:
        if not isinstance(c, (int, float)):
            raise SchemaError(f"{ctx}: vector contains non-numeric value")


def _require_positive(v: Any, ctx: str) -> None:
    if not isinstance(v, (int, float)) or float(v) <= 0.0:
        raise SchemaError(f"{ctx}: expected positive float")


def _validate_member(member: dict[str, Any], allowed_tids: Tuple[str, ...], ctx: str) -> None:
    _require_keys(member, ("id", "tid", "p0", "p1"), ctx)

    tid = str(member["tid"])
    if tid not in allowed_tids:
        raise SchemaError(f"{ctx}: invalid tid '{tid}'")

    _require_vec3(member["p0"], f"{ctx}.p0")
    _require_vec3(member["p1"], f"{ctx}.p1")

    prof = member.get("profile")
    if prof is not None:
        _require_keys(prof, ("w", "d"), f"{ctx}.profile")
        _require_positive(prof["w"], f"{ctx}.profile.w")
        _require_positive(prof["d"], f"{ctx}.profile.d")


def validate_frameplan_fachwerk_schema(frameplan: FramePlanFachwerk) -> None:
    if not isinstance(frameplan, dict):
        raise SchemaError("FramePlan must be a dict")

    _require_keys(
        frameplan,
        ("schema_version", "coordinate_system", "basis", "frame_layout", "members"),
        "frameplan",
    )

    schema = int(frameplan["schema_version"])
    if schema != SCHEMA_VERSION_FACHWERK:
        raise SchemaError(
            f"Unsupported Fachwerk FramePlan schema_version={schema} "
            f"(expected {SCHEMA_VERSION_FACHWERK})"
        )

    cs = frameplan["coordinate_system"]
    _require_keys(cs, ("origin", "axes", "units"), "coordinate_system")

    if cs["origin"] != "building_center_ground":
        raise SchemaError("coordinate_system.origin must be 'building_center_ground'")

    axes = cs["axes"]
    _require_keys(axes, ("x", "y", "z"), "coordinate_system.axes")

    if axes["x"] != "longitudinal_forward":
        raise SchemaError("coordinate_system.axes.x invalid")
    if axes["y"] != "right_when_facing_positive_x":
        raise SchemaError("coordinate_system.axes.y invalid")
    if axes["z"] != "up":
        raise SchemaError("coordinate_system.axes.z invalid")

    if cs["units"] != "meters":
        raise SchemaError("coordinate_system.units must be 'meters'")

    basis = frameplan["basis"]
    _require_keys(basis, ("z0", "z_plate"), "basis")
    if not isinstance(basis["z0"], (int, float)):
        raise SchemaError("basis.z0 must be numeric")
    if not isinstance(basis["z_plate"], (int, float)):
        raise SchemaError("basis.z_plate must be numeric")
    if float(basis["z_plate"]) <= float(basis["z0"]):
        raise SchemaError("basis.z_plate must be above z0")

    frame_layout = frameplan["frame_layout"]
    _require_keys(frame_layout, ("x_frames", "y_rows", "frame_roles"), "frame_layout")

    members = frameplan["members"]
    _require_keys(members, ("posts", "rails", "braces", "infills"), "members")

    openings = frameplan.get("openings")
    if openings is not None and not isinstance(openings, list):
        raise SchemaError("openings must be list or None")


def validate_frameplan_fachwerk_domain(frameplan: FramePlanFachwerk) -> None:
    members = frameplan["members"]

    posts = members["posts"]
    rails = members["rails"]
    braces = members["braces"]

    if not isinstance(posts, list) or not posts:
        raise SchemaError("members.posts must be non-empty list")
    if not isinstance(rails, list) or not rails:
        raise SchemaError("members.rails must be non-empty list")
    if not isinstance(braces, list):
        raise SchemaError("members.braces must be list")

    for i, m in enumerate(posts):
        _validate_member(m, ALLOWED_POST_TIDS, f"members.posts[{i}]")
    for i, m in enumerate(rails):
        _validate_member(m, ALLOWED_RAIL_TIDS, f"members.rails[{i}]")
    for i, m in enumerate(braces):
        _validate_member(m, ALLOWED_BRACE_TIDS, f"members.braces[{i}]")
