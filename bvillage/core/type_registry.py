# bvillage/core/type_registry.py
from __future__ import annotations

from typing import Any, Dict

__all__ = [
    "register",
    "get",
    "list_types",
]


_registry: Dict[str, Any] = {}


def register(name: str, provider: Any) -> None:
    """
    Register a type provider object.

    Required provider surface
    -------------------------
    - provider.type_id : str
    - provider.plan_structure_and_interior(ctx, *, resolved_policy)
    - provider.plan_openings_for_type(ctx, *, structure, interior, frameplan)

    Optional
    --------
    - provider.validate_for_type(ctx, *, structure, frameplan)
    """
    if not isinstance(name, str) or not name.strip():
        raise RuntimeError("Type registry requires non-empty name")

    if name in _registry:
        raise RuntimeError(f"Type already registered: {name}")

    _registry[name] = provider


def get(name: str) -> Any:
    try:
        return _registry[name]
    except KeyError as exc:
        raise RuntimeError(f"Unknown type provider: {name}") from exc


def list_types() -> tuple[str, ...]:
    return tuple(sorted(_registry.keys()))
