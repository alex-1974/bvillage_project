# bvillage/core/model.py

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple, Literal
from bvillage.core.seed import Seed

SchemaVersion = Literal["1.0"]
Severity = Literal["HARD", "SOFT", "SUGGEST"]
EpochBand = Literal["E1", "E2", "E3"]

Vec2 = Tuple[float, float]
Vec3 = Tuple[float, float, float]
Range2 = Tuple[float, float]


@dataclass(frozen=True)
class Context:
    schema_version: SchemaVersion = "1.0"
    seed: Seed = Seed(0)

    region: str = "unknown"
    epoch_band: EpochBand = "E2"
    settlement_type: str = "rural"  # rural / village / town
    wealth: float = 0.5            # 0..1
    occupants: int = 4
    climate_hint: str = "temperate"

    house_type: str = "hallenhaus"  # plugin id


@dataclass(frozen=True)
class Footprint:
    length: float
    width: float
    orientation_deg: float = 0.0  # world rotation


@dataclass(frozen=True)
class FieldCell:
    id: str
    # bbox in local building coordinates (minx, miny, maxx, maxy)
    bbox: Tuple[float, float, float, float]
    tags: Tuple[str, ...] = ()


@dataclass(frozen=True)
class Grid:
    # Axes in local coordinates (meters). Convention:
    # x axis = length direction (longitudinal), y axis = width direction (transverse)
    axis_x: Tuple[float, ...]
    axis_y: Tuple[float, ...]
    fields: Tuple[FieldCell, ...] = ()


@dataclass(frozen=True)
class BayFrame:
    id: str
    bay_index: int
    tags: Tuple[str, ...] = ("PRIMARY_FRAME",)


@dataclass(frozen=True)
class WallSegment:
    id: str
    side: Literal["N", "S", "E", "W"]
    # u_axis is along wall run, expressed in meters in local coords (projected scalar along that wall)
    u_axis: Range2
    z_range: Range2
    tags: Tuple[str, ...] = ("EXTERIOR",)


@dataclass(frozen=True)
class ReservedSlot:
    id: str
    field_id: str
    tags: Tuple[str, ...]


@dataclass(frozen=True)
class StructurePlan:
    schema_version: SchemaVersion = "1.0"
    footprint: Footprint = Footprint(0.0, 0.0, 0.0)
    stories: int = 1

    grid: Grid = Grid((), (), ())
    frames: Tuple[BayFrame, ...] = ()
    walls: Tuple[WallSegment, ...] = ()
    reserved_slots: Tuple[ReservedSlot, ...] = ()

    # Optional: planner can store openings already “strategically” chosen (e.g., gate).
    # Interior/openings pipeline may add more later.
    notes: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Zone:
    id: str
    field_ids: Tuple[str, ...]
    tags: Tuple[str, ...] = ()


@dataclass(frozen=True)
class Room:
    id: str
    type: str
    field_ids: Tuple[str, ...]
    story: int = 0
    tags: Tuple[str, ...] = ()


@dataclass(frozen=True)
class Door:
    id: str
    between: Tuple[str, str]  # room ids
    wall_ref: str             # wall id or interior wall id later
    width: float
    z_range: Range2 = (0.0, 2.0)
    tags: Tuple[str, ...] = ("INTERIOR_DOOR",)


@dataclass(frozen=True)
class OpeningDemand:
    room_id: str
    wall_preference: str = "EXTERIOR"
    min_count: int = 0
    max_count: int = 0
    tags: Tuple[str, ...] = ()


@dataclass(frozen=True)
class InteriorPlan:
    schema_version: SchemaVersion = "1.0"
    zones: Tuple[Zone, ...] = ()
    rooms: Tuple[Room, ...] = ()
    doors: Tuple[Door, ...] = ()
    openings_demands: Tuple[OpeningDemand, ...] = ()
    notes: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Opening:
    id: str
    type: Literal["gate", "door", "window", "shutter"]
    wall_id: str
    u_axis: Range2
    z_range: Range2
    tags: Tuple[str, ...] = ()

    # Animation readiness (pure metadata; blender builder will realize it)
    animation: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class OpeningsPlan:
    schema_version: SchemaVersion = "1.0"
    openings: Tuple[Opening, ...] = ()
    notes: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Issue:
    code: str
    severity: Severity
    message: str
    related_ids: Tuple[str, ...] = ()
    suggested_repairs: Tuple[str, ...] = ()


@dataclass(frozen=True)
class Score:
    plausibility: float = 0.0
    usability: float = 0.0
    variety: float = 0.0
    total: float = 0.0


@dataclass(frozen=True)
class EntryPoint:
    type: str  # main_entry / service_entry / etc.
    location: Vec3
    normal: Vec3
    width: float


@dataclass(frozen=True)
class AnimatableGroup:
    opening_id: str
    object_group_name: str


@dataclass(frozen=True)
class BuildManifest:
    schema_version: SchemaVersion = "1.0"
    house_id: str = "H_0"
    entry_points: Tuple[EntryPoint, ...] = ()
    animatable_groups: Tuple[AnimatableGroup, ...] = ()
    metadata: Dict[str, Any] = field(default_factory=dict)


def to_dict(obj: Any) -> Dict[str, Any]:
    """Stable conversion for JSON logging/versioning."""
    return asdict(obj)
