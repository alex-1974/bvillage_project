# bvillage/core/culturemap_resolve.py

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Tuple

from .hot_path import hot
from .culturemap_schema import CultureCandidate, CultureTrace
from .culturemap_load import load_culture_traces_geojson
from .culturemap_query import bbox_contains, point_in_geometry


def _m_time(trace: CultureTrace, year: int) -> float:
    if trace.core_time.contains(year):
        return 1.0
    if trace.halo_time.contains(year):
        return 0.5
    return 0.0


def _m_space(trace: CultureTrace, lon: float, lat: float) -> float:
    # fast reject core bbox
    if bbox_contains(trace.core_bbox, lon, lat):
        if point_in_geometry(lon, lat, trace.core_geometry):
            return 1.0

    # halo
    if trace.halo_geometry is not None and trace.halo_bbox is not None:
        if bbox_contains(trace.halo_bbox, lon, lat):
            if point_in_geometry(lon, lat, trace.halo_geometry):
                return 0.5

    return 0.0


def _score(trace: CultureTrace, lon: float, lat: float, year: int) -> Tuple[float, float, float]:
    ms = _m_space(trace, lon, lat)
    if ms <= 0.0:
        return 0.0, 0.0, 0.0
    mt = _m_time(trace, year)
    if mt <= 0.0:
        return 0.0, ms, 0.0
    score = trace.typicality * trace.confidence * ms * mt
    return score, ms, mt


@lru_cache(maxsize=8)
def _load_default_catalog() -> List[CultureTrace]:
    """
    Default path: bvillage/data/culturemap/cultures.geojson (relative to project root).
    Adjust as needed in your runner if your cwd differs.
    """
    p = Path("bvillage/data/culturemap/cultures.geojson")
    return load_culture_traces_geojson(p)

@hot
def culture_candidates(
    lon: float,
    lat: float,
    year: int,
    *,
    worldview_id: str = "default",
    top_k: int = 10,
    catalog: Optional[List[CultureTrace]] = None,
) -> List[CultureCandidate]:
    """
    Resolve culture candidates for a given lon/lat/year.
    Returns sorted list (best score first). Deterministic ordering.

    Notes:
    - lon/lat in WGS84 degrees
    - year is integer (BC as negative)
    """
    if catalog is None:
        catalog = _load_default_catalog()

    cands: List[CultureCandidate] = []
    for tr in catalog:
        if worldview_id != "default" and tr.worldview_id != worldview_id:
            continue

        s, ms, mt = _score(tr, lon, lat, year)
        if s <= 0.0:
            continue

        cands.append(
            CultureCandidate(
                culture_id=tr.culture_id,
                trace_id=tr.trace_id,
                score=s,
                m_space=ms,
                m_time=mt,
                typicality=tr.typicality,
                confidence=tr.confidence,
                domain_ids=tr.domain_ids,
                archetype_ids=tr.archetype_ids,
                label=tr.label,
                role=tr.role,
                worldview_id=tr.worldview_id,
                source=tr.source,
            )
        )

    # Deterministic sorting: score desc, then ids
    cands.sort(key=lambda c: (-c.score, c.culture_id, c.trace_id))
    if top_k > 0:
        return cands[:top_k]
    return cands
