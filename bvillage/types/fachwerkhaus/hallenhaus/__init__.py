# bvillage/types/fachwerkhaus/hallenhaus/__init__.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from bvillage.core.registry import register_house_type
from bvillage.core.type_registry import register as register_type
from bvillage.core.archetype_registry import register as register_archetype

from .provider import (
    plan_structure_and_interior,
    plan_openings_for_type,
    validate_for_type,
)

__all__ = ["HallenhausProvider"]


@dataclass(frozen=True, slots=True)
class HallenhausProvider:
    """
    Type provider for Fachwerkhaus Hallenhaus.

    Structural frame generation is dispatched by the Foreman to the domain layer.
    """

    type_id: str = "fachwerkhaus.hallenhaus"

    def plan_structure_and_interior(self, ctx: Any, *, resolved_policy: Any):
        return plan_structure_and_interior(ctx, resolved_policy=resolved_policy)

    def plan_openings_for_type(
        self,
        ctx: Any,
        *,
        structure: Any,
        interior: Any,
        frameplan: dict[str, Any],
    ):
        return plan_openings_for_type(
            ctx,
            structure=structure,
            interior=interior,
            frameplan=frameplan,
        )

    def validate_for_type(
        self,
        ctx: Any,
        *,
        structure: Any,
        frameplan: dict[str, Any],
    ):
        return validate_for_type(
            ctx,
            structure=structure,
            frameplan=frameplan,
        )


_provider = HallenhausProvider()

# Legacy registry hook (kept for compatibility during stabilization)
register_house_type(_provider, origin=__name__)

# New plugin registries
register_type(_provider.type_id, _provider)
register_archetype(
    _provider.type_id,
    type_provider=_provider.type_id,
    domain="fachwerk",
)
