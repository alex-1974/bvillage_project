# bvillage/core/materials/policies/resolve.py

from __future__ import annotations

from typing import Any, Optional

from bvillage.core.materials.role_registry import get_role_default_material

__all__ = ["default_material_id_for_member"]


def default_material_id_for_member(
    member: Any,
    ctx: Any,
    *,
    fallback: Optional[str] = None,
) -> Optional[str]:
    """
    Resolve default material for a structural member.

    Priority
    --------
    1) explicit fallback
    2) role-based default registered by domain
    3) None
    """

    if fallback:
        return fallback

    if isinstance(member, dict):
        role = member.get("role")
        if role:
            return get_role_default_material(role)

    return None
