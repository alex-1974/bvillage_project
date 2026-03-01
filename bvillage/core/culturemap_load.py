# bvillage/core/culturemap_load.py

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .culturemap_schema import CultureTrace, TimeRange
from .culturemap_query import bbox_of_polygon_coords


def _as_tuple_str(xs: Any) -> Tuple[str, ...]:
    if xs is None:
        return ()
    if isinstance(xs, (list, tuple)):
        out: List[str] = []
        for x in xs:
            if isinstance(x, str) and x:
                out.append(x)
        return tuple(out)
    if isinstance(xs, str) and xs:
        return (xs,)
    return ()


def _get_int(d: Dict[str, Any], key: str, default: int) -> int:
    v = d.get(key, default)
    try:
        return int(v)
    except Exception:
        return default


def _get_float(d: Dict[str, Any], key: str, default: float) -> float:
    v = d.get(key, default)
    try:
        return float(v)
    except Exception:
        return default


def load_culture_traces_geojson(path: str | Path) -> List[CultureTrace]:
    """
    Load CultureTrace features from a FeatureCollection GeoJSON.

    Supported:
    - core geometry is stored as feature.geometry
    - halo geometry is stored in feature.properties_ext.halo_geometry (optional)
    - bbox optional: feature.bbox (if absent, computed)
    """
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))

    if data.get("type") != "FeatureCollection":
        raise ValueError(f"Expected FeatureCollection in {p}")

    traces: List[CultureTrace] = []
    for feat in data.get("features", []):
        if not isinstance(feat, dict) or feat.get("type") != "Feature":
            continue

        props = feat.get("properties") or {}
        props_ext = feat.get("properties_ext") or {}

        culture_id = str(props.get("culture_id", "")).strip()
        trace_id = str(props.get("trace_id", "")).strip()
        label = str(props.get("label", "")).strip() or trace_id
        role = str(props.get("role", "unknown")).strip() or "unknown"

        if not culture_id or not trace_id:
            # skip malformed
            continue

        domain_ids = _as_tuple_str(props.get("domain_ids"))
        archetype_ids = _as_tuple_str(props.get("archetype_ids"))

        ct = props.get("core_time") or {}
        ht = props.get("halo_time") or {}

        core_time = TimeRange(
            start_year=_get_int(ct, "start_year", -10**9),
            end_year=_get_int(ct, "end_year", 10**9),
        )
        halo_time = TimeRange(
            start_year=_get_int(ht, "start_year", core_time.start_year),
            end_year=_get_int(ht, "end_year", core_time.end_year),
        )

        typicality = _get_float(props, "typicality", 1.0)
        confidence = _get_float(props, "confidence", 1.0)
        worldview_id = str(props.get("worldview_id", "default")).strip() or "default"
        source = str(props.get("source", "unknown")).strip() or "unknown"

        core_geom = feat.get("geometry")
        if not isinstance(core_geom, dict):
            continue

        halo_geom = props_ext.get("halo_geometry")
        if halo_geom is not None and not isinstance(halo_geom, dict):
            halo_geom = None

        # bbox
        bbox = feat.get("bbox")
        if isinstance(bbox, list) and len(bbox) == 4:
            core_bbox = (float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3]))
        else:
            core_bbox = bbox_of_polygon_coords(core_geom.get("coordinates"))

        halo_bbox = None
        if halo_geom is not None:
            halo_bbox = bbox_of_polygon_coords(halo_geom.get("coordinates"))

        traces.append(
            CultureTrace(
                culture_id=culture_id,
                trace_id=trace_id,
                label=label,
                role=role,  # type: ignore[arg-type]
                domain_ids=domain_ids,
                archetype_ids=archetype_ids,
                core_time=core_time,
                halo_time=halo_time,
                typicality=max(0.0, min(1.0, typicality)),
                confidence=max(0.0, min(1.0, confidence)),
                worldview_id=worldview_id,
                source=source,
                core_geometry=core_geom,
                halo_geometry=halo_geom,
                core_bbox=core_bbox,
                halo_bbox=halo_bbox,
            )
        )

    # Deterministic ordering (stable diffs)
    traces.sort(key=lambda t: (t.culture_id, t.trace_id))
    return traces
