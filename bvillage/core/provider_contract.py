# bvillage/core/provider_contract.py
from __future__ import annotations

from typing import Protocol, runtime_checkable

from bvillage.core.model import Context, InteriorPlan, OpeningsPlan, StructurePlan

__all__ = ["TypeProvider"]


@runtime_checkable
class TypeProvider(Protocol):
    """
    Contract for all type-family providers.

    Architecture
    ------------
    A provider belongs to one type-family plugin and is resolved indirectly
    via archetype_id dispatch. The Foreman knows only this contract, not any
    concrete architectural implementation.

    Responsibilities
    ----------------
    - produce StructurePlan
    - produce InteriorPlan
    - produce OpeningsPlan

    Non-responsibilities
    --------------------
    - no Blender emission
    - no direct renderer calls
    - no plugin-dispatch logic

    Return contract
    ---------------
    generate(ctx) -> (StructurePlan, InteriorPlan, OpeningsPlan)
    """

    def generate(
        self,
        ctx: Context,
    ) -> tuple[StructurePlan, InteriorPlan, OpeningsPlan]:
        ...
