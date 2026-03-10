# bvillage/types/timber_frame/longhouse/contracts/validate_frameplan_type.py

from __future__ import annotations

from typing import Any

from bvillage.core.errors import SchemaError

__all__ = ["validate_frameplan_langhaus_type"]


def validate_frameplan_langhaus_type(frameplan: dict[str, Any]) -> None:
    """
    Hallenhaus/Langhaus-specific validation on top of the domain contract.

    Scope
    -----
    - type-specific expectations only
    - does not redefine the general Fachwerk domain schema
    """
    if not isinstance(frameplan, dict):
        raise SchemaError("Type validation requires frameplan dict")

    frame_layout = frameplan.get("frame_layout")
    if not isinstance(frame_layout, dict):
        raise SchemaError("frame_layout missing or invalid")

    frame_roles = frame_layout.get("frame_roles")
    if not isinstance(frame_roles, list) or len(frame_roles) < 2:
        raise SchemaError("Langhaus requires at least 2 frame roles")

    if frame_roles[0] != "GABLE_END":
        raise SchemaError("Langhaus first frame role must be GABLE_END")
    if frame_roles[-1] != "GABLE_END":
        raise SchemaError("Langhaus last frame role must be GABLE_END")

    y_rows = frame_layout.get("y_rows")
    if not isinstance(y_rows, list) or len(y_rows) != 3:
        raise SchemaError("Langhaus currently requires exactly 3 row positions")

    hall_row = float(y_rows[1])
    if abs(hall_row) > 1e-9:
        raise SchemaError("Langhaus hall row must be centered at y=0.0")
