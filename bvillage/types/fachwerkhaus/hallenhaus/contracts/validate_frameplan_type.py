# bvillage/types/fachwerkhaus/hallenhaus/validate_frameplan_type.py

from __future__ import annotations

from bvillage.core.errors import SchemaError
from bvillage.types.fachwerkhaus.hallenhaus.contracts.schema_frame_roles import (
    ALLOWED_FRAME_ROLES,
)
from bvillage.types.fachwerkhaus.hallenhaus.contracts.schema_frameplan_langhaus import (
    FramePlanLanghaus,
)


def _require_keys(obj: dict, keys: tuple[str, ...], ctx: str) -> None:
    for k in keys:
        if k not in obj:
            raise SchemaError(f"{ctx}: missing required key '{k}'")


def validate_frameplan_langhaus_type(frameplan: FramePlanLanghaus) -> None:
    layout = frameplan["frame_layout"]
    _require_keys(layout, ("x_frames", "y_rows", "frame_roles"), "frame_layout")

    xs = layout["x_frames"]
    ys = layout["y_rows"]
    roles = layout["frame_roles"]

    if not isinstance(xs, list) or len(xs) < 2:
        raise SchemaError("frame_layout.x_frames must be list[float] with len>=2")
    if not isinstance(ys, list) or len(ys) < 2:
        raise SchemaError("frame_layout.y_rows must be list[float] with len>=2")
    if not isinstance(roles, list) or len(roles) != len(xs):
        raise SchemaError("frame_layout.frame_roles must match x_frames length")

    for i, x in enumerate(xs):
        if not isinstance(x, (int, float)):
            raise SchemaError(f"frame_layout.x_frames[{i}] not numeric")

    for i, y in enumerate(ys):
        if not isinstance(y, (int, float)):
            raise SchemaError(f"frame_layout.y_rows[{i}] not numeric")

    for i, r in enumerate(roles):
        rr = str(r)
        if rr not in ALLOWED_FRAME_ROLES:
            raise SchemaError(f"frame_layout.frame_roles[{i}] invalid '{rr}'")
