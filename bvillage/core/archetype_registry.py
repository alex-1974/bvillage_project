# bvillage/core/archetype_registry.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

__all__ = [
    "ArchetypeBinding",
    "register",
    "get",
    "list_bindings",
]


@dataclass(frozen=True, slots=True)
class ArchetypeBinding:
    """
    Binding from a stable archetype id to the plugin ids that implement it.

    Example
    -------
    archetype: "fachwerkhaus.hallenhaus"
    type_provider: "fachwerkhaus.hallenhaus"
    domain: "fachwerk"
    """

    archetype: str
    type_provider: str
    domain: str


_registry: Dict[str, ArchetypeBinding] = {}


def register(archetype: str, *, type_provider: str, domain: str) -> None:
    if not isinstance(archetype, str) or not archetype.strip():
        raise RuntimeError("Archetype binding requires non-empty archetype")
    if not isinstance(type_provider, str) or not type_provider.strip():
        raise RuntimeError("Archetype binding requires non-empty type_provider")
    if not isinstance(domain, str) or not domain.strip():
        raise RuntimeError("Archetype binding requires non-empty domain")

    if archetype in _registry:
        raise RuntimeError(f"Archetype already registered: {archetype}")

    _registry[archetype] = ArchetypeBinding(
        archetype=archetype,
        type_provider=type_provider,
        domain=domain,
    )


def get(archetype: str) -> ArchetypeBinding:
    try:
        return _registry[archetype]
    except KeyError as exc:
        raise RuntimeError(f"Unknown archetype: {archetype}") from exc


def list_bindings() -> tuple[str, ...]:
    return tuple(sorted(_registry.keys()))
