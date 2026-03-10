# bvillage/core/site_manager.py
from __future__ import annotations

from bvillage.core.dispatch_registry import (
    resolve_foreman_for_grammar,
    resolve_provider_for_archetype,
)
from bvillage.core.plugin_bootstrap import ensure_plugins_loaded
from bvillage.core.policy_resolver import resolve_policy

__all__ = ["SiteManager"]


class SiteManager:
    """
    Core-level coordinator.

    Responsibilities
    ----------------
    - plugin bootstrap
    - policy resolution
    - archetype dispatch
    - grammar dispatch

    Non-responsibilities
    --------------------
    - no construction logic
    - no topology generation
    - no frame generation
    - no roof generation
    - no renderer logic
    """

    def build(self, ctx):
        if not ctx.archetype_id:
            raise RuntimeError("Context.archetype_id missing")

        ensure_plugins_loaded()

        resolved_policy = resolve_policy(ctx)

        binding = resolve_provider_for_archetype(ctx.archetype_id)
        foreman = resolve_foreman_for_grammar(binding.construction_grammar)

        return foreman.dispatch(
            ctx=ctx,
            resolved_policy=resolved_policy,
            provider=binding.provider,
        )
