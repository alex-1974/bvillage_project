# bvillage/domains/fachwerk/blender/integrity.py

#
# Post-flight integrity checks for Fachwerk builds (scene vs plan).
#
# Purpose:
#   Verify that the Blender output matches the FramePlan + house mapping.
#
# Notes:
#   - Fast + robust: uses object origins (midpoints), not mesh endpoints.
#   - Designed for logging-first usage during development.
#   - strict=False recommended in interactive Blender runs.
#
# Naming contract assumed:
#   Opening parts are named: <OPENING_NAME>_<PART>
#     window: JAMB_L, JAMB_R, LINTEL, SILL
#     gate  : JAMB_L, JAMB_R, LINTEL

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import bpy

LOG = logging.getLogger("bvillage.domains.fachwerk.blender.integrity")


@dataclass(frozen=True, slots=True)
class IntegrityConfig:
    tol_plane: float = 0.03         # meters: tolerance for wall plane checks
    strict: bool = False            # raise RuntimeError on hard failures
    max_listed_failures: int = 20   # don't spam logs


# ------------------------------------------------------------
# Small helpers
# ------------------------------------------------------------

def _centroid_world(obj: bpy.types.Object) -> Tuple[float, float, float]:
    """
    Robust centroid for objects whose mesh vertices are already in world space
    (like our make_beam_rect implementation).
    If the object has a transform, we still respect matrix_world.
    """
    if obj is None:
        return (0.0, 0.0, 0.0)

    if obj.type == "MESH" and obj.data is not None and hasattr(obj.data, "vertices") and len(obj.data.vertices) > 0:
        sx = sy = sz = 0.0
        n = len(obj.data.vertices)
        mw = obj.matrix_world
        for v in obj.data.vertices:
            p = mw @ v.co
            sx += float(p.x)
            sy += float(p.y)
            sz += float(p.z)
        return (sx / n, sy / n, sz / n)

    # fallback: object origin
    loc = obj.matrix_world.translation
    return (float(loc.x), float(loc.y), float(loc.z))
    
def _count_all_objects(col: bpy.types.Collection) -> int:
    try:
        return sum(1 for _ in col.all_objects)
    except Exception:
        try:
            return len(col.objects)
        except Exception:
            return 0


def _obj_by_name(name: str) -> Optional[bpy.types.Object]:
    return bpy.data.objects.get(name)


def _abs(x: float) -> float:
    return x if x >= 0.0 else -x


def _walls_basis(house: Dict[str, Any]) -> Dict[str, float]:
    axis_x = house["axis_x"]
    axis_y = house["axis_y"]

    x_min = float(min(axis_x))
    x_max = float(max(axis_x))
    center_x = 0.5 * (x_min + x_max)

    y_min = float(min(axis_y))
    y_max = float(max(axis_y))
    halfW = 0.5 * (y_max - y_min)

    return {"x_min": x_min, "x_max": x_max, "center_x": center_x, "halfW": halfW}


def _opening_expected_parts(opening_type: str) -> List[str]:
    if opening_type == "window":
        return ["JAMB_L", "JAMB_R", "LINTEL", "SILL"]
    if opening_type == "gate":
        return ["JAMB_L", "JAMB_R", "LINTEL"]
    # future-proof fallback
    return ["JAMB_L", "JAMB_R", "LINTEL"]


def _wall_plane_expected(wall: str, basis: Dict[str, float]) -> Tuple[str, float]:
    w = wall.upper()
    if w == "N":
        return ("y", -basis["halfW"])
    if w == "S":
        return ("y", +basis["halfW"])
    if w == "E":
        return ("x", +basis["x_max"])
    if w == "W":
        return ("x", +basis["x_min"])
    return ("", 0.0)


def _plane_value(obj: bpy.types.Object, axis: str) -> float:
    cx, cy, cz = _centroid_world(obj)
    if axis == "x":
        return cx
    if axis == "y":
        return cy
    if axis == "z":
        return cz
    return 0.0


# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------

def run_integrity_checks(
    *,
    fp: Dict[str, Any],
    house: Dict[str, Any],
    col_frame: bpy.types.Collection,
    col_roof: bpy.types.Collection,
    col_openings: bpy.types.Collection,
    col_braces: bpy.types.Collection,
    col_infills: bpy.types.Collection,
    col_debug: bpy.types.Collection,
    config: Optional[IntegrityConfig] = None,
) -> Dict[str, Any]:
    cfg = config or IntegrityConfig()
    basis = _walls_basis(house)

    openings = fp.get("openings") or []
    axes_u = fp.get("axes_u") or {}
    z_axes = fp.get("axes_z") or []

    hard_failures: List[str] = []
    soft_warnings: List[str] = []

    counts = {
        "frame": _count_all_objects(col_frame),
        "roof": _count_all_objects(col_roof),
        "openings": _count_all_objects(col_openings),
        "braces": _count_all_objects(col_braces),
        "infills": _count_all_objects(col_infills),
        "debug": _count_all_objects(col_debug),
    }

    LOG.info(
        "INTEGRITY start | counts frame=%d roof=%d openings=%d braces=%d infills=%d debug=%d",
        counts["frame"], counts["roof"], counts["openings"], counts["braces"], counts["infills"], counts["debug"],
    )
    LOG.info(
        "INTEGRITY basis | x=[%.3f..%.3f] center_x=%.3f halfW=%.3f z_axes=%d openings=%d",
        basis["x_min"], basis["x_max"], basis["center_x"], basis["halfW"], len(z_axes), len(openings),
    )

    # --------------------------------------------------------
    # 1) Opening frame parts exist and lie on expected wall plane
    # --------------------------------------------------------
    expected_opening_objects = 0

    for o in openings:
        name = str(o.get("name", "?"))
        typ = str(o.get("type", ""))
        wall = str(o.get("wall", ""))

        parts = _opening_expected_parts(typ)
        expected_opening_objects += len(parts)

        axis, target = _wall_plane_expected(wall, basis)
        if not axis:
            hard_failures.append(f"opening {name}: unknown wall '{wall}'")
            continue

        for part in parts:
            obj_name = f"{name}_{part}"
            obj = _obj_by_name(obj_name)
            if obj is None:
                hard_failures.append(f"missing opening part: {obj_name}")
                continue

            v = _plane_value(obj, axis)
            if _abs(v - target) > cfg.tol_plane:
                hard_failures.append(
                    f"opening {name} part {part}: off wall plane {axis}={v:.3f} expected {target:.3f} tol={cfg.tol_plane:.3f}"
                )

    if counts["openings"] != expected_opening_objects:
        # keep it soft: later you may add decorative members
        soft_warnings.append(
            f"openings count mismatch: expected {expected_opening_objects} (by contract) got {counts['openings']}"
        )

    # --------------------------------------------------------
    # 2) Braces count expectation (corner-only heuristic)
    # --------------------------------------------------------
    expected_braces = 0
    for wall in ("N", "S", "E", "W"):
        u_all = axes_u.get(wall, {}).get("all") or []
        if len(u_all) >= 2:
            expected_braces += 2

    if counts["braces"] != expected_braces:
        soft_warnings.append(f"braces count mismatch: expected {expected_braces} got {counts['braces']}")

    # --------------------------------------------------------
    # 3) Infills count range (max bound + conservative min estimate)
    # --------------------------------------------------------
    if len(z_axes) >= 2:
        n_z_cells = len(z_axes) - 1

        max_panels = 0
        for wall in ("N", "S", "E", "W"):
            u_all = axes_u.get(wall, {}).get("all") or []
            if len(u_all) >= 2:
                max_panels += (len(u_all) - 1) * n_z_cells

        # Conservative estimate of fully-covered cells by openings
        est_cover = 0
        for o in openings:
            wall = str(o.get("wall", "")).upper()
            u_all = [float(u) for u in (axes_u.get(wall, {}).get("all") or [])]
            if len(u_all) < 2:
                continue

            u0o = float(o.get("u0", 0.0))
            u1o = float(o.get("u1", 0.0))
            z0o = float(o.get("z0", 0.0))
            z1o = float(o.get("z1", 0.0))
            lo_uo, hi_uo = (min(u0o, u1o), max(u0o, u1o))
            lo_zo, hi_zo = (min(z0o, z1o), max(z0o, z1o))

            for i in range(len(u_all) - 1):
                cu0, cu1 = float(u_all[i]), float(u_all[i + 1])
                lo_cu, hi_cu = (min(cu0, cu1), max(cu0, cu1))
                if lo_cu >= lo_uo and hi_cu <= hi_uo:
                    for j in range(len(z_axes) - 1):
                        cz0, cz1 = float(z_axes[j]), float(z_axes[j + 1])
                        lo_cz, hi_cz = (min(cz0, cz1), max(cz0, cz1))
                        if lo_cz >= lo_zo and hi_cz <= hi_zo:
                            est_cover += 1

        min_panels = max(0, max_panels - est_cover)

        actual = counts["infills"]
        LOG.info(
            "INTEGRITY infills range | z_cells=%d max=%d min_est=%d est_cover=%d actual=%d",
            n_z_cells, max_panels, min_panels, est_cover, actual,
        )

        if actual > max_panels:
            hard_failures.append(f"infills too many: got {actual} max {max_panels}")
        if actual < min_panels:
            soft_warnings.append(f"infills unusually low: got {actual} min_est {min_panels} (est_cover={est_cover})")
    else:
        soft_warnings.append("infills range check skipped: z_axes < 2")

    # --------------------------------------------------------
    # 4) Report
    # --------------------------------------------------------
    for msg in soft_warnings[: cfg.max_listed_failures]:
        LOG.warning("INTEGRITY warn | %s", msg)
    if len(soft_warnings) > cfg.max_listed_failures:
        LOG.warning("INTEGRITY warn | ... and %d more", len(soft_warnings) - cfg.max_listed_failures)

    for msg in hard_failures[: cfg.max_listed_failures]:
        LOG.error("INTEGRITY FAIL | %s", msg)
    if len(hard_failures) > cfg.max_listed_failures:
        LOG.error("INTEGRITY FAIL | ... and %d more", len(hard_failures) - cfg.max_listed_failures)

    ok = (len(hard_failures) == 0)
    LOG.info("INTEGRITY done | ok=%s hard=%d soft=%d", ok, len(hard_failures), len(soft_warnings))

    result = {
        "ok": ok,
        "counts": counts,
        "hard": hard_failures,
        "soft": soft_warnings,
        "basis": basis,
    }

    if cfg.strict and not ok:
        raise RuntimeError(f"Integrity check failed: hard={len(hard_failures)} soft={len(soft_warnings)}")

    return result
    
# ---------------------------------------------------------------------
# Public API compatibility (stable symbol expected by build_frame.py)
# ---------------------------------------------------------------------

def check_integrity(*, fp, house, collections):
    """
    Compatibility wrapper for build_frame.py.

    Expects collections dict with keys:
        frame, roof, openings, braces, infills, debug
    """
    return run_integrity_checks(
        fp=fp,
        house=house,
        col_frame=collections["frame"],
        col_roof=collections["roof"],
        col_openings=collections["openings"],
        col_braces=collections["braces"],
        col_infills=collections["infills"],
        col_debug=collections["debug"],
    )
