# bvillage/domains/fachwerk/__init__.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from bvillage.core.domain_registry import register as register_domain

from bvillage.domains.fachwerk.core.derive_frameplan_boxframe import (
    derive_frameplan_boxframe,
)
from bvillage.domains.fachwerk.contracts.validate_frameplan_fachwerk import (
    validate_frameplan_fachwerk_schema,
    validate_frameplan_fachwerk_domain,
)

__all__ = ["FachwerkDomainProvider"]


@dataclass(frozen=True, slots=True)
class FachwerkDomainProvider:
    """
    Domain provider for Fachwerk construction.

    Responsibilities
    ----------------
    - produce members-first FramePlan from StructurePlan
    - validate domain-level frameplan constraints
    """

    domain_id: str = "fachwerk"

    def frame_producer(self, ctx: Any, structure: Any):
        return derive_frameplan_boxframe(ctx, structure)

    def validate_frameplan(self, frameplan: dict[str, Any]) -> None:
        validate_frameplan_fachwerk_schema(frameplan)
        validate_frameplan_fachwerk_domain(frameplan)


_provider = FachwerkDomainProvider()
register_domain(_provider.domain_id, _provider)
