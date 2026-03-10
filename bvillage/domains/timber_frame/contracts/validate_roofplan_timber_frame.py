# bvillage/domains/timber_frame/contracts/validate_roofplan_timber_frame.py

from __future__ import annotations
from typing import Any

from bvillage.core.errors import SchemaError


def _require_keys(obj: dict, keys: tuple[str, ...], path: str):
    for k in keys:
        if k not in obj:
            raise SchemaError(f"{path}.{k} missing")


def _validate_member(member: dict, path: str):

    _require_keys(member, ("id", "tid", "p0", "p1", "profile"), path)

    if len(member["p0"]) != 3 or len(member["p1"]) != 3:
        raise SchemaError(f"{path} invalid coordinate length")

    profile = member["profile"]

    _require_keys(profile, ("width", "depth"), f"{path}.profile")


def validate_roofplan_timber_frame(roofplan: dict[str, Any]) -> None:

    if not isinstance(roofplan, dict):
        raise SchemaError("RoofPlan must be dict")

    _require_keys(
        roofplan,
        ("schema_version", "coordinate_system", "roof_type", "basis", "members"),
        "roofplan",
    )

    basis = roofplan["basis"]

    _require_keys(
        basis,
        (
            "x_frames",
            "half_width",
            "z_plate",
            "pitch_deg",
            "z_ridge",
            "z_kehl",
            "y_kehl",
            "kehl_frac",
        ),
        "roofplan.basis",
    )

    members = roofplan["members"]

    _require_keys(
        members,
        ("ridge", "rafters", "collar_ties"),
        "roofplan.members",
    )

    if not members["ridge"]:
        raise SchemaError("RoofPlan must contain ridge")

    for i, m in enumerate(members["ridge"]):
        _validate_member(m, f"members.ridge[{i}]")

    for i, m in enumerate(members["rafters"]):
        _validate_member(m, f"members.rafters[{i}]")

    for i, m in enumerate(members["collar_ties"]):
        _validate_member(m, f"members.collar_ties[{i}]")
