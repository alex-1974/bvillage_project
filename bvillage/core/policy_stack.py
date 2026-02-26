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
    v0.4.0 MVP:
    Resolve a small, type-aware policy set from Context.

    Later:
    - split into modular policy_*.py files
    - add region/epoch tables + overrides
    - add richer schemas + provenance
    """
    epoch = getattr(ctx, "epoch_band", "late_medieval")
    region = getattr(ctx, "region", "north")
    settlement = getattr(ctx, "settlement_type", "village")
    wealth = float(getattr(ctx, "wealth", 0.5))
    house_type = getattr(ctx, "house_type", "")

    # --- Fachwerk domain inputs (minimal) ---
    # Keep your existing idea but move it here (planner stays dumb).
    base = 1.55
    span = 0.35
    b_max = base + span * (wealth - 0.3)
    b_max = max(1.45, min(1.85, b_max))

    fachwerk = FachwerkPolicySpec(
        b_max=b_max,
        default_jamb_t=0.20,
    )

    # --- Constraints (type-specific defaults) ---
    # These are your planner constants, lifted into policy stack.
    # You can later branch on epoch/region/settlement/wealth/house_type.
    constraints: Dict[str, ConstraintSpec] = {}

    if house_type == "fachwerkhaus.hallenhaus":
        # Brustriegel height
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

        # Target infill (gefach) width intent (consumed later by fachwerk-core for secondary studs)
        constraints["gefach_width_target"] = ConstraintSpec(
            hard=RangeHardSpec(0.0, 1.60),
            soft=RangeSoftSpec(
                ideal=(1.20, 1.50),
                allowed=(0.90, 1.60),
                weight=3.0,
            ),
            unit="m",
            code_prefix="HALL",
        )

    else:
        # generic fallback (safe, conservative)
        constraints["brustriegel_z"] = ConstraintSpec(
            hard=None,
            soft=RangeSoftSpec(ideal=(0.95, 1.10), allowed=(0.85, 1.25), weight=1.0),
            unit="m",
            code_prefix="GEN",
        )

    return ResolvedPolicy(
        schema=1,
        constraints=constraints,
        fachwerk=fachwerk,
    )
