# bvillage/core/domain_registry.py
from __future__ import annotations

from typing import Any, Dict

__all__ = [
    "register",
    "get",
    "list_domains",
]


_registry: Dict[str, Any] = {}


def register(name: str, provider: Any) -> None:
    """
    Register a domain provider object.

    Required provider surface
    -------------------------
    - provider.domain_id : str
    - provider.frame_producer(ctx, structure)

    Optional
    --------
    - provider.validate_frameplan(frameplan)
    """
    if not isinstance(name, str) or not name.strip():
        raise RuntimeError("Domain registry requires non-empty name")

    if name in _registry:
        raise RuntimeError(f"Domain already registered: {name}")

    _registry[name] = provider


def get(name: str) -> Any:
    try:
        return _registry[name]
    except KeyError as exc:
        raise RuntimeError(f"Unknown domain provider: {name}") from exc


def list_domains() -> tuple[str, ...]:
    return tuple(sorted(_registry.keys()))
