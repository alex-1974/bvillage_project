# bvillage/core/materials/role_registry.py

from __future__ import annotations

from typing import Dict, Mapping, Optional

__all__ = [
    "register_role_defaults",
    "get_role_default_material",
    "list_role_defaults",
    "clear_role_defaults",
]

_ROLE_DEFAULTS: Dict[str, str] = {}


def register_role_defaults(mapping: Mapping[str, str]) -> None:
    """
    Register role -> default material mappings.

    Notes
    -----
    This registry is core-level and domain-agnostic.
    Domain packages may register their own mappings at import time.
    """
    for role, material_id in mapping.items():
        if not isinstance(role, str) or not role.strip():
            raise RuntimeError("Role registry requires non-empty role")
        if not isinstance(material_id, str) or not material_id.strip():
            raise RuntimeError(f"Role registry requires non-empty material id for role {role!r}")

        role_key = role.strip()
        material_key = material_id.strip()

        existing = _ROLE_DEFAULTS.get(role_key)
        if existing is not None and existing != material_key:
            raise RuntimeError(
                f"Conflicting default material for role {role_key!r}: {existing!r} vs {material_key!r}"
            )

        _ROLE_DEFAULTS[role_key] = material_key


def get_role_default_material(role: str) -> Optional[str]:
    if not isinstance(role, str) or not role.strip():
        return None
    return _ROLE_DEFAULTS.get(role.strip())


def list_role_defaults() -> dict[str, str]:
    return dict(sorted(_ROLE_DEFAULTS.items()))


def clear_role_defaults() -> None:
    _ROLE_DEFAULTS.clear()
