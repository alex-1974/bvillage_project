# bvillage/core/policy_resolver.py

from __future__ import annotations

from bvillage.core.dispatch_registry import resolve_provider_for_archetype
from bvillage.core.model import Context

__all__ = ["resolve_policy"]


def resolve_policy(ctx: Context):
    binding = resolve_provider_for_archetype(ctx.archetype_id)
    provider = binding.provider

    resolver = getattr(provider, "resolve_policy", None)
    if not callable(resolver):
        raise RuntimeError(
            f"Provider {provider.__class__.__name__} does not implement resolve_policy(ctx)"
        )

    return resolver(ctx)
