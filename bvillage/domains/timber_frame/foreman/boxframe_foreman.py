"""
Timber-frame foreman (BOX_FRAME pipeline)
"""

from __future__ import annotations

from bvillage.core.notes import set_domain_artifact
from bvillage.domains.timber_frame.core.derive_frameplan_boxframe import (
    derive_frameplan_boxframe,
)


class BoxFrameForeman:

    pipeline_mode = "STRUCTURE_FIRST"

    def dispatch(self, *, ctx, resolved_policy, provider):

        # -----------------------------------------
        # TYPE LAYER
        # -----------------------------------------

        structure, interior = provider.plan_structure_and_interior(
            ctx,
            resolved_policy=resolved_policy,
        )

        # -----------------------------------------
        # DOMAIN LAYER
        # -----------------------------------------

        frameplan = derive_frameplan_boxframe(ctx, structure)

        set_domain_artifact(
            structure.notes,
            domain="fachwerk",
            artifact="frameplan",
            payload=frameplan,
        )

        # -----------------------------------------
        # OPENINGS
        # -----------------------------------------

        openings = provider.plan_openings_for_type(
            ctx,
            structure=structure,
            interior=interior,
            frameplan=frameplan,
        )

        # -----------------------------------------
        # TYPE VALIDATION
        # -----------------------------------------

        provider.validate_for_type(
            ctx,
            structure=structure,
            frameplan=frameplan,
        )

        return structure, interior, openings
