# tests/test_engine_contracts.py

"""
tests.test_engine_contracts
===========================

High-value invariant tests for the Fachwerk engine.

These tests are deliberately more strict than the unit tests:
- They validate monotonicity, bounds, containment, and non-overlap constraints.
- They protect against "patch chaos" regressions.

Scope
-----
- bvillage.domains.fachwerk.core.openings_norm
- bvillage.domains.fachwerk.core.axes_u
- bvillage.domains.fachwerk.core.axes_z
- bvillage.domains.fachwerk.core.frameplan

Units: meters.
"""

from __future__ import annotations

from typing import Iterable

from bvillage.domains.fachwerk.core.openings_norm import normalize_openings_from_plan
from bvillage.domains.fachwerk.core.axes_u import compute_vertical_axes
from bvillage.domains.fachwerk.core.axes_z import compute_z_axes
from bvillage.domains.fachwerk.core.frameplan import build_frameplan, FramePolicy

from conftest import make_structure, make_openings_plan, opening


EPS = 1e-9


def _is_sorted(xs: Iterable[float]) -> bool:
    xs = list(xs)
    return all(xs[i] <= xs[i + 1] + EPS for i in range(len(xs) - 1))


def _within(a: float, x: float, b: float) -> bool:
    return (x >= a - EPS) and (x <= b + EPS)


def _strictly_inside(a: float, x: float, b: float) -> bool:
    return (x > a + 1e-6) and (x < b - 1e-6)


def test_contract_openings_final_sorted_and_ranges_valid():
    ops = make_openings_plan(
        opening(oid="Gate", typ="gate", wall_id="W_S_0", u0=+1.0, u1=-1.0, z0=2.2, z1=0.0),  # inverted on purpose
        opening(oid="Win", typ="window", wall_id="W_N_0", u0=3.0, u1=2.0, z0=1.6, z1=0.9),   # inverted on purpose
    )
    finals = normalize_openings_from_plan(ops, default_jamb_t=0.2, width_type="axis")

    # deterministic ordering by (wall, u_center, name)
    assert finals[0].wall <= finals[1].wall

    for o in finals:
        assert o.u0 <= o.u1
        assert o.z0 <= o.z1
        assert o.width_axis > 0
        assert o.width_clear > 0


def test_contract_axes_u_contains_wall_bounds_and_opening_edges():
    structure = make_structure(L=10.0, W=4.0, z0=0.0, H_e=2.58)
    ops = make_openings_plan(
        opening(oid="Gate", typ="gate", wall_id="W_S_0", u0=-1.0, u1=1.0, z0=0.0, z1=2.2),
        opening(oid="WinS", typ="window", wall_id="W_S_0", u0=3.0, u1=4.0, z0=0.9, z1=1.6),
    )
    finals = normalize_openings_from_plan(ops, default_jamb_t=0.2, width_type="axis")

    v = compute_vertical_axes(L=structure.footprint.length, W=structure.footprint.width, b_max=1.5, openings=list(finals))

    # S wall bounds must be present
    assert v["S"]["primary"] == [-5.0, 5.0]

    # opening axes must include edges (for each opening)
    opening_edges = sorted({-1.0, 1.0, 3.0, 4.0})
    assert v["S"]["opening"] == opening_edges

    # 'all' must be sorted + include all fixed axes
    assert _is_sorted(v["S"]["all"])
    for u in v["S"]["primary"] + v["S"]["opening"]:
        assert any(abs(u - a) <= 1e-9 for a in v["S"]["all"])


def test_contract_axes_u_secondary_not_inside_openings():
    structure = make_structure(L=10.0, W=4.0, z0=0.0, H_e=2.58)
    ops = make_openings_plan(
        opening(oid="Gate", typ="gate", wall_id="W_S_0", u0=-1.0, u1=1.0, z0=0.0, z1=2.2),
    )
    finals = normalize_openings_from_plan(ops, default_jamb_t=0.2, width_type="axis")

    v = compute_vertical_axes(L=structure.footprint.length, W=structure.footprint.width, b_max=0.9, openings=list(finals))
    sec = v["S"]["secondary"]

    # No secondary axis strictly inside the opening interval
    for u in sec:
        assert not _strictly_inside(-1.0, u, 1.0)


def test_contract_axes_u_all_within_wall_range():
    structure = make_structure(L=12.0, W=6.0, z0=0.0, H_e=2.58)
    ops = make_openings_plan(
        opening(oid="Win", typ="window", wall_id="W_N_0", u0=-5.0, u1=-3.0, z0=0.9, z1=1.6),
    )
    finals = normalize_openings_from_plan(ops, default_jamb_t=0.2, width_type="axis")

    v = compute_vertical_axes(L=structure.footprint.length, W=structure.footprint.width, b_max=1.0, openings=list(finals))

    # For N/S walls: range is [-L/2, +L/2]
    umin, umax = -12.0 / 2.0, 12.0 / 2.0
    for u in v["N"]["all"]:
        assert _within(umin, u, umax)


def test_contract_axes_z_contains_bounds_and_opening_edges():
    structure = make_structure(L=10.0, W=4.0, z0=0.1, H_e=2.7)
    ops = make_openings_plan(
        opening(oid="Gate", typ="gate", wall_id="W_S_0", u0=-1.0, u1=1.0, z0=0.1, z1=2.2),
        opening(oid="Win", typ="window", wall_id="W_N_0", u0=2.0, u1=3.0, z0=0.9, z1=1.6),
    )
    finals = normalize_openings_from_plan(ops, default_jamb_t=0.2, width_type="axis")

    z_axes, _, _ = compute_z_axes(
        z0=0.1,
        H_e=2.7,
        horizontal_axes_style=[0.1, 0.9, 1.6, 2.2, 2.7],
        z_merge_tol=1e-6,
        z_band_min=0.15,
        z_band_target_min=0.25,
        openings=list(finals),
    )

    assert _is_sorted(z_axes)
    assert 0.1 in z_axes
    assert 2.7 in z_axes
    assert 0.9 in z_axes
    assert 1.6 in z_axes
    assert 2.2 in z_axes


def test_contract_frameplan_self_consistent():
    structure = make_structure(L=19.9, W=6.9, z0=0.0, H_e=2.58)
    ops = make_openings_plan(
        opening(oid="Door", typ="door", wall_id="W_S_0", u0=-4.3, u1=-1.3, z0=0.0, z1=2.2),
        opening(oid="WinS", typ="window", wall_id="W_S_0", u0=3.0, u1=4.2, z0=0.9, z1=1.6),
        opening(oid="WinN", typ="window", wall_id="W_N_0", u0=1.6, u1=2.8, z0=0.9, z1=1.6),
    )
    policy = FramePolicy(b_max=1.4)

    fp = build_frameplan(
        structure=structure,
        openings=ops,
        policy=policy,
        seed=123,
    )

    # dimensions must match footprint + inferred wall height
    assert abs(fp.L - 19.9) < 1e-9
    assert abs(fp.W - 6.9) < 1e-9
    assert abs(fp.z0 - 0.0) < 1e-9
    # FramePlan repairs/quantizes wall height; current policy snaps 2.58 -> 2.60
    assert abs(fp.H_e - 2.60) < 1e-9

    # axes dict shape
    assert set(fp.vertical_axes.keys()) == {"N", "S", "E", "W"}

    # z-axes include bounds
    assert fp.z_axes[0] <= fp.z_axes[-1]
    assert fp.z_axes[0] <= fp.z0 + EPS
    assert fp.z_axes[-1] >= fp.H_e - EPS

    # openings_final are consistent
    assert len(fp.openings_final) == 3
    for o in fp.openings_final:
        assert o.u0 <= o.u1
        assert o.z0 <= o.z1
