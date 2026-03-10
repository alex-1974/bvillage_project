# bvillage/core/dispatch_registry.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

__all__ = [
    "ArchetypeBinding",
    "register_provider_with_archetypes",
    "resolve_provider_for_archetype",
    "register_foreman_for_grammar",
    "resolve_foreman_for_grammar",
    "list_registered_archetypes",
    "list_registered_foremen",
]


@dataclass(frozen=True, slots=True)
class ArchetypeBinding:
    archetype_id: str
    provider: Any
    construction_grammar: str


_PROVIDER_REGISTRY: dict[str, ArchetypeBinding] = {}
_FOREMAN_REGISTRY: dict[str, Any] = {}


# ------------------------------------------------------------
# Provider registry
# ------------------------------------------------------------

def register_provider_with_archetypes(
    provider: Any,
    *,
    construction_grammars: dict[str, str],
) -> None:
    if not isinstance(construction_grammars, dict) or not construction_grammars:
        raise RuntimeError("Provider registration requires non-empty construction_grammars")

    for archetype_id, grammar in construction_grammars.items():
        if not isinstance(archetype_id, str) or not archetype_id.strip():
            raise RuntimeError("Invalid archetype_id during provider registration")
        if not isinstance(grammar, str) or not grammar.strip():
            raise RuntimeError(
                f"Invalid construction_grammar during provider registration for archetype {archetype_id!r}"
            )

        archetype_id = archetype_id.strip()
        grammar = grammar.strip()

        if archetype_id in _PROVIDER_REGISTRY:
            existing = _PROVIDER_REGISTRY[archetype_id]
            raise RuntimeError(
                "Duplicate archetype registration:\n"
                f"  archetype_id: {archetype_id}\n"
                f"  existing provider: {existing.provider.__class__.__name__}\n"
                f"  new provider: {provider.__class__.__name__}"
            )

        _PROVIDER_REGISTRY[archetype_id] = ArchetypeBinding(
            archetype_id=archetype_id,
            provider=provider,
            construction_grammar=grammar,
        )


def resolve_provider_for_archetype(archetype_id: str) -> ArchetypeBinding:
    if not isinstance(archetype_id, str) or not archetype_id.strip():
        raise RuntimeError("Invalid archetype_id")

    try:
        return _PROVIDER_REGISTRY[archetype_id]
    except KeyError:
        raise RuntimeError(
            f"Unknown archetype_id: {archetype_id}\n"
            f"Registered archetypes: {sorted(_PROVIDER_REGISTRY.keys())}"
        )


def list_registered_archetypes() -> tuple[str, ...]:
    return tuple(sorted(_PROVIDER_REGISTRY.keys()))


# ------------------------------------------------------------
# Foreman registry
# ------------------------------------------------------------

def register_foreman_for_grammar(
    construction_grammar: str,
    foreman: Any,
) -> None:
    if not isinstance(construction_grammar, str) or not construction_grammar.strip():
        raise RuntimeError("Invalid construction_grammar during foreman registration")

    grammar = construction_grammar.strip()

    if grammar in _FOREMAN_REGISTRY:
        existing = _FOREMAN_REGISTRY[grammar]
        raise RuntimeError(
            "Duplicate foreman registration:\n"
            f"  construction_grammar: {grammar}\n"
            f"  existing foreman: {existing.__class__.__name__}\n"
            f"  new foreman: {foreman.__class__.__name__}"
        )

    _FOREMAN_REGISTRY[grammar] = foreman


def resolve_foreman_for_grammar(construction_grammar: str) -> Any:
    if not isinstance(construction_grammar, str) or not construction_grammar.strip():
        raise RuntimeError("Invalid construction_grammar")

    grammar = construction_grammar.strip()

    try:
        return _FOREMAN_REGISTRY[grammar]
    except KeyError:
        raise RuntimeError(
            f"No foreman registered for grammar: {grammar}\n"
            f"Registered grammars: {sorted(_FOREMAN_REGISTRY.keys())}"
        )


def list_registered_foremen() -> tuple[str, ...]:
    return tuple(sorted(_FOREMAN_REGISTRY.keys()))
