# bvillage/core/geom_eps.py

"""
bvillage.core.geom_eps
======================

Central numeric tolerances for geometric computations.

Why
---
Floating point jitter accumulates. Using inconsistent eps values across modules
creates hard-to-debug edge cases (axes missing, overlaps, spurious thin bands).

Policy
------
- Distinguish "merge tolerances" (clustering values) from "inside checks"
  (strict interior rules).
- Keep eps values stable; change only with explicit justification.

Units
-----
All eps values in meters (base unit).

Recommended usage
-----------------
- EPS_EQ: for approximate equality checks.
- EPS_MERGE: for deduplicating / clustering near-equal coordinates.
- EPS_INSIDE: for "strictly inside" checks (avoid snapping to boundaries).
"""

from __future__ import annotations

from dataclasses import dataclass


# Approx equality for coordinates (meters)
EPS_EQ: float = 1e-9

# Merge tolerance for axis clustering/dedup (meters)
EPS_MERGE: float = 1e-6

# Strict interior margin for "inside opening" checks (meters)
EPS_INSIDE: float = 1e-6


def approx_equal(a: float, b: float, *, abs_tol: float = EPS_EQ) -> bool:
    """Absolute tolerance equality helper."""
    return abs(float(a) - float(b)) <= abs_tol


def clamp(v: float, lo: float, hi: float) -> float:
    """Clamp value to [lo, hi]."""
    v = float(v)
    lo = float(lo)
    hi = float(hi)
    if hi < lo:
        lo, hi = hi, lo
    return lo if v < lo else hi if v > hi else v
    
def clamp01(v: float) -> float:
    """Clamp value to [0, 1]."""
    return clamp(v, 0.0, 1.0)


def eps_eq(a: float, b: float, *, abs_tol: float = EPS_EQ) -> bool:
    """EPS-aware equality."""
    return approx_equal(a, b, abs_tol=abs_tol)


def eps_le(a: float, b: float, *, abs_tol: float = EPS_EQ) -> bool:
    """a <= b with EPS tolerance."""
    return float(a) <= float(b) + abs_tol


def eps_ge(a: float, b: float, *, abs_tol: float = EPS_EQ) -> bool:
    """a >= b with EPS tolerance."""
    return float(a) >= float(b) - abs_tol
