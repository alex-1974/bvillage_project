# bvillage/core/validate.py

"""
bvillage.core.validate
======================

Purpose
-------
Generic validation of generated plans to prevent "mystery failures".

Design
------
- Core validation stays house-type agnostic.
- Type-specific validation lives next to the type implementation.
- `validate()` runs core checks + (optional) type hook.

Type Hook Convention
--------------------
If ctx.house_type == "fachwerkhaus.hallenhaus", we attempt to import:

    bvillage.types.fachwerkhaus.hallenhaus.validate

and call:

    validate_type(ctx, structure, interior) -> list[Issue]

If module or function does not exist, it's skipped.

Units: meters (only indirectly relevant here).
Performance: O(n) over rooms/doors/demands; tiny.
"""

from __future__ import annotations

import importlib
from typing import Dict, List, Set

from .model import Context, StructurePlan, InteriorPlan, Issue


def validate(ctx: Context, structure: StructurePlan, interior: InteriorPlan) -> List[Issue]:
    """
    Validate structure + interior plan coherence.

    Returns
    -------
    list[Issue]
        Empty list means "no detected issues".
    """
    issues: List[Issue] = []

    # Core (type-agnostic) checks
    issues.extend(_validate_connectivity(interior))
    issues.extend(_validate_opening_feasibility(structure, interior))

    # Optional type hook
    issues.extend(_try_type_validation(ctx, structure, interior))

    return issues


# ============================================================
# Core Validators (agnostic)
# ============================================================

def _validate_connectivity(interior: InteriorPlan) -> List[Issue]:
    """
    All rooms should be reachable via the door graph.
    """
    rooms = {r.id for r in interior.rooms}
    if not rooms:
        return [Issue(code="H_NO_ROOMS", severity="HARD", message="No rooms generated.")]

    adj: Dict[str, Set[str]] = {rid: set() for rid in rooms}
    for d in interior.doors:
        a, b = d.between
        if a in rooms and b in rooms:
            adj[a].add(b)
            adj[b].add(a)

    start = next(iter(rooms))
    seen = {start}
    q = [start]
    while q:
        cur = q.pop()
        for nxt in adj[cur]:
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)

    if seen != rooms:
        missing = sorted(list(rooms - seen))
        return [
            Issue(
                code="H_ROOMS_NOT_CONNECTED",
                severity="HARD",
                message=f"Not all rooms are reachable from {start}. Unreachable: {missing}",
                related_ids=tuple(missing),
                suggested_repairs=("R_ADD_CONNECTION_DOOR",),
            )
        ]

    return []


def _validate_opening_feasibility(structure: StructurePlan, interior: InteriorPlan) -> List[Issue]:
    """
    If any demand requires exterior openings, ensure the structure has WINDOW_OK segments.
    """
    issues: List[Issue] = []

    window_ok = any(("WINDOW_OK" in w.tags) for w in structure.walls)

    for od in interior.openings_demands:
        if od.min_count > 0 and od.wall_preference == "EXTERIOR" and not window_ok:
            issues.append(
                Issue(
                    code="H_NO_WINDOW_POTENTIAL",
                    severity="HARD",
                    message=f"Room {od.room_id} demands exterior windows but no WINDOW_OK wall segments exist.",
                    related_ids=(od.room_id,),
                    suggested_repairs=("R_ENABLE_WINDOW_WALLS",),
                )
            )

    return issues


# ============================================================
# Type-specific hook (optional)
# ============================================================

def _try_type_validation(ctx: Context, structure: StructurePlan, interior: InteriorPlan) -> List[Issue]:
    """
    Attempt to run type-specific validation.

    Convention:
      ctx.house_type = "fachwerkhaus.hallenhaus"
      -> module "bvillage.types.fachwerkhaus.hallenhaus.validate"
      -> function "validate_type(ctx, structure, interior) -> list[Issue]"

    If not present, returns [].

    Notes
    -----
    - Any import errors are converted into a HARD issue with details.
      That way broken plugins are visible but don't crash batch generation.
    """
    ht = getattr(ctx, "house_type", None)
    if not isinstance(ht, str) or not ht:
        return []

    mod_name = f"bvillage.types.{ht}.validate"
    try:
        mod = importlib.import_module(mod_name)
    except ModuleNotFoundError:
        return []
    except Exception as exc:
        return [
            Issue(
                code="H_TYPE_VALIDATE_IMPORT_FAIL",
                severity="HARD",
                message=f"Failed to import type validator {mod_name}: {exc}",
                related_ids=(ht,),
                suggested_repairs=("R_FIX_TYPE_VALIDATOR_IMPORT",),
            )
        ]

    fn = getattr(mod, "validate_type", None)
    if fn is None:
        return []

    try:
        out = fn(ctx, structure, interior)
    except Exception as exc:
        return [
            Issue(
                code="H_TYPE_VALIDATE_CRASH",
                severity="HARD",
                message=f"Type validator crashed for {ht}: {exc}",
                related_ids=(ht,),
                suggested_repairs=("R_FIX_TYPE_VALIDATOR",),
            )
        ]

    if out is None:
        return []
    return list(out)
