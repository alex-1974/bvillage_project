from __future__ import annotations

from typing import Any

from bvillage.core.errors import SchemaError
from bvillage.core.model import InteriorPlan, OpeningsPlan, StructurePlan

from bvillage.types.timber_frame.longhouse.contracts.validate_frameplan_type import (
    validate_frameplan_langhaus_type,
)
from bvillage.types.timber_frame.longhouse.openings import plan_openings
from bvillage.types.timber_frame.longhouse.plan_topology import plan_topology
from bvillage.types.timber_frame.longhouse.planner import plan_interior

__all__ = ["LonghouseTypeProvider"]


class LonghouseTypeProvider:
    """
    Type-layer provider for timber-frame longhouse archetypes.

    Responsibilities
    ----------------
    - topology planning
    - interior planning
    - opening planning
    - type-specific validation

    Non-responsibilities
    --------------------
    - no frame production
    - no roof production
    - no renderer logic
    """

    def plan_structure_and_interior(
        self,
        ctx: Any,
        *,
        resolved_policy: Any,
    ) -> tuple[StructurePlan, InteriorPlan]:
        if getattr(ctx, "grammar", None) != "hall":
            raise SchemaError(
                f"Hallenhaus requires grammar='hall', got '{getattr(ctx, 'grammar', None)}'."
            )

        structure = plan_topology(ctx, resolved_policy)
        interior = plan_interior(ctx, structure)
        return structure, interior

    def plan_openings_for_type(
        self,
        ctx: Any,
        *,
        structure: StructurePlan,
        interior: InteriorPlan,
        frameplan: dict[str, Any],
    ) -> OpeningsPlan:
        return plan_openings(
            ctx,
            structure=structure,
            interior=interior,
            frameplan=frameplan,
        )

    def validate_for_type(
        self,
        ctx: Any,
        *,
        structure: StructurePlan,
        frameplan: dict[str, Any],
    ) -> None:
        _ = ctx
        _ = structure
        validate_frameplan_langhaus_type(frameplan)
