# bvillage/core/culturemap_query.py
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Tuple

from .culturemap_schema import BBox, GeoJSONGeometry, LonLat


def bbox_of_polygon_coords(coords: Any) -> BBox:
    """
    coords for Polygon: [ ring0, ring1, ... ], ring: [[lon,lat], ...]
    coords for MultiPolygon: [ polygon0, polygon1, ... ]
    """
    min_lon = 1e99
    min_lat = 1e99
    max_lon = -1e99
    max_lat = -1e99

    def _update(pt):
        nonlocal min_lon, min_lat, max_lon, max_lat
        lon, lat = float(pt[0]), float(pt[1])
        if lon < min_lon:
            min_lon = lon
        if lon > max_lon:
            max_lon = lon
        if lat < min_lat:
            min_lat = lat
        if lat > max_lat:
            max_lat = lat

    def _walk(obj):
        # We expect nested lists: multipolygon -> polygon -> ring -> point
        if not obj:
            return
        first = obj[0]
        if isinstance(first, (int, float)):  # point [lon, lat]
            _update(obj)
            return
        for x in obj:
            _walk(x)

    _walk(coords)
    return (min_lon, min_lat, max_lon, max_lat)


def bbox_contains(bbox: BBox, lon: float, lat: float) -> bool:
    min_lon, min_lat, max_lon, max_lat = bbox
    return (min_lon <= lon <= max_lon) and (min_lat <= lat <= max_lat)


def point_in_ring(lon: float, lat: float, ring: List[List[float]]) -> bool:
    """
    Ray casting algorithm.
    ring: list of [lon,lat], ideally closed, but we handle open rings too.
    """
    inside = False
    n = len(ring)
    if n < 3:
        return False

    x, y = lon, lat
    j = n - 1
    for i in range(n):
        xi, yi = float(ring[i][0]), float(ring[i][1])
        xj, yj = float(ring[j][0]), float(ring[j][1])

        # check edge intersects ray to +inf in x direction
        intersects = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 0.0) + xi)
        if intersects:
            inside = not inside
        j = i

    return inside


def point_in_polygon(lon: float, lat: float, coords: Any) -> bool:
    """
    Polygon coords: [outer_ring, hole1, hole2,...]
    """
    if not coords or not isinstance(coords, list):
        return False
    outer = coords[0]
    if not point_in_ring(lon, lat, outer):
        return False
    # holes
    for hole in coords[1:]:
        if point_in_ring(lon, lat, hole):
            return False
    return True


def point_in_geometry(lon: float, lat: float, geom: GeoJSONGeometry) -> bool:
    """
    Supports GeoJSON Polygon / MultiPolygon.
    """
    gtype = geom.get("type")
    coords = geom.get("coordinates")

    if gtype == "Polygon":
        return point_in_polygon(lon, lat, coords)

    if gtype == "MultiPolygon":
        if not isinstance(coords, list):
            return False
        for poly_coords in coords:
            if point_in_polygon(lon, lat, poly_coords):
                return True
        return False

    return False
