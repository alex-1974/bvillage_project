# bvillage/domains/fachwerk/blender/materials_assign.py

from __future__ import annotations

from typing import Any, Optional

import bpy

from bvillage.core.materials.material_registry import resolve_for_builder
from bvillage.domains.fachwerk.blender.materials_adapter import apply_material_to_object


def assign_member_material(
    *,
    obj: Optional[bpy.types.Object],
    member: dict[str, Any],
    ctx_view: Any,
    default_material_id: str,
    name_hint: str,
) -> None:
    """Resolve deterministic material for a member and assign to a Blender object.

    Single canonical path for *all* Blender modules:
      resolve_for_builder(...) -> apply_material_to_object(...)

    Notes
    -----
    - This function performs no logging (hot path safe).
    - Errors should be handled at the call site where phase/context is known.
    """
    if obj is None:
        return

    resolved, surface, sample = resolve_for_builder(
        member,
        ctx_view,
        default_material_id=default_material_id,
    )

    apply_material_to_object(
        obj=obj,
        resolved=resolved,
        surface=surface,
        sample=sample,
        ctx=ctx_view,
        member=member,
        name_hint=name_hint,
    )
