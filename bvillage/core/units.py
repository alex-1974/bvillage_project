# bvillage/core/units.py

"""
bvillage.core.units
===================

Purpose
-------
Central unit helpers. Internal base unit is meters (m).

This module provides:
- explicit conversions between mm/cm/m
- robust formatting helpers for reports/logs
- minimal parsing helpers (optional; conservative)

Design goals
------------
- Keep domain logic unit-free (always meters).
- Convert only at boundaries: IO, reports, UI.
- Avoid float surprises: use clear rounding in formatting.
- Tiny, dependency-free.

Contracts
---------
to_m(value, unit) -> float
from_m(meters, unit) -> float
fmt_m(meters, unit="m", prec=3) -> str

Units supported: "mm", "cm", "m"

Performance: trivial.
"""

from __future__ import annotations

from typing import Literal

Unit = Literal["mm", "cm", "m"]


# ------------------------------------------------------------
# Conversions (exact scale factors)
# ------------------------------------------------------------

_SCALE_TO_M: dict[Unit, float] = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
}

_SCALE_FROM_M: dict[Unit, float] = {
    "mm": 1000.0,
    "cm": 100.0,
    "m": 1.0,
}


def to_m(value: float, unit: Unit) -> float:
    """
    Convert a length to meters.

    Parameters
    ----------
    value:
        Numeric value in the given unit.
    unit:
        "mm" | "cm" | "m"

    Returns
    -------
    float
        Value in meters.
    """
    return float(value) * _SCALE_TO_M[unit]


def from_m(meters: float, unit: Unit) -> float:
    """
    Convert meters to another unit.

    Parameters
    ----------
    meters:
        Value in meters.
    unit:
        "mm" | "cm" | "m"

    Returns
    -------
    float
        Value in given unit.
    """
    return float(meters) * _SCALE_FROM_M[unit]


# ------------------------------------------------------------
# Formatting helpers
# ------------------------------------------------------------

def fmt_m(meters: float, *, unit: Unit = "m", prec: int = 3) -> str:
    """
    Format meters as a human-readable value with unit.

    Examples
    --------
    fmt_m(2.58) -> "2.580 m"
    fmt_m(0.261, unit="mm", prec=0) -> "261 mm"

    Notes
    -----
    - Formatting only; does not clamp.
    - Uses standard rounding of Python format.
    """
    v = from_m(meters, unit)
    if unit == "mm" and prec == 0:
        # common: integer mm in reports
        return f"{int(round(v))} mm"
    return f"{v:.{prec}f} {unit}"


def fmt_range_m(a: float, b: float, *, unit: Unit = "m", prec: int = 3) -> str:
    """
    Format a range [a,b] in meters.
    """
    return f"[{from_m(a, unit):.{prec}f},{from_m(b, unit):.{prec}f}] {unit}"


def approx_equal(a: float, b: float, *, abs_tol: float = 1e-9) -> bool:
    """
    Absolute tolerance equality helper for unit tests / geometry checks.
    """
    return abs(float(a) - float(b)) <= abs_tol


# ------------------------------------------------------------
# Conservative parsing (optional)
# ------------------------------------------------------------

def parse_length(text: str) -> float:
    """
    Parse a simple length string into meters.

    Supported examples
    ------------------
    "2.58m", "2.58 m"
    "261mm", "261 mm"
    "19.9cm", "19.9 cm"

    Returns
    -------
    float meters

    Raises
    ------
    ValueError on unsupported/ambiguous input.

    Notes
    -----
    This is deliberately conservative. Prefer explicit numeric+unit inputs in code.
    """
    if not isinstance(text, str):
        raise ValueError("parse_length expects a str")

    s = text.strip().lower().replace(" ", "")
    if s.endswith("mm"):
        return to_m(float(s[:-2]), "mm")
    if s.endswith("cm"):
        return to_m(float(s[:-2]), "cm")
    if s.endswith("m"):
        return to_m(float(s[:-1]), "m")

    raise ValueError(f"Unsupported length format: {text!r}")
