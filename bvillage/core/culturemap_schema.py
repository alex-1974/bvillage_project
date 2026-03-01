# bvillage/core/culturemap_schema.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Sequence, Tuple, Union

LonLat = Tuple[float, float]
BBox = Tuple[float, float, float, float]  # (min_lon, min_lat, max_lon, max_lat)

GeoJSONPolygon = Dict[str, Any]
GeoJSONGeometry = Dict[str, Any]

Role = Literal["core_phase", "expansion", "diaspora", "late_form", "unknown"]


@dataclass(frozen=True, slots=True)
class TimeRange:
    start_year: int
    end_year: int

    def contains(self, year: int) -> bool:
        return self.start_year <= year <= self.end_year


@dataclass(frozen=True, slots=True)
class CultureTrace:
    culture_id: str
    trace_id: str
    label: str
    role: Role

    domain_ids: Tuple[str, ...]
    archetype_ids: Tuple[str, ...]

    core_time: TimeRange
    halo_time: TimeRange

    typicality: float  # 0..1
    confidence: float  # 0..1
    worldview_id: str
    source: str

    core_geometry: GeoJSONGeometry
    halo_geometry: Optional[GeoJSONGeometry]

    core_bbox: BBox
    halo_bbox: Optional[BBox]


@dataclass(frozen=True, slots=True)
class CultureCandidate:
    culture_id: str
    trace_id: str
    score: float

    # “evidence” for debugging / reporting
    m_space: float
    m_time: float
    typicality: float
    confidence: float

    domain_ids: Tuple[str, ...]
    archetype_ids: Tuple[str, ...]
    label: str
    role: Role
    worldview_id: str
    source: str
