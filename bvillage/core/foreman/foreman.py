from __future__ import annotations

from bvillage.core.model import Context, StructurePlan, InteriorPlan, OpeningsPlan
from bvillage.core.provider_contract import TypeProvider
from bvillage.core.foreman.plan_dispatch import resolve_provider_for_archetype

def generate(
    ctx: Context,
) -> tuple[StructurePlan, InteriorPlan, OpeningsPlan]:

    if not ctx.archetype_id:
        raise RuntimeError("Context.archetype_id missing")

    # ------------------------------------------------------------
    # resolve archetype binding
    # ------------------------------------------------------------

    binding = resolve_provider_for_archetype(ctx.archetype_id)

    provider = binding.provider

    # ------------------------------------------------------------
    # contract check
    # ------------------------------------------------------------

    if not isinstance(provider, TypeProvider):
        raise RuntimeError(
            f"Provider {provider!r} does not implement TypeProvider contract"
        )

    # ------------------------------------------------------------
    # generate plans
    # ------------------------------------------------------------

    result = provider.generate(ctx)

    if not isinstance(result, tuple) or len(result) != 3:
        raise RuntimeError(
            f"{provider.__class__.__name__}.generate() must return "
            "(StructurePlan, InteriorPlan, OpeningsPlan)"
        )

    structure, interior, openings = result

    return structure, interior, openings
