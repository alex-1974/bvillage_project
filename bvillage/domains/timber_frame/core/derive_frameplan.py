# bvillage/domains/timber_frame/core/derive_frameplan.py
from __future__ import annotations

from typing import Any

from bvillage.core.model import StructurePlan
from bvillage.domains.timber_frame.contracts.schema_frameplan_fachwerk import (
    FramePlanFachwerk,
)
from bvillage.domains.timber_frame.core.derive_frameplan_boxframe import (
    derive_frameplan_boxframe,
)

__all__ = ["derive_frameplan"]


def derive_frameplan(
    ctx: Any,
    structure: StructurePlan,
    seq: tuple[str, ...] | None = None,
    xs: tuple[float, ...] | None = None,
    cs: dict[str, Any] | None = None,
) -> FramePlanFachwerk:
    """
    Legacy compatibility wrapper.

    Architecture
    ------------
    Domain code must not import type-layer contracts or schemas.
    The previous implementation violated this rule by importing the
    longhouse type schema directly.

    Current role
    ------------
    This function is retained only as a thin compatibility shim for older
    call sites. The canonical domain entry point is now:

        derive_frameplan_boxframe(ctx, structure)

    Notes
    -----
    The legacy parameters `seq`, `xs`, and `cs` are intentionally accepted
    but ignored. The modern members-first frame derivation reads the required
    information directly from StructurePlan.
    """
    _ = seq
    _ = xs
    _ = cs

    return derive_frameplan_boxframe(ctx, structure)
