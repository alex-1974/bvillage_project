# bvillage/core/site_manager.py

from __future__ import annotations

from bvillage.core.dispatch_registry import (
    resolve_foreman_for_grammar,
    resolve_provider_for_archetype,
)
from bvillage.core.plugin_bootstrap import ensure_plugins_loaded
from bvillage.core.policy_resolver import resolve_policy
from bvillage.core.trace import get_trace

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

        trace = get_trace()

        with trace.stage(
            "ensure_plugins_loaded",
            archetype_id=ctx.archetype_id,
        ):
            ensure_plugins_loaded()

        with trace.stage(
            "resolve_policy",
            archetype_id=ctx.archetype_id,
        ):
            resolved_policy = resolve_policy(ctx)

        with trace.stage(
            "resolve_provider_for_archetype",
            archetype_id=ctx.archetype_id,
        ):
            binding = resolve_provider_for_archetype(ctx.archetype_id)

        with trace.stage(
            "resolve_foreman_for_grammar",
            construction_grammar=binding.construction_grammar,
        ):
            foreman = resolve_foreman_for_grammar(binding.construction_grammar)

        with trace.stage(
            "foreman.dispatch",
            provider_class=binding.provider.__class__.__name__,
            foreman_class=foreman.__class__.__name__,
            construction_grammar=binding.construction_grammar,
        ):
            return foreman.dispatch(
                ctx=ctx,
                resolved_policy=resolved_policy,
                provider=binding.provider,
            )
