# bvillage/core/quality/physical_plausibility_validator.py
from __future__ import annotations

from typing import Any, Dict, List

__all__ = ["validate_physical_plausibility"]


def validate_physical_plausibility(frameplan: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Physical plausibility validator.

    Contract
    --------
    This validator must NEVER mutate the frameplan.

    Input
    -----
    members-first FramePlan

    Output
    ------
    list of issue dicts
    """

    issues: List[Dict[str, Any]] = []

    members = frameplan.get("members", {})

    posts = members.get("posts", [])
    rails = members.get("rails", [])
    braces = members.get("braces", [])

    _check_member_lengths(posts, "post", issues)
    _check_member_lengths(rails, "rail", issues)
    _check_member_lengths(braces, "brace", issues)

    _check_member_ids(posts, issues)
    _check_member_ids(rails, issues)
    _check_member_ids(braces, issues)

    return issues


# ---------------------------------------------------------
# checks
# ---------------------------------------------------------


def _check_member_lengths(
    members: List[Dict[str, Any]],
    kind: str,
    issues: List[Dict[str, Any]],
) -> None:

    for m in members:

        p0 = m.get("p0")
        p1 = m.get("p1")

        if p0 is None or p1 is None:
            issues.append(
                {
                    "severity": "ERROR",
                    "code": "PPV_MISSING_ENDPOINT",
                    "member": m.get("id"),
                    "message": f"{kind} missing endpoints",
                }
            )
            continue

        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        dz = p1[2] - p0[2]

        length2 = dx * dx + dy * dy + dz * dz

        if length2 <= 0.000001:

            issues.append(
                {
                    "severity": "ERROR",
                    "code": "PPV_ZERO_LENGTH_MEMBER",
                    "member": m.get("id"),
                    "message": f"{kind} has zero length",
                }
            )


def _check_member_ids(
    members: List[Dict[str, Any]],
    issues: List[Dict[str, Any]],
) -> None:

    seen = set()

    for m in members:

        mid = m.get("id")

        if mid is None:
            issues.append(
                {
                    "severity": "ERROR",
                    "code": "PPV_MEMBER_ID_MISSING",
                    "message": "member without id",
                }
            )
            continue

        if mid in seen:
            issues.append(
                {
                    "severity": "ERROR",
                    "code": "PPV_MEMBER_ID_DUPLICATE",
                    "member": mid,
                    "message": "duplicate member id",
                }
            )

        seen.add(mid)
