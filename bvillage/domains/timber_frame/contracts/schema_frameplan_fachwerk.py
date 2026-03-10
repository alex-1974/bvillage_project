# bvillage/domains/timber_frame/contracts/schema_frameplan_fachwerk.py

from __future__ import annotations

from typing import Any, Dict, List, Tuple, TypedDict

__all__ = [
    "SCHEMA_VERSION_FACHWERK",
    "FrameMember",
    "FrameMembers",
    "FrameLayout",
    "FramePlanFachwerk",
]


SCHEMA_VERSION_FACHWERK = "fachwerk_frameplan.v1"


# ---------------------------------------------------------
# Members
# ---------------------------------------------------------

class FrameMember(TypedDict):
    id: str
    tid: str
    p0: Tuple[float, float, float]
    p1: Tuple[float, float, float]
    tags: Tuple[str, ...]


class FrameMembers(TypedDict):
    posts: List[FrameMember]
    rails: List[FrameMember]
    braces: List[FrameMember]
    infills: List[FrameMember]


# ---------------------------------------------------------
# Frame layout
# ---------------------------------------------------------

class FrameLayout(TypedDict):
    x_frames: List[float]
    y_rows: List[float]
    frame_roles: List[str]


# ---------------------------------------------------------
# FramePlan
# ---------------------------------------------------------

class FramePlanFachwerk(TypedDict):

    schema_version: str

    coordinate_system: Dict[str, Any]

    basis: Dict[str, float]

    frame_layout: FrameLayout

    members: FrameMembers

    openings: List[Dict[str, Any]]

    notes: Dict[str, Any]
