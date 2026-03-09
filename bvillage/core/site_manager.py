"""
bvillage/core/site_manager.py

Core build coordinator.

Core responsibilities
---------------------
- plugin bootstrap
- policy resolution
- archetype dispatch
- foreman dispatch

Core must never contain construction grammar logic.
"""

from __future__ import annotations

from bvillage.core.policy_stack import resolve_policy_stack
from bvillage.core.foreman.plan_bootstrap import ensure_plugins_loaded
from bvillage.core.foreman.plan_dispatch import (
    resolve_provider_for_archetype,
    resolve_foreman_for_grammar,
)


__all__ = ["SiteManager"]


class SiteManager:

    def build(self, ctx):

        if not ctx.archetype_id:
            raise RuntimeError("Context.archetype_id missing")

        # load plugins
        ensure_plugins_loaded()

        # resolve policies
        resolved_policy = resolve_policy_stack(ctx)

        # resolve archetype → provider
        binding = resolve_provider_for_archetype(ctx.archetype_id)

        # resolve grammar → foreman
        foreman = resolve_foreman_for_grammar(binding.construction_grammar)

        # handoff to plugin pipeline
        return foreman.dispatch(
            ctx=ctx,
            resolved_policy=resolved_policy,
            provider=binding.provider,
        )
