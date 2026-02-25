# bvillage/types/fachwerkhaus/hallenhaus/validate.py

"""
bvillage.types.fachwerkhaus.hallenhaus.validate
==============================================

Hallenhaus-specific validation rules.

These rules were intentionally moved out of bvillage.core.validate
to keep core type-agnostic.

Contracts
---------
validate_type(ctx, structure, interior) -> list[Issue]

Units: meters (area proxy via grid fields).
"""

from __future__ import annotations

from typing import List

from bvillage.core.model import Context, StructurePlan, InteriorPlan, Issue


def validate_type(ctx: Context, structure: StructurePlan, interior: InteriorPlan) -> List[Issue]:
    """
    Hallenhaus rules:
    - DIELE must exist and be >= 40% of fields
    - For rural/village: STALL must exist and be >= 20% of fields
    """
    issues: List[Issue] = []

    total_fields = len(structure.grid.fields)
    if total_fields <= 0:
        return [Issue(code="H_NO_FIELDS", severity="HARD", message="Structure grid has no fields.")]

    room_by_id = {r.id: r for r in interior.rooms}

    # DIELE dominance
    diele = room_by_id.get("R_DIELE")
    if diele is None:
        issues.append(
            Issue(
                code="H_NO_DIELE",
                severity="HARD",
                message="Hallenhaus requires a DIELE room (R_DIELE).",
                suggested_repairs=("R_CREATE_DIELE",),
            )
        )
    else:
        share = len(diele.field_ids) / total_fields
        if share < 0.40:
            issues.append(
                Issue(
                    code="H_NO_DIELE_DOMINANCE",
                    severity="HARD",
                    message=f"DIELE too small: {share:.2%} < 40%.",
                    related_ids=(diele.id,),
                    suggested_repairs=("R_EXTEND_DIELE", "R_REDUCE_OTHER_ZONES"),
                )
            )

    # STALL share for rural/village
    if ctx.settlement_type in ("rural", "village"):
        stall = room_by_id.get("R_STALL")
        if stall is None:
            issues.append(
                Issue(
                    code="H_NO_STALL",
                    severity="HARD",
                    message="Rural hallenhaus requires a STALL room (R_STALL).",
                    suggested_repairs=("R_CREATE_STALL",),
                )
            )
        else:
            share = len(stall.field_ids) / total_fields
            if share < 0.20:
                issues.append(
                    Issue(
                        code="H_STALL_TOO_SMALL",
                        severity="HARD",
                        message=f"STALL too small: {share:.2%} < 20%.",
                        related_ids=(stall.id,),
                        suggested_repairs=("R_EXTEND_STALL", "R_REDUCE_OTHER_ZONES"),
                    )
                )

    return issues
