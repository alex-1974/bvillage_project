# tests/test_axes_u.py

"""
tests.test_axes_u
=================

Tests for vertical axis computation along walls.

Units: meters.
"""

from __future__ import annotations

from bvillage.domains.timber_frame.core.axes_u import compute_vertical_axes, interval_intersects
from bvillage.domains.timber_frame.core.openings_norm import normalize_openings_from_plan
from conftest import make_structure, make_openings_plan, opening


def _span_intersects_any_opening(wall: str, a: float, b: float, openings_final) -> bool:
    for op in openings_final:
        if op.wall != wall:
            continue
        if interval_intersects(a, b, op.u0, op.u1):
            return True
    return False


def test_compute_vertical_axes_primary_and_opening_axes_present():
    structure = make_structure(L=10.0, W=4.0, z0=0.0, H_e=2.5)
    ops = make_openings_plan(
        opening(oid="Gate", typ="gate", wall_id="W_S_0", u0=-1.0, u1=1.0, z0=0.0, z1=2.2),
    )
    openings_final = normalize_openings_from_plan(ops, default_jamb_thickness=0.2, width_type="axis")

    v = compute_vertical_axes(L=structure.footprint.length, W=structure.footprint.width, binder_max=1.5, openings=list(openings_final))

    assert set(v.keys()) == {"N", "S", "E", "W"}
    assert v["S"]["primary"] == [-5.0, 5.0]
    assert v["S"]["opening"] == [-1.0, 1.0]
    assert v["S"]["all"] == sorted(v["S"]["all"])


def test_compute_vertical_axes_secondary_limits_spans_outside_openings():
    structure = make_structure(L=10.0, W=4.0, z0=0.0, H_e=2.5)
    ops = make_openings_plan(
        opening(oid="Gate", typ="gate", wall_id="W_S_0", u0=-1.0, u1=1.0, z0=0.0, z1=2.2),
    )
    openings_final = normalize_openings_from_plan(ops, default_jamb_thickness=0.2, width_type="axis")

    binder_max = 1.5
    v = compute_vertical_axes(L=structure.footprint.length, W=structure.footprint.width, binder_max=binder_max, openings=list(openings_final))
    all_axes = v["S"]["all"]

    for a, b in zip(all_axes[:-1], all_axes[1:]):
        span = b - a
        if span > binder_max + 1e-9:
            assert _span_intersects_any_opening("S", a, b, openings_final), (a, b, span)
