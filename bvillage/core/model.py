# bvillage/core/model.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal
from bvillage.core.seed import Seed

# WHY: asdict is intentionally NOT imported here.
# architect.py and planner.py both document the reason:
# "no dataclass.asdict to avoid surprises" — explicit dict construction
# gives stable, debuggable output without hidden recursion over nested dataclasses.

SchemaVersion = Literal["1.0"]
Severity = Literal["HARD", "SOFT", "SUGGEST"]
EpochBand = Literal["early_medieval", "high_medieval", "late_medieval"]

Vec2 = tuple[float, float]
Vec3 = tuple[float, float, float]
Range2 = tuple[float, float]


@dataclass(frozen=True, slots=True)
class Context:
    schema_version: SchemaVersion = "1.0"
    seed: Seed = field(default_factory=lambda: Seed(0))
    region: str = "unknown"
    epoch_band: EpochBand = "high_medieval"
    settlement_type: str = "rural"
    wealth: float = 0.5
    occupants: int = 4
    climate_hint: str = "temperate"
    house_type: str = "fachwerkhaus.hallenhaus"

    # Structural Grammar Architecture (SGA)
    # Grammar is a top-level structural contract, not a policy knob.
    # Default is safe for v0.4.0 (only Hallenhaus exists as active type).
    grammar: str = "hall"


@dataclass(frozen=True, slots=True)
class Footprint:
    length: float
    width: float
    orientation_deg: float = 0.0  # world rotation


@dataclass(frozen=True, slots=True)
class FieldCell:
    id: str
    # bbox in local building coordinates (minx, miny, maxx, maxy)
    bbox: tuple[float, float, float, float]
    tags: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Grid:
    # Axes in local coordinates (meters). Convention:
    # x axis = length direction (longitudinal), y axis = width direction (transverse)
    axes_u: tuple[float, ...]
    axes_v: tuple[float, ...]
    fields: tuple[FieldCell, ...] = ()


@dataclass(frozen=True, slots=True)
class BayFrame:
    id: str
    bay_index: int
    tags: tuple[str, ...] = ("PRIMARY_FRAME",)


@dataclass(frozen=True, slots=True)
class WallSegment:
    id: str
    side: Literal["N", "S", "E", "W"]
    # u_range is along wall run, expressed in meters in local coords (projected scalar along that wall)
    u_range: Range2
    z_range: Range2
    tags: tuple[str, ...] = ("EXTERIOR",)


@dataclass(frozen=True, slots=True)
class ReservedSlot:
    id: str
    field_id: str
    tags: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class StructurePlan:
    schema_version: SchemaVersion = "1.0"
    footprint: Footprint = field(default_factory=lambda: Footprint(0.0, 0.0, 0.0))
    stories: int = 1

    grid: Grid = field(default_factory=lambda: Grid((), (), ()))
    frames: tuple[BayFrame, ...] = ()
    walls: tuple[WallSegment, ...] = ()
    reserved_slots: tuple[ReservedSlot, ...] = ()

    # Optional: planner can store openings already "strategically" chosen (e.g., gate).
    # Interior/openings pipeline may add more later.
    # WHY: dict not frozenset — notes carries heterogeneous structured artifacts
    # (frameplans, reports, domain metadata). Frozen dataclass + mutable notes is
    # intentional: the reference is fixed, the contents are not. See notes.py.
    notes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Zone:
    id: str
    field_ids: tuple[str, ...]
    tags: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Room:
    id: str
    type: str
    field_ids: tuple[str, ...]
    story: int = 0
    tags: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Door:
    id: str
    between: tuple[str, str]  # room ids
    wall_ref: str             # wall id or interior wall id later
    width: float
    z_range: Range2 = (0.0, 2.0)
    tags: tuple[str, ...] = ("INTERIOR_DOOR",)


@dataclass(frozen=True, slots=True)
class OpeningDemand:
    room_id: str
    wall_preference: str = "EXTERIOR"
    min_count: int = 0
    max_count: int = 0
    tags: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class InteriorPlan:
    schema_version: SchemaVersion = "1.0"
    zones: tuple[Zone, ...] = ()
    rooms: tuple[Room, ...] = ()
    doors: tuple[Door, ...] = ()
    opening_demands: tuple[OpeningDemand, ...] = ()
    notes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Opening:
    id: str
    type: Literal["gate", "door", "window", "shutter"]
    wall_id: str
    u_range: Range2
    z_range: Range2
    tags: tuple[str, ...] = ()

    # Animation readiness (pure metadata; blender builder will realize it)
    animation: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class OpeningsPlan:
    schema_version: SchemaVersion = "1.0"
    openings: tuple[Opening, ...] = ()
    notes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Issue:
    code: str
    severity: Severity
    message: str
    related_ids: tuple[str, ...] = ()
    suggested_repairs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Score:
    plausibility: float = 0.0
    usability: float = 0.0
    variety: float = 0.0
    total: float = 0.0
