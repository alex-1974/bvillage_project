# bvillage/domains/timber_frame/policies/timber_frame_policy_stack.py

from __future__ import annotations

from dataclasses import replace
from typing import Dict

from bvillage.core.model import Context
from bvillage.core.policy_types import ConstraintSpec, RangeHardSpec, RangeSoftSpec, ResolvedPolicy

from .timber_frame_policy_types import TimberFramePolicySpec


def _baseline() -> TimberFramePolicySpec:

    return TimberFramePolicySpec(
        binder_max=1.60,
        bay_width=3.645,
        building_width=7.2,
        plate_height=2.6,
        bay_count=5,
        gable_mode="end_frame",
    )


def _wealth_layer(wealth: float, fw: TimberFramePolicySpec) -> TimberFramePolicySpec:

    bay_count = fw.bay_count

    if wealth >= 0.80:
        bay_count = 7
    elif wealth >= 0.60:
        bay_count = 6
    elif wealth <= 0.20:
        bay_count = 4

    return replace(fw, bay_count=int(bay_count))


def _archetype_layer(
    archetype_id: str,
    wealth: float,
    fw: TimberFramePolicySpec,
):

    constraints: Dict[str, ConstraintSpec] = {}

    if archetype_id.startswith("FW-LH"):

        base = 1.50
        span = 0.15

        binder_max = base + span * (wealth - 0.5)
        binder_max = max(1.40, min(1.65, binder_max))

        target = 1.35 + 0.10 * (wealth - 0.5)
        target = max(1.20, min(1.50, target))

        jitter = 0.10

        fw = replace(
            fw,
            binder_max=binder_max,
            target_gefach_width=target,
            target_gefach_jitter=jitter,
        )

        constraints["gefach_width_target"] = ConstraintSpec(
            hard=RangeHardSpec(0.0, binder_max),
            soft=RangeSoftSpec(
                ideal=(target - jitter, target + jitter),
                allowed=(1.10, binder_max),
                weight=3.0,
            ),
        )

    return fw, constraints


def resolve_policy_stack(ctx: Context) -> ResolvedPolicy:

    fw = _baseline()

    fw = _wealth_layer(ctx.wealth, fw)

    fw, constraints = _archetype_layer(
        ctx.archetype_id,
        ctx.wealth,
        fw,
    )

    return ResolvedPolicy(
        schema=2,
        constraints=constraints,
        domain=fw,
    )
