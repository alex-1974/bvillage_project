# tests/test_openings_norm.py

"""
tests.test_openings_norm
=======================

Tests for openings normalization (OpeningsPlan -> OpeningFinal).

Units: meters.
"""

from __future__ import annotations

from bvillage.domains.timber_frame.core.openings_norm import normalize_openings_from_plan
from conftest import opening, make_openings_plan


def test_normalize_openings_maps_wall_id_to_side():
    ops = make_openings_plan(
        opening(oid="Op1", typ="door", wall_id="W_S_0", u0=-1.0, u1=1.0, z0=0.0, z1=2.0),
        opening(oid="Op2", typ="window", wall_id="W_N_0", u0=2.0, u1=3.0, z0=1.0, z1=1.6),
    )
    finals = normalize_openings_from_plan(ops, default_jamb_thickness=0.2, width_type="axis")

    assert len(finals) == 2
    by_name = {f.name: f for f in finals}
    assert by_name["Op1"].wall == "S"
    assert by_name["Op2"].wall == "N"


def test_normalize_openings_axis_width_default_produces_clear_minus_jamb():
    ops = make_openings_plan(
        opening(oid="Op1", typ="door", wall_id="W_S_0", u0=-1.0, u1=1.0, z0=0.0, z1=2.0),
    )
    finals = normalize_openings_from_plan(ops, default_jamb_thickness=0.2, width_type="axis")
    f = finals[0]

    assert f.width_range == 2.0
    assert abs(f.width_clear - 1.8) < 1e-9
    assert abs(f.u_center - 0.0) < 1e-9
    assert abs(f.u0 - (-1.0)) < 1e-9
    assert abs(f.u1 - (1.0)) < 1e-9


def test_normalize_openings_clear_width_expands_axis_by_jamb():
    ops = make_openings_plan(
        opening(oid="Op1", typ="door", wall_id="W_S_0", u0=-1.0, u1=1.0, z0=0.0, z1=2.0),
    )
    finals = normalize_openings_from_plan(ops, default_jamb_thickness=0.2, width_type="clear")
    f = finals[0]

    assert abs(f.width_clear - 2.0) < 1e-9
    assert abs(f.width_range - 2.2) < 1e-9
    assert abs(f.u_center - 0.0) < 1e-9
    assert abs(f.u0 - (-1.1)) < 1e-9
    assert abs(f.u1 - (1.1)) < 1e-9
