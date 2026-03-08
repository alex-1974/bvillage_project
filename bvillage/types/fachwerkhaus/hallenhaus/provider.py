# bvillage/types/fachwerkhaus/hallenhaus/provider.py
from __future__ import annotations

from typing import Any, Tuple

from bvillage.core.errors import SchemaError
from bvillage.core.model import InteriorPlan, OpeningsPlan, StructurePlan

from bvillage.types.fachwerkhaus.hallenhaus.plan_topology import plan_topology
from bvillage.types.fachwerkhaus.hallenhaus.planner import plan_interior
from bvillage.types.fachwerkhaus.hallenhaus.openings import plan_openings
from bvillage.types.fachwerkhaus.hallenhaus.contracts.validate_frameplan_type import (
    validate_frameplan_langhaus_type,
)

__all__ = [
    "plan_structure_and_interior",
    "plan_openings_for_type",
    "validate_for_type",
]


def plan_structure_and_interior(
    ctx: Any,
    *,
    resolved_policy: Any,
) -> Tuple[StructurePlan, InteriorPlan]:
    """
    Type-layer planning only.

    Responsibilities
    ----------------
    - topology planning
    - interior planning

    Non-responsibilities
    --------------------
    - no frame production
    - no domain dispatch
    - no renderer logic
    """
    if getattr(ctx, "grammar", None) != "hall":
        raise SchemaError(
            f"Hallenhaus requires grammar='hall', got '{getattr(ctx, 'grammar', None)}'."
        )

    structure = plan_topology(ctx, resolved_policy)
    interior = plan_interior(ctx, structure)
    return structure, interior


def plan_openings_for_type(
    ctx: Any,
    *,
    structure: StructurePlan,
    interior: InteriorPlan,
    frameplan: dict[str, Any],
) -> OpeningsPlan:
    """
    Type-layer opening planning.
    """
    return plan_openings(
        ctx,
        structure=structure,
        interior=interior,
        frameplan=frameplan,
    )


def validate_for_type(
    ctx: Any,
    *,
    structure: StructurePlan,
    frameplan: dict[str, Any],
) -> None:
    """
    Type-specific validation hook called by the Foreman.

    WHY:
    Core must not import Hallenhaus-specific validation directly.
    """
    _ = ctx
    _ = structure
    validate_frameplan_langhaus_type(frameplan)
