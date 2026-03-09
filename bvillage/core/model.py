# bvillage/core/model.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from bvillage.core.seed import Seed

# WHY: asdict is intentionally NOT imported here.
# Plans are meant to be assembled explicitly to keep output stable,
# debuggable, and free of hidden recursion surprises.

SchemaVersion = Literal["1.0"]
Severity = Literal["HARD", "SOFT", "SUGGEST"]
EpochBand = Literal["early_medieval", "high_medieval", "late_medieval"]

Vec2 = tuple[float, float]
Vec3 = tuple[float, float, float]
Range2 = tuple[float, float]


@dataclass(frozen=True, slots=True)
class Context:
    """
    Generation context for one building request.

    Architecture
    ------------
    Context carries only generation inputs.

    It must not contain:
    - plugin paths
    - provider ids
    - type-family folder names

    Canonical dispatch input:
    - archetype_id (stable machine-readable id, e.g. FW-LH-ND)

    Notes
    -----
    archetype_id is resolved by the Foreman/dispatch layer into:
    - domain
    - type_family
    - construction_grammar

    grammar remains an explicit structural contract because it is used
    as a generation invariant during the ongoing v0.4 migration.
    """
    schema_version: SchemaVersion = "1.0"

    seed: Seed = field(default_factory=lambda: Seed(0))

    region: str = "unknown"
    epoch_band: EpochBand = "high_medieval"
    settlement_type: str = "rural"
    wealth: float = 0.5

    occupants: int = 4
    climate_hint: str = "temperate"

    # Stable dispatch key, resolved via plugin registry / archetype binding.
    archetype_id: str = "FW-LH-ND"

    # Structural Grammar Architecture (SGA)
    # Grammar is a structural contract, not a free-form style knob.
    # It may later be resolved entirely from archetype binding, but remains
    # explicit for now to support migration and invariant checks.
    grammar: str = "hall"


@dataclass(frozen=True, slots=True)
class Footprint:
    """
    Building footprint in local building coordinates.
    """
    length: float
    width: float
    orientation_deg: float = 0.0


@dataclass(frozen=True, slots=True)
class FieldCell:
    """
    Semantic topology cell in local building coordinates.

    bbox = (minx, miny, maxx, maxy)
    """
    id: str
    bbox: tuple[float, float, float, float]
    tags: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Grid:
    """
    Topological axis/grid structure.

    Convention
    ----------
    x axis = longitudinal
    y axis = transverse
    """
    axes_u: tuple[float, ...]
    axes_v: tuple[float, ...]
    fields: tuple[FieldCell, ...] = ()


@dataclass(frozen=True, slots=True)
class BayFrame:
    """
    Semantic primary frame marker.

    This is topology metadata, not a structural member.
    """
    id: str
    bay_index: int
    tags: tuple[str, ...] = ("PRIMARY_FRAME",)


@dataclass(frozen=True, slots=True)
class WallSegment:
    """
    Exterior or future interior wall segment.

    u_range is expressed as a scalar interval along the wall run.
    z_range is vertical extent in local coordinates.
    """
    id: str
    side: Literal["N", "S", "E", "W"]
    u_range: Range2
    z_range: Range2
    tags: tuple[str, ...] = ("EXTERIOR",)


@dataclass(frozen=True, slots=True)
class ReservedSlot:
    """
    Semantic reservation inside topology.

    Used for zones such as hearth, circulation reserve, etc.
    """
    id: str
    field_id: str
    tags: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class StructurePlan:
    """
    Canonical type-layer topology artifact.

    Responsibilities
    ----------------
    - footprint
    - grid
    - semantic frames
    - wall segments
    - reserved topology slots

    Non-responsibilities
    --------------------
    - no structural member geometry
    - no Blender data
    """
    schema_version: SchemaVersion = "1.0"

    footprint: Footprint = field(default_factory=lambda: Footprint(0.0, 0.0, 0.0))
    stories: int = 1

    grid: Grid = field(default_factory=lambda: Grid((), (), ()))
    frames: tuple[BayFrame, ...] = ()
    walls: tuple[WallSegment, ...] = ()
    reserved_slots: tuple[ReservedSlot, ...] = ()

    # Heterogeneous structured side-channel for transitional artifacts.
    # Reference is fixed (frozen dataclass), contents may evolve during pipeline.
    notes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Zone:
    """
    Semantic zone spanning one or more field cells.
    """
    id: str
    field_ids: tuple[str, ...]
    tags: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Room:
    """
    Room-level semantic subdivision.
    """
    id: str
    type: str
    field_ids: tuple[str, ...]
    story: int = 0
    tags: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Door:
    """
    Interior connection between two rooms.
    """
    id: str
    between: tuple[str, str]
    wall_ref: str
    width: float
    z_range: Range2 = (0.0, 2.0)
    tags: tuple[str, ...] = ("INTERIOR_DOOR",)


@dataclass(frozen=True, slots=True)
class OpeningDemand:
    """
    Interior-driven demand for later opening planning.
    """
    room_id: str
    wall_preference: str = "EXTERIOR"
    min_count: int = 0
    max_count: int = 0
    tags: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class InteriorPlan:
    """
    Canonical interior semantics artifact.
    """
    schema_version: SchemaVersion = "1.0"
    zones: tuple[Zone, ...] = ()
    rooms: tuple[Room, ...] = ()
    doors: tuple[Door, ...] = ()
    opening_demands: tuple[OpeningDemand, ...] = ()
    notes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Opening:
    """
    Finalized exterior opening choice.

    Animation metadata is descriptive only; realization happens in Blender layer.
    """
    id: str
    type: Literal["gate", "door", "window", "shutter"]
    wall_id: str
    u_range: Range2
    z_range: Range2
    tags: tuple[str, ...] = ()
    animation: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class OpeningsPlan:
    """
    Canonical opening artifact.
    """
    schema_version: SchemaVersion = "1.0"
    openings: tuple[Opening, ...] = ()
    notes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Issue:
    """
    Validation or audit issue.
    """
    code: str
    severity: Severity
    message: str
    related_ids: tuple[str, ...] = ()
    suggested_repairs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Score:
    """
    Aggregate evaluation metrics.
    """
    plausibility: float = 0.0
    usability: float = 0.0
    variety: float = 0.0
    total: float = 0.0
