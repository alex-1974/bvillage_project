# bvillage/core/materials/policies/resolve.py

from typing import Any, Optional
from .fachwerk import ROLE_DEFAULT_MATERIAL


def default_material_id_for_member(
    member: Any,
    ctx: Any,
    *,
    fallback: Optional[str] = None,
) -> Optional[str]:
    """
    Resolve default material for a member based on domain policy.

    Priority:
      1) explicit fallback passed in
      2) role-based default (domain policy)
      3) None
    """

    if fallback:
        return fallback

    if isinstance(member, dict):
        role = member.get("role")
        if role:
            return ROLE_DEFAULT_MATERIAL.get(role)

    return None
