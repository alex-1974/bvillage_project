# bvillage/core/policy_stack.py

from __future__ import annotations
from typing import Dict

from .model import Context
from .policy_types import (
    ResolvedPolicy,
    ConstraintSpec,
    RangeHardSpec,
    RangeSoftSpec,
    FachwerkPolicySpec,
)


def resolve_policy_stack(ctx: Context) -> ResolvedPolicy:
    """
    Resolve minimal cultural + structural policy from Context.

    This is the ONLY place where:
    - b_max
    - target_gefach_w
    - typological parameters

    are derived.

    Planner and Domains must not invent structural defaults.
    """

    epoch = getattr(ctx, "epoch_band", "late_medieval")
    region = getattr(ctx, "region", "north")
    settlement = getattr(ctx, "settlement_type", "village")
    wealth = float(getattr(ctx, "wealth", 0.5))
    house_type = getattr(ctx, "house_type", "")

    # =========================================================
    # Fachwerk Structural Policy
    # =========================================================

    if house_type == "fachwerkhaus.hallenhaus":

        # ---- Statics limit (hard structural max spacing) ----
        # Historically narrower than decorative later Fachwerk.
        # Wealth slightly increases span (better timber quality).
        base = 1.50
        span = 0.15
        b_max = base + span * (wealth - 0.5)
        b_max = max(1.40, min(1.65, b_max))

        # ---- Cultural target gefach width (aesthetic rhythm) ----
        # Long walls in Hallenhaus typically 1.20–1.50 m
        target_gefach_w = 1.35 + 0.10 * (wealth - 0.5)
        target_gefach_w = max(1.20, min(1.50, target_gefach_w))

        target_gefach_jitter = 0.08

    else:
        # Generic fallback for other Fachwerk types
        b_max = 1.65
        target_gefach_w = 1.45
        target_gefach_jitter = 0.12

    fachwerk = FachwerkPolicySpec(
        b_max=b_max,
        default_jamb_t=0.20,
    )

    # =========================================================
    # Constraints (minimal MVP set)
    # =========================================================

    constraints: Dict[str, ConstraintSpec] = {}

    if house_type == "fachwerkhaus.hallenhaus":

        constraints["brustriegel_z"] = ConstraintSpec(
            hard=None,
            soft=RangeSoftSpec(
                ideal=(0.95, 1.10),
                allowed=(0.85, 1.25),
                weight=1.0,
            ),
            unit="m",
            code_prefix="HALL",
        )

        constraints["gefach_width_target"] = ConstraintSpec(
            hard=RangeHardSpec(0.0, b_max),
            soft=RangeSoftSpec(
                ideal=(target_gefach_w - 0.10, target_gefach_w + 0.10),
                allowed=(1.10, b_max),
                weight=3.0,
            ),
            unit="m",
            code_prefix="HALL",
        )

    return ResolvedPolicy(
        schema=2,
        constraints=constraints,
        fachwerk=fachwerk,
    )
