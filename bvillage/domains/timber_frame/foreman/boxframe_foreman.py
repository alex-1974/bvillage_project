# bvillage/domains/timber_frame/foreman/boxframe_foreman.py

from __future__ import annotations

from bvillage.core.notes import set_domain_artifact
from bvillage.core.trace import get_trace
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
        trace = get_trace()

        with trace.stage("plan_structure_and_interior") as ev:
            structure, interior = provider.plan_structure_and_interior(
                ctx,
                resolved_policy=resolved_policy,
            )
            if trace.enabled:
                trace.add_data(
                    ev,
                    structure_class=structure.__class__.__name__,
                    interior_class=interior.__class__.__name__,
                    wall_count=len(getattr(structure, "walls", ())),
                    frame_count=len(getattr(structure, "frames", ())),
                    room_count=len(getattr(interior, "rooms", ())),
                    zone_count=len(getattr(interior, "zones", ())),
                )

        with trace.stage("derive_frameplan_boxframe") as ev:
            frameplan = derive_frameplan_boxframe(ctx, structure)
            if trace.enabled:
                trace.add_data(
                    ev,
                    member_count=len(frameplan.get("members", ())),
                )

        with trace.stage("set_domain_artifact.frameplan"):
            set_domain_artifact(
                structure.notes,
                domain="fachwerk",
                artifact="frameplan",
                payload=frameplan,
            )

        with trace.stage("derive_roofplan_boxframe") as ev:
            roofplan = derive_roofplan_boxframe(
                frameplan,
                resolved_policy=resolved_policy,
            )
            if trace.enabled:
                trace.add_data(
                    ev,
                    roof_member_count=len(roofplan.get("members", ())),
                )

        with trace.stage("set_domain_artifact.roofplan"):
            set_domain_artifact(
                structure.notes,
                domain="fachwerk",
                artifact="roofplan",
                payload=roofplan,
            )

        with trace.stage("plan_openings_for_type") as ev:
            openings = provider.plan_openings_for_type(
                ctx,
                structure=structure,
                interior=interior,
                frameplan=frameplan,
            )
            if trace.enabled:
                trace.add_data(
                    ev,
                    opening_count=len(getattr(openings, "openings", ())),
                )

        with trace.stage("validate_for_type"):
            provider.validate_for_type(
                ctx,
                structure=structure,
                frameplan=frameplan,
            )

        return structure, interior, openings
