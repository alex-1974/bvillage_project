# bvillage/types/timber_frame/longhouse/contracts/schema_frame_roles.py

from __future__ import annotations

from typing import Literal, Tuple

FrameRole = Literal[
    "STRUCTURAL",
    "GATE",
    "GABLE_END",
]

ALLOWED_FRAME_ROLES: Tuple[str, ...] = (
    "STRUCTURAL",
    "GATE",
    "GABLE_END",
)

__all__ = [
    "FrameRole",
    "ALLOWED_FRAME_ROLES",
]
