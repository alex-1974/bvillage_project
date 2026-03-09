from __future__ import annotations

from bvillage.foreman.plan_dispatch import resolve_provider_for_archetype


def generate(ctx):

    binding = resolve_provider_for_archetype(ctx.archetype_id)

    provider = binding.provider

    structure, interior, openings = provider.generate(ctx)

    return structure, interior, openings
