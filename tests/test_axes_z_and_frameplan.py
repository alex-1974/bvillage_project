# tests/test_axes_z_and_frameplan.py

"""
tests.test_axes_z_and_frameplan
===============================

Covers:
- Z-axis generation: sortedness, inclusion of bounds and opening z-edges.
- Frameplan smoke test: wires openings->axes correctly.

Units: meters.
"""

from __future__ import annotations

from bvillage.domains.fachwerk.core.axes_z import compute_z_axes
from bvillage.domains.fachwerk.core.frameplan import build_frameplan, FramePolicy
from bvillage.domains.fachwerk.core.openings_norm import normalize_openings_from_plan

from conftest import make_structure, make_openings_plan, opening


def test_compute_z_axes_contains_bounds_and_opening_edges():
    structure = make_structure(L=10.0, W=4.0, z0=0.0, H_e=2.58)
    ops = make_openings_plan(
        opening(oid="Gate", typ="gate", wall_id="W_S_0", u0=-1.0, u1=1.0, z0=0.0, z1=2.2),
        opening(oid="Win", typ="window", wall_id="W_N_0", u0=2.0, u1=3.0, z0=0.9, z1=1.6),
    )
    openings_final = normalize_openings_from_plan(ops, default_jamb_thickness=0.2, width_type="axis")

    z_axes, z_clusters, z_log = compute_z_axes(
        z0=0.0,
        H_e=2.58,
        horizontal_axes_style=[0.0, 0.9, 1.6, 2.2, 2.58],
        z_merge_tol=1e-6,
        z_band_min=0.15,
        z_band_target_min=0.25,
        openings=list(openings_final),
    )

    assert z_axes == sorted(z_axes)
    assert 0.0 in z_axes
    assert 2.58 in z_axes
    assert 2.2 in z_axes
    assert 0.9 in z_axes
    assert 1.6 in z_axes
    assert isinstance(z_clusters, list)
    assert isinstance(z_log, list)


def test_build_frameplan_smoke_normalizes_and_repairs_height_and_generates_axes():
    """
    Contract:
    - FramePlan canonicalizes z0 to 0.0
    - FramePlan may repair/quantize H_e
    - Resulting H_e must equal top Z-axis
    - Axes must be sorted and span full height
    """
    structure = make_structure(L=12.0, W=6.0, z0=0.1, H_e=2.7)
    ops = make_openings_plan(
        opening(oid="Gate", typ="gate", wall_id="W_S_0", u0=-1.4, u1=1.4, z0=0.1, z1=2.2),
    )
    policy = FramePolicy(binder_max=1.4)

    fp = build_frameplan(
        structure=structure,
        openings=ops,
        policy=policy,
        seed=123,
    )

    # Footprint must pass through unchanged
    assert abs(fp.L - 12.0) < 1e-9
    assert abs(fp.W - 6.0) < 1e-9

    # z0 is canonicalized
    assert abs(fp.z0 - 0.0) < 1e-9

    # Height must be positive and within reasonable band
    assert 2.0 <= fp.H_e <= 3.0

    # Height must equal the top Z-axis
    assert abs(fp.H_e - fp.z_axes[-1]) < 1e-9

    # Z-axes must be sorted and span from z0 to H_e
    assert fp.z_axes == sorted(fp.z_axes)
    assert abs(fp.z_axes[0] - fp.z0) < 1e-9
    assert abs(fp.z_axes[-1] - fp.H_e) < 1e-9

    # All cardinal walls must be present
    assert set(fp.vertical_axes.keys()) == {"N", "S", "E", "W"}

    # Must generate at least bottom + top axis
    assert len(fp.z_axes) >= 2
