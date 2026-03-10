# bvillage/domains/timber_frame/contracts/schema_roofplan_timber_frame.py

from __future__ import annotations
from typing import TypedDict, List, Dict


class RoofMember(TypedDict):
    id: str
    tid: str
    p0: List[float]
    p1: List[float]
    profile: Dict[str, float]


class RoofMembers(TypedDict):
    ridge: List[RoofMember]
    rafters: List[RoofMember]
    collar_ties: List[RoofMember]


class RoofBasis(TypedDict):
    x_frames: List[float]
    half_width: float
    z_plate: float
    pitch_deg: float
    z_ridge: float
    z_kehl: float
    y_kehl: float
    kehl_frac: float


class RoofPlanTimberFrame(TypedDict):
    schema_version: str
    coordinate_system: str
    roof_type: str
    basis: RoofBasis
    members: RoofMembers
