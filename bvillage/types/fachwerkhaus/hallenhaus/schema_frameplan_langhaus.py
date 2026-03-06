# bvillage/types/fachwerkhaus/hallenhaus/schema_frameplan_langhaus.py

from __future__ import annotations

from typing import List, Literal, Optional, Sequence, Tuple, TypedDict

from bvillage.types.fachwerkhaus.hallenhaus.schema_frame_roles import FrameRole

Vec3 = Tuple[float, float, float]

Units = Literal["meters"]
AxisOrigin = Literal["building_center_ground"]

AxisX = Literal["longitudinal_forward"]
AxisY = Literal["right_when_facing_positive_x"]
AxisZ = Literal["up"]


class CoordinateSystemAxes(TypedDict):
    x: AxisX
    y: AxisY
    z: AxisZ


class CoordinateSystem(TypedDict):
    origin: AxisOrigin
    axes: CoordinateSystemAxes
    units: Units


class BasisHeights(TypedDict):
    z0: float
    z_plate: float


class FrameLayout(TypedDict):
    x_frames: List[float]
    y_rows: List[float]
    frame_roles: List[FrameRole]


class ProfileRect(TypedDict):
    w: float
    d: float


class Member(TypedDict, total=False):
    id: str
    tid: str
    p0: Vec3
    p1: Vec3

    profile: Optional[ProfileRect]
    material_id: Optional[str]
    tags: Optional[Sequence[str]]


class Members(TypedDict):
    posts: List[Member]
    rails: List[Member]
    braces: List[Member]
    infills: List[Member]


WallSide = Literal["N", "S", "E", "W"]
OpeningType = Literal["door", "gate", "window"]


class Opening(TypedDict):
    id: str
    type: OpeningType
    wall: WallSide
    u0: float
    u1: float
    z0: float
    z1: float


class Meta(TypedDict, total=False):
    building_type: str
    epoch: str
    region: str
    seed: int


class FramePlanLanghaus(TypedDict):
    schema_version: int
    coordinate_system: CoordinateSystem
    basis: BasisHeights
    frame_layout: FrameLayout
    members: Members
    openings: Optional[List[Opening]]
    meta: Optional[Meta]


SCHEMA_VERSION_LANGHAUS: int = 4

__all__ = [
    "Vec3",
    "Units",
    "AxisOrigin",
    "AxisX",
    "AxisY",
    "AxisZ",
    "CoordinateSystemAxes",
    "CoordinateSystem",
    "BasisHeights",
    "FrameLayout",
    "ProfileRect",
    "Member",
    "Members",
    "WallSide",
    "OpeningType",
    "Opening",
    "Meta",
    "FramePlanLanghaus",
    "SCHEMA_VERSION_LANGHAUS",
]
