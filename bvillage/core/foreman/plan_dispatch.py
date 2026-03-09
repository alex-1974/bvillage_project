"""
Dispatch registry

1. archetype_id → provider
2. construction_grammar → foreman
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True, slots=True)
class ArchetypeBinding:
    archetype_id: str
    provider: Any
    construction_grammar: str


_PROVIDER_REGISTRY: Dict[str, ArchetypeBinding] = {}
_FOREMAN_REGISTRY: Dict[str, Any] = {}


# ------------------------------------------------------------
# provider registration
# ------------------------------------------------------------

def register_provider_with_archetypes(provider, construction_grammars):

    for archetype_id, grammar in construction_grammars.items():

        if archetype_id in _PROVIDER_REGISTRY:
            raise RuntimeError(f"Duplicate archetype: {archetype_id}")

        _PROVIDER_REGISTRY[archetype_id] = ArchetypeBinding(
            archetype_id=archetype_id,
            provider=provider,
            construction_grammar=grammar,
        )


def resolve_provider_for_archetype(archetype_id):

    try:
        return _PROVIDER_REGISTRY[archetype_id]

    except KeyError:
        raise RuntimeError(
            f"Unknown archetype: {archetype_id}\n"
            f"Known: {sorted(_PROVIDER_REGISTRY)}"
        )


# ------------------------------------------------------------
# foreman registration
# ------------------------------------------------------------

def register_foreman_for_grammar(grammar, foreman):

    if grammar in _FOREMAN_REGISTRY:
        raise RuntimeError(f"Duplicate foreman for grammar {grammar}")

    _FOREMAN_REGISTRY[grammar] = foreman


def resolve_foreman_for_grammar(grammar):

    try:
        return _FOREMAN_REGISTRY[grammar]

    except KeyError:
        raise RuntimeError(
            f"No foreman registered for grammar {grammar}\n"
            f"Known grammars: {sorted(_FOREMAN_REGISTRY)}"
        )
