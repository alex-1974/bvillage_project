# bvillage/core/foreman/plan_dispatch.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from bvillage.core.provider_contract import TypeProvider
from bvillage.core.schema_archetype_id import validate_archetype_id

__all__ = [
    "ArchetypeBinding",
    "register_provider_with_archetypes",
    "resolve_provider_for_archetype",
    "list_registered_archetypes",
]


@dataclass(frozen=True, slots=True)
class ArchetypeBinding:
    archetype_id: str
    provider: TypeProvider
    construction_grammar: str


_REGISTRY: Dict[str, ArchetypeBinding] = {}


def register_provider_with_archetypes(
    provider: TypeProvider,
    construction_grammars: dict[str, str],
) -> None:
    if not isinstance(provider, TypeProvider):
        raise RuntimeError(
            f"Provider {provider!r} does not satisfy TypeProvider contract"
        )

    for archetype_id, grammar in construction_grammars.items():
        if not isinstance(archetype_id, str) or not archetype_id.strip():
            raise RuntimeError("Invalid archetype_id during registration")

        archetype_id = archetype_id.strip()

        validate_archetype_id(archetype_id)

        if archetype_id in _REGISTRY:
            existing = _REGISTRY[archetype_id]
            raise RuntimeError(
                "Duplicate archetype registration:\n"
                f"  archetype_id: {archetype_id}\n"
                f"  existing provider: {existing.provider.__class__.__name__}\n"
                f"  new provider: {provider.__class__.__name__}"
            )

        _REGISTRY[archetype_id] = ArchetypeBinding(
            archetype_id=archetype_id,
            provider=provider,
            construction_grammar=str(grammar),
        )


def resolve_provider_for_archetype(archetype_id: str) -> ArchetypeBinding:
    if not isinstance(archetype_id, str) or not archetype_id.strip():
        raise RuntimeError("Invalid archetype_id")

    try:
        return _REGISTRY[archetype_id]
    except KeyError:
        raise RuntimeError(
            f"Unknown archetype_id: {archetype_id}\n"
            f"Registered archetypes: {sorted(_REGISTRY.keys())}"
        )


def list_registered_archetypes() -> tuple[str, ...]:
    return tuple(sorted(_REGISTRY.keys()))
