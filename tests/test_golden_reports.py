# tests/test_golden_reports.py

"""
tests.test_golden_reports
=========================

Golden-ish report tests.

Philosophy
----------
We DO NOT snapshot entire reports byte-for-byte (too brittle).
We assert the presence of essential, stable lines/sections.

This protects:
- report structure (headers, key sections)
- critical numeric formatting (dims, axes output basics)
- regression of accidental None-handling / missing sections
"""

from __future__ import annotations

from bvillage.core.model import Context
from bvillage.core.report import report_plans
from bvillage.domains.fachwerk.core.frameplan import build_frameplan, FramePolicy, frameplan_report

from conftest import make_structure, make_openings_plan, opening
from bvillage.core.seed import Seed

def test_frameplan_report_contains_core_sections_and_expected_openings():
    structure = make_structure(L=19.9, W=6.9, z0=0.0, H_e=2.58)
    ops = make_openings_plan(
        opening(oid="Op01", typ="door", wall_id="W_S_0", u0=-4.3, u1=-1.3, z0=0.0, z1=2.2),
        opening(oid="Op02", typ="window", wall_id="W_S_0", u0=3.0, u1=4.2, z0=0.9, z1=1.6),
        opening(oid="Op03", typ="window", wall_id="W_N_0", u0=1.6, u1=2.8, z0=0.9, z1=1.6),
    )
    policy = FramePolicy(binder_max=1.4, style_z_levels=[0.0, 0.9, 1.6, 2.2, 2.58])

    fp = build_frameplan(
        structure=structure,
        openings=ops,
        policy=policy,
        seed=123,
    )
    rep = frameplan_report(fp)

    # Stable header + dims signature
    assert "========== PLANNER REPORT ==========" in rep
    assert "[Dims] L=19.900 W=6.900 H_e=2.600 z0=0.000" in rep

    # Z axes header exists
    assert "[Z Axes]" in rep

    # Openings section lists expected ids
    assert "[Openings Final] n=3" in rep
    assert "Op01" in rep
    assert "Op02" in rep
    assert "Op03" in rep

    # Axes summary exists
    assert "[Axes Summary]" in rep
    assert "Wall N:" in rep
    assert "Wall S:" in rep
    
    assert "[Z Repair Log]" in rep
    assert "drop z=2.580" in rep


def test_core_report_contains_sections_and_formats_dims_in_meters():
    ctx = Context(
        seed=Seed(42),
        epoch_band="late_medieval",
        region="north",
        settlement_type="village",
        wealth=0.6,
        house_type="fachwerkhaus.hallenhaus",
    )

    structure = make_structure(L=10.0, W=4.0, z0=0.0, H_e=2.5)
    rep = report_plans(ctx, structure, interior=None, openings=None, issues=None, score=None)

    # Headers
    assert "========== BVILLAGE REPORT ==========" in rep
    assert "[Context]" in rep
    assert "[Dims]" in rep

    # Units formatting (meters)
    assert "L=10.000 m" in rep
    assert "W=4.000 m" in rep

    # Grid/Walls sections
    assert "[Grid]" in rep
    assert "[Walls]" in rep

    # Must not crash / emit "Issues" if issues=None
    assert "[Issues]" not in rep
