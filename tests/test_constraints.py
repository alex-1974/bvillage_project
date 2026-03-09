# tests/test_constraints.py

import math
from bvillage.core.model import Context
from bvillage.core.seed import Seed
from bvillage.core.constraints import (
    RangeHard, RangeSoft, CostProfile, eval_range, sample_soft
)

def _ctx(seed=123):
    return Context(
        seed=Seed(seed),
        epoch_band="late_medieval",
        region="north",
        settlement_type="village",
        wealth=0.6,
        archetype_id="FW-LH-ND",
    )

def test_hard_violation_emits_hard_issue():
    ctx = _ctx()
    ev = eval_range(
        ctx,
        name="fach_width",
        value=2.0,
        hard=RangeHard(0.0, 1.6),
        soft=None,
    )
    assert any(i.severity == "HARD" for i in ev.issues)

def test_soft_inside_ideal_zero_penalty():
    ctx = _ctx()
    profiles = (CostProfile(name="auth", mode="quadratic"),)
    soft = RangeSoft(ideal=(1.2, 1.5), allowed=(0.9, 1.6), weight=3.0)
    ev = eval_range(ctx, name="fach_width", value=1.35, soft=soft, profiles=profiles)
    assert ev.penalties["auth"] == 0.0
    assert len(ev.issues) == 0

def test_soft_inside_allowed_outside_ideal_has_penalty_no_issue():
    ctx = _ctx()
    profiles = (CostProfile(name="auth", mode="linear"),)
    soft = RangeSoft(ideal=(1.2, 1.5), allowed=(0.9, 1.6), weight=1.0)
    ev = eval_range(ctx, name="fach_width", value=1.55, soft=soft, profiles=profiles)
    assert ev.penalties["auth"] > 0.0
    assert all(i.severity != "SOFT" for i in ev.issues)

def test_soft_outside_allowed_emits_soft_issue_and_bigger_penalty():
    ctx = _ctx()
    profiles = (CostProfile(name="auth", mode="linear", outside_allowed_step=5.0),)
    soft = RangeSoft(ideal=(1.2, 1.5), allowed=(0.9, 1.6), weight=1.0)
    ev = eval_range(ctx, name="fach_width", value=0.8, soft=soft, profiles=profiles)
    assert any(i.severity == "SOFT" for i in ev.issues)
    assert ev.penalties["auth"] > 0.0

def test_sample_soft_is_deterministic():
    ctx1 = _ctx(seed=999)
    ctx2 = _ctx(seed=999)
    soft = RangeSoft(ideal=(0.95, 1.10), allowed=(0.85, 1.25), weight=1.0)
    v1 = sample_soft(ctx1, key="hall.wallN.brustriegel", soft=soft)
    v2 = sample_soft(ctx2, key="hall.wallN.brustriegel", soft=soft)
    assert math.isclose(v1, v2, rel_tol=0, abs_tol=0)
