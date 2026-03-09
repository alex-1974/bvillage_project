# bvillage/domains/timber_frame/blender/integrity.py

from __future__ import annotations

import logging
from typing import Any

from bvillage.core.errors import SchemaError

__all__ = ["run_integrity_checks", "check_integrity"]

LOG = logging.getLogger("bvillage.domains.timber_frame.blender.integrity")


# ---------------------------------------------------------------------
# Helpers (strict canonical FramePlan)
# ---------------------------------------------------------------------

def _get_basis(fp: dict[str, Any]) -> dict[str, float]:
    """
    Require canonical fp["basis"].

    Required keys
    -------------
    - x_min
    - x_max
    - center_x
    - halfW
    """
    basis = fp.get("basis")
    if not isinstance(basis, dict):
        raise SchemaError("Integrity: missing frameplan basis")

    required = ("x_min", "x_max", "center_x", "halfW")
    out: dict[str, float] = {}

    for key in required:
        if key not in basis:
            raise SchemaError(f"Integrity: basis missing required key '{key}'")
        try:
            out[key] = float(basis[key])
        except Exception as exc:
            raise SchemaError(f"Integrity: invalid basis value for '{key}'") from exc

    return out


def _get_axes_z(fp: dict[str, Any]) -> list[float]:
    """
    Require canonical flattened z-axis list.

    Contract
    --------
    Renderer integrity must not infer or normalize legacy axis payloads.
    """
    axes_z = fp.get("axes_z_flat")
    if not isinstance(axes_z, (list, tuple)):
        raise SchemaError("Integrity: missing canonical axes_z_flat")

    out: list[float] = []
    for i, v in enumerate(axes_z):
        try:
            out.append(float(v))
        except Exception as exc:
            raise SchemaError(f"Integrity: invalid axes_z_flat[{i}]") from exc

    if len(out) < 2:
        raise SchemaError(f"Integrity: axes_z_flat too short (need >=2), got={out!r}")

    return out


def _get_axes_u(fp: dict[str, Any]) -> dict[str, list[float]]:
    """
    Require canonical flattened per-wall u-axis dict.

    Expected shape
    --------------
    {
        "N": [...],
        "S": [...],
        "E": [...],
        "W": [...],
    }
    """
    axes_u = fp.get("axes_u_flat")
    if not isinstance(axes_u, dict):
        raise SchemaError("Integrity: missing canonical axes_u_flat")

    out: dict[str, list[float]] = {}

    for wall in ("N", "S", "E", "W"):
        vals = axes_u.get(wall)
        if not isinstance(vals, (list, tuple)):
            raise SchemaError(f"Integrity: axes_u_flat[{wall!r}] missing or invalid")

        flt: list[float] = []
        for i, v in enumerate(vals):
            try:
                flt.append(float(v))
            except Exception as exc:
                raise SchemaError(f"Integrity: invalid axes_u_flat[{wall!r}][{i}]") from exc

        out[wall] = flt

    return out


def _normalize_openings(fp: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Require canonical normalized openings.

    Contract
    --------
    open entries must already contain:
    - wall
    - u0/u1
    - z0/z1

    No fallback from legacy fp["openings"] is allowed.
    """
    openings = fp.get("openings_norm")
    if openings is None:
        return []

    if not isinstance(openings, list):
        raise SchemaError("Integrity: openings_norm must be a list")

    out: list[dict[str, Any]] = []

    for i, op in enumerate(openings):
        if not isinstance(op, dict):
            raise SchemaError(f"Integrity: openings_norm[{i}] must be dict")

        for key in ("wall", "u0", "u1", "z0", "z1"):
            if key not in op:
                raise SchemaError(f"Integrity: openings_norm[{i}] missing required key '{key}'")

        wall = op["wall"]
        if wall not in ("N", "S", "E", "W"):
            raise SchemaError(f"Integrity: openings_norm[{i}] has invalid wall {wall!r}")

        try:
            out.append(
                {
                    **op,
                    "wall": str(wall),
                    "u0": float(op["u0"]),
                    "u1": float(op["u1"]),
                    "z0": float(op["z0"]),
                    "z1": float(op["z1"]),
                }
            )
        except Exception as exc:
            raise SchemaError(f"Integrity: openings_norm[{i}] contains invalid numeric values") from exc

    return out


def _is_non_decreasing(xs: list[float], *, tol: float = 1e-9) -> bool:
    for i in range(len(xs) - 1):
        if xs[i + 1] + tol < xs[i]:
            return False
    return True


# ---------------------------------------------------------------------
# Main checks
# ---------------------------------------------------------------------

def run_integrity_checks(
    *,
    fp: dict[str, Any],
    house: dict[str, Any],  # kept only for signature compatibility
    col_frame,
    col_roof,
    col_openings,
    col_braces,
    col_infills,
    col_debug,
) -> bool:
    """
    FramePlan-driven integrity checks.

    Notes
    -----
    - strict canonical FramePlan contract
    - no legacy fallbacks
    - no structural inference
    """
    _ = house
    _ = col_frame
    _ = col_roof
    _ = col_openings
    _ = col_braces
    _ = col_infills
    _ = col_debug

    ok = True

    try:
        basis = _get_basis(fp)
        z_list = _get_axes_z(fp)
        axes_u_flat = _get_axes_u(fp)
        openings = _normalize_openings(fp)
    except Exception as exc:
        LOG.error("INTEGRITY FAIL | schema error: %s", exc)
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

    if not _is_non_decreasing(z_list):
        LOG.error("INTEGRITY FAIL | axes_z_flat not sorted/non-decreasing: %r", z_list)
        ok = False

    for wall in ("N", "S", "E", "W"):
        u_list = axes_u_flat[wall]

        if len(u_list) < 2:
            LOG.warning("INTEGRITY warn | axes_u_flat[%s] too short (need >=2), got=%r", wall, u_list)
            continue

        if not _is_non_decreasing(u_list):
            LOG.error("INTEGRITY FAIL | axes_u_flat[%s] not sorted/non-decreasing: %r", wall, u_list)
            ok = False

    for op in openings:
        wall = op["wall"]
        u0 = op["u0"]
        u1 = op["u1"]
        z0 = op["z0"]
        z1 = op["z1"]

        op_name = op.get("name", op.get("id", "?"))

        if u1 <= u0:
            LOG.error("INTEGRITY FAIL | opening %r has u1<=u0", op_name)
            ok = False

        if z1 <= z0:
            LOG.error("INTEGRITY FAIL | opening %r has z1<=z0", op_name)
            ok = False

        if wall in ("E", "W"):
            if u0 < -halfW - 1e-6 or u1 > halfW + 1e-6:
                LOG.warning(
                    "INTEGRITY warn | opening %r u out of wall range: u=[%s,%s] halfW=%s",
                    op_name,
                    u0,
                    u1,
                    halfW,
                )
        else:
            length = x_max - x_min
            if u0 < -0.5 * length - 1e-6 or u1 > 0.5 * length + 1e-6:
                LOG.warning(
                    "INTEGRITY warn | opening %r u out of expected range: u=[%s,%s] L=%s",
                    op_name,
                    u0,
                    u1,
                    length,
                )

        if z0 < z_list[0] - 1e-6 or z1 > z_list[-1] + 1e-6:
            LOG.warning(
                "INTEGRITY warn | opening %r z out of axes_z range: z=[%s,%s] axes=[%s..%s]",
                op_name,
                z0,
                z1,
                z_list[0],
                z_list[-1],
            )

    LOG.info("INTEGRITY done | ok=%s", ok)
    return ok


# ---------------------------------------------------------------------
# Compatibility wrapper (expected by build_frame.py)
# ---------------------------------------------------------------------

def check_integrity(*, fp: dict[str, Any], house: dict[str, Any], collections: dict[str, Any]) -> bool:
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
