# bvillage/domains/fachwerk/blender/integrity.py

import logging
from typing import Any, Dict, List, Tuple

LOG = logging.getLogger("bvillage.domains.fachwerk.blender.integrity")


# ---------------------------------------------------------------------
# Helpers (canonical FramePlan-first)
# ---------------------------------------------------------------------

def _get_basis(fp: Dict[str, Any]) -> Dict[str, float]:
    """
    Prefer canonical fp["basis"].
    Fallback: derive from fp["dims"] (L,W).
    """
    basis = fp.get("basis")
    if isinstance(basis, dict) and all(k in basis for k in ("x_min", "x_max", "center_x", "halfW")):
        return {
            "x_min": float(basis["x_min"]),
            "x_max": float(basis["x_max"]),
            "center_x": float(basis["center_x"]),
            "halfW": float(basis["halfW"]),
        }

    dims = fp.get("dims") or {}
    L = dims.get("L")
    W = dims.get("W")
    if L is None or W is None:
        raise ValueError("Missing basis and dims.L/dims.W in frameplan dict")

    Lf = float(L)
    Wf = float(W)
    return {"x_min": 0.0, "x_max": Lf, "center_x": 0.5 * Lf, "halfW": 0.5 * Wf}


def _as_float_list(x: Any) -> List[float]:
    """
    Accept list/tuple of numerics; return float list.
    If dict is given, values are collected recursively (best-effort).
    """
    vals: List[float] = []

    def _collect(v: Any) -> None:
        if v is None:
            return
        if isinstance(v, (int, float)):
            vals.append(float(v))
            return
        if isinstance(v, str):
            try:
                vals.append(float(v))
            except Exception:
                return
            return
        if isinstance(v, (list, tuple)):
            for it in v:
                _collect(it)
            return
        if isinstance(v, dict):
            for it in v.values():
                _collect(it)
            return

    _collect(x)
    return vals


def _is_non_decreasing(xs: List[float], *, tol: float = 1e-9) -> bool:
    for i in range(len(xs) - 1):
        if xs[i + 1] + tol < xs[i]:
            return False
    return True


def _normalize_openings(fp: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Prefer canonical fp["openings_norm"] where u0/u1/z0/z1 exist as floats.
    Fallback: attempt to normalize fp["openings"].
    """
    on = fp.get("openings_norm")
    if isinstance(on, list) and on:
        out = []
        for op in on:
            if not isinstance(op, dict):
                continue
            if all(k in op for k in ("wall", "u0", "u1", "z0", "z1")):
                o2 = dict(op)
                o2["u0"] = float(o2["u0"])
                o2["u1"] = float(o2["u1"])
                o2["z0"] = float(o2["z0"])
                o2["z1"] = float(o2["z1"])
                out.append(o2)
        return out

    openings = fp.get("openings") or []
    if isinstance(openings, dict):
        openings = list(openings.values())
    if not isinstance(openings, list):
        return []

    out = []
    for op in openings:
        if not isinstance(op, dict):
            continue
        wall = op.get("wall")
        if wall is None:
            continue

        u0 = op.get("u0"); u1 = op.get("u1")
        if u0 is None or u1 is None:
            ur = op.get("u")
            if isinstance(ur, (list, tuple)) and len(ur) == 2:
                u0, u1 = ur[0], ur[1]

        z0 = op.get("z0"); z1 = op.get("z1")
        if z0 is None or z1 is None:
            zr = op.get("z")
            if isinstance(zr, (list, tuple)) and len(zr) == 2:
                z0, z1 = zr[0], zr[1]

        if u0 is None or u1 is None or z0 is None or z1 is None:
            continue

        o2 = dict(op)
        o2["u0"] = float(u0)
        o2["u1"] = float(u1)
        o2["z0"] = float(z0)
        o2["z1"] = float(z1)
        out.append(o2)

    return out


# ---------------------------------------------------------------------
# Main checks
# ---------------------------------------------------------------------

def run_integrity_checks(
    *,
    fp: Dict[str, Any],
    house: Dict[str, Any],  # kept for signature compatibility (not required)
    col_frame,
    col_roof,
    col_openings,
    col_braces,
    col_infills,
    col_debug,
) -> bool:
    """
    FramePlan-driven integrity checks.

    Notes:
      - This is intentionally light-weight: fail fast on schema/range issues.
      - Detailed geometric validation can live in core audits/tests.
    """
    ok = True

    # Basis
    try:
        basis = _get_basis(fp)
    except Exception as exc:
        LOG.error("INTEGRITY FAIL | missing basis: %s", exc)
        return False

    x_min = basis["x_min"]
    x_max = basis["x_max"]
    center_x = basis["center_x"]
    halfW = basis["halfW"]

    if not (x_max > x_min):
        LOG.error("INTEGRITY FAIL | invalid basis x-range: x_min=%s x_max=%s", x_min, x_max)
        ok = False
    if not (halfW > 0.0):
        LOG.error("INTEGRITY FAIL | invalid basis halfW=%s", halfW)
        ok = False

    # Axes (canonical preferred)
    axes_z = fp.get("axes_z_flat")
    if axes_z is None:
        axes_z = fp.get("axes_z")
    z_list = _as_float_list(axes_z)
    z_list = sorted(set(z_list))

    if len(z_list) < 2:
        LOG.error("INTEGRITY FAIL | axes_z missing/too short (need >=2), got=%r", z_list)
        ok = False
    elif not _is_non_decreasing(z_list):
        LOG.error("INTEGRITY FAIL | axes_z not sorted/non-decreasing: %r", z_list)
        ok = False

    axes_u_flat = fp.get("axes_u_flat")
    if not isinstance(axes_u_flat, dict):
        # fallback
        axes_u_flat = fp.get("axes_u") if isinstance(fp.get("axes_u"), dict) else {}

    # Per-wall u-axes basic checks
    for wall in ("N", "S", "E", "W"):
        u_any = axes_u_flat.get(wall, [])
        u_list = _as_float_list(u_any)
        u_list = sorted(set(u_list))

        if len(u_list) < 2:
            LOG.warning("INTEGRITY warn | axes_u[%s] missing/too short (need >=2), got=%r", wall, u_list)
            continue
        if not _is_non_decreasing(u_list):
            LOG.error("INTEGRITY FAIL | axes_u[%s] not sorted/non-decreasing: %r", wall, u_list)
            ok = False

    # Openings range checks
    openings = _normalize_openings(fp)
    for op in openings:
        wall = op.get("wall")
        u0 = float(op["u0"]); u1 = float(op["u1"])
        z0 = float(op["z0"]); z1 = float(op["z1"])

        if u1 <= u0:
            LOG.error("INTEGRITY FAIL | opening %r has u1<=u0", op.get("name", op.get("id", "?")))
            ok = False
        if z1 <= z0:
            LOG.error("INTEGRITY FAIL | opening %r has z1<=z0", op.get("name", op.get("id", "?")))
            ok = False

        # Wall-specific u bounds: for N/S, u is along x around center_x; for E/W, u is y in [-halfW..+halfW]
        if wall in ("E", "W"):
            if u0 < -halfW - 1e-6 or u1 > halfW + 1e-6:
                LOG.warning("INTEGRITY warn | opening %r u out of wall range: u=[%s,%s] halfW=%s",
                            op.get("name", op.get("id", "?")), u0, u1, halfW)
        else:
            # N/S: allow u in [-L/2..+L/2] loosely derived from center_x
            L = x_max - x_min
            if u0 < -0.5 * L - 1e-6 or u1 > 0.5 * L + 1e-6:
                LOG.warning("INTEGRITY warn | opening %r u out of expected range: u=[%s,%s] L=%s",
                            op.get("name", op.get("id", "?")), u0, u1, L)

        # z bounds
        if z_list:
            if z0 < z_list[0] - 1e-6 or z1 > z_list[-1] + 1e-6:
                LOG.warning("INTEGRITY warn | opening %r z out of axes_z range: z=[%s,%s] axes=[%s..%s]",
                            op.get("name", op.get("id", "?")), z0, z1, z_list[0], z_list[-1])

    LOG.info("INTEGRITY done | ok=%s", ok)
    return ok


# ---------------------------------------------------------------------
# Compatibility wrapper (expected by build_frame.py)
# ---------------------------------------------------------------------

def check_integrity(*, fp: Dict[str, Any], house: Dict[str, Any], collections: Dict[str, Any]) -> bool:
    """
    build_frame.py expects check_integrity(fp=..., house=..., collections=...).

    collections keys:
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
