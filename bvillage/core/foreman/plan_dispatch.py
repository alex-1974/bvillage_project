from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from bvillage.types.provider import TypeProvider


@dataclass(slots=True)
class ArchetypeBinding:

    archetype_id: str
    provider: TypeProvider
    construction_grammar: str


_REGISTRY: Dict[str, ArchetypeBinding] = {}


def register_provider_with_archetypes(
    provider: TypeProvider,
    construction_grammars: dict[str, str],
) -> None:

    for archetype_id, grammar in construction_grammars.items():

        if archetype_id in _REGISTRY:
            raise RuntimeError(f"Archetype already registered: {archetype_id}")

        _REGISTRY[archetype_id] = ArchetypeBinding(
            archetype_id=archetype_id,
            provider=provider,
            construction_grammar=grammar,
        )


def resolve_provider_for_archetype(archetype_id: str) -> ArchetypeBinding:

    try:
        return _REGISTRY[archetype_id]

    except KeyError:
        raise RuntimeError(f"Unknown archetype_id: {archetype_id}")
