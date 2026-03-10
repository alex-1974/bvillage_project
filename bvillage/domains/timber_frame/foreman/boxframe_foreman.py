# bvillage/domains/timber_frame/foreman/boxframe_foreman.py

from __future__ import annotations

from bvillage.core.notes import set_domain_artifact
from bvillage.domains.timber_frame.core.derive_frameplan_boxframe import (
    derive_frameplan_boxframe,
)
from bvillage.domains.timber_frame.core.derive_roofplan_boxframe import (
    derive_roofplan_boxframe,
)

__all__ = ["BoxFrameForeman"]


class BoxFrameForeman:
    pipeline_mode = "STRUCTURE_FIRST"

    def dispatch(
        self,
        *,
        ctx,
        resolved_policy,
        provider,
    ):
        structure, interior = provider.plan_structure_and_interior(
            ctx,
            resolved_policy=resolved_policy,
        )

        frameplan = derive_frameplan_boxframe(ctx, structure)

        set_domain_artifact(
            structure.notes,
            domain="fachwerk",
            artifact="frameplan",
            payload=frameplan,
        )

        roofplan = derive_roofplan_boxframe(
            frameplan,
            resolved_policy=resolved_policy,
        )

        set_domain_artifact(
            structure.notes,
            domain="fachwerk",
            artifact="roofplan",
            payload=roofplan,
        )

        openings = provider.plan_openings_for_type(
            ctx,
            structure=structure,
            interior=interior,
            frameplan=frameplan,
        )

        provider.validate_for_type(
            ctx,
            structure=structure,
            frameplan=frameplan,
        )

        return structure, interior, openings
