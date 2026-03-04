# bvillage/core/constraints.py

"""
bvillage.core.constraints
========================

Deterministic parameter ranges with Hard/Soft semantics and multi-profile cost scoring.

- Hard constraints: violation => HARD Issue
- Soft constraints: deviation => penalty score in one or more CostProfiles
  - outside allowed => SOFT Issue + stronger penalty

Core-only:
- no Blender imports
- deterministic sampling (seed + key)
- emits Issues + numeric penalties (per profile)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
import hashlib
from random import Random

from .hot_path import hot, hot_api

from .model import Context, Issue

__all__ = ['RangeHard', 'RangeSoft', 'CostProfile', 'ConstraintEval', 'eval_range', 'sample_soft', 'rng_for', 'penalty_soft']

Range2 = tuple[float, float]
PenaltyMode = Literal["linear", "quadratic", "hinge"]

@dataclass(frozen=True, slots=True)
class RangeHard:
    min_v: float
    max_v: float

    def contains(self, v: float) -> bool:
        return self.min_v <= v <= self.max_v

@dataclass(frozen=True, slots=True)
class RangeSoft:
    """
    Soft range with a preferred (ideal) band and an allowed band.
    """
    ideal: Range2
    allowed: Range2
    weight: float = 1.0

@dataclass(frozen=True, slots=True)
class CostProfile:
    """
    How penalties grow with deviation.

    mode:
      - linear:    w * d
      - quadratic: w * d^2  (strongly discourages near-limits; good for authenticity/risk)
      - hinge:     w * max(0, d - deadband) (ignore tiny deviations)
    """
    name: str
    mode: PenaltyMode = "quadratic"
    deadband: float = 0.0                # used by hinge
    outside_allowed_step: float = 2.0    # penalty multiplier when outside allowed

@dataclass(frozen=True, slots=True)
class ConstraintEval:
    value: float
    penalties: dict[str, float]
    issues: tuple[Issue, ...] = ()

_DEFAULT_PROFILE: tuple[CostProfile, ...] = (
    CostProfile(name="default", mode="quadratic"),
)

@hot
def _u01_from_u32(x: int) -> float:
    """Maps a uint32 to a uniform float in [0, 1)."""
    return (x & 0xFFFFFFFF) / 4294967296.0  # 2**32

# ----------------------------
# Deterministic RNG
# ----------------------------

@hot
def _stable_u32(seed: int, key: str) -> int:
    """
    Stable (process-independent) 32-bit hash from seed+key.
    Avoid Python's salted hash().
    """
    h = hashlib.blake2b(digest_size=8)
    h.update(str(seed).encode("utf-8"))
    h.update(b"|")
    h.update(key.encode("utf-8"))
    return int.from_bytes(h.digest()[:4], "little", signed=False)

def rng_for(ctx: Context, key: str) -> Random:
    """
    Deterministic RNG factory.

    Requires ctx.seed to be a Seed object.
    """
    return Random(int(ctx.seed.derive(key)))

# ----------------------------
# Scoring helpers
# ----------------------------

def _dist_outside(v: float, a: float, b: float) -> float:
    if v < a:
        return a - v
    if v > b:
        return v - b
    return 0.0

def _shape_cost(d: float, prof: CostProfile) -> float:
    if d <= 0.0:
        return 0.0
    if prof.mode == "linear":
        return d
    if prof.mode == "quadratic":
        return d * d
    # hinge
    dd = max(0.0, d - float(prof.deadband))
    return dd

# HOT PATH — may run many times per house; explodes with candidate sampling
@hot
def penalty_soft(v: float, soft: RangeSoft, prof: CostProfile) -> float:
    """
    Piecewise penalty:
      - inside ideal => 0
      - inside allowed but outside ideal => shaped cost to nearest ideal boundary
      - outside allowed => shaped cost to nearest allowed boundary, amplified
    """
    ia, ib = soft.ideal
    aa, ab = soft.allowed

    # In ideal: free
    if ia <= v <= ib:
        return 0.0

    w = soft.weight

    # Inside allowed: penalize distance to ideal band
    if aa <= v <= ab:
        d = _dist_outside(v, ia, ib)
        return w * _shape_cost(d, prof)

    # Outside allowed: penalize distance to allowed + amplify
    d = _dist_outside(v, aa, ab)
    return w * prof.outside_allowed_step * _shape_cost(d, prof)

# ----------------------------
# Public API
# ----------------------------

# HOT PATH — may run many times per house; explodes with candidate sampling
@hot_api
def eval_range(
    ctx: Context,
    *,
    name: str,
    value: float,
    hard: RangeHard | None = None,
    soft: RangeSoft | None = None,
    profiles: tuple[CostProfile, ...] | None = None,
    unit: str = "m",
    code_prefix: str = "C",
) -> ConstraintEval:
    """
    Evaluate a value against hard/soft ranges.
    Returns Issues plus penalties per profile name.

    - Hard violation => HARD Issue
    - Soft outside allowed => SOFT Issue
    - Penalties computed for each profile independently.
    """
    if profiles is None:
        profiles = _DEFAULT_PROFILE

    issues: list[Issue] = []
    #penalties: dict[str, float] = {p.name: 0.0 for p in profiles}
    if len(profiles) == 1:
        p = profiles[0]
        penalties = {p.name: penalty_soft(value, soft, p)} if soft else {p.name: 0.0}
    else:
        penalties = {p.name: 0.0 for p in profiles}
    
    # HARD
    if hard is not None and not hard.contains(value):
        issues.append(
            Issue(
                code=f"H_{code_prefix}_{name.upper()}_HARD",
                severity="HARD",
                message=(
                    f"{name}={value:.3f}{unit} violates hard range "
                    f"[{hard.min_v:.3f},{hard.max_v:.3f}]{unit}"
                ),
                related_ids=(),
                suggested_repairs=(f"R_ADJUST_{name.upper()}",),
            )
        )

    # SOFT penalties + optional SOFT issue if outside allowed
    if soft is not None:
        for prof in profiles:
            penalties[prof.name] += penalty_soft(value, soft, prof)

        aa, ab = soft.allowed
        if not (aa <= value <= ab):
            issues.append(
                Issue(
                    code=f"S_{code_prefix}_{name.upper()}_SOFT",
                    severity="SOFT",
                    message=(
                        f"{name}={value:.3f}{unit} outside allowed soft range "
                        f"[{aa:.3f},{ab:.3f}]{unit}"
                    ),
                    related_ids=(),
                    suggested_repairs=(f"R_ADJUST_{name.upper()}",),
                )
            )

    return ConstraintEval(value=value, penalties=penalties, issues=tuple(issues))

# WHY: duplicate _u01_from_u32 removed — canonical definition with docstring is above.

# HOT PATH — may run many times per house; explodes with candidate sampling
@hot
def sample_soft(
    ctx: Context,
    *,
    key: str,
    soft: RangeSoft,
    prefer_ideal_prob: float = 0.80,
) -> float:
    """
    Deterministically sample a value:
      - with probability prefer_ideal_prob from ideal band
      - else from allowed band

    HOT PATH:
      - no Random() construction
      - no allocations
      - stable across processes
    """
    base = int(ctx.seed.derive(key))

    # Draw 1: choose band
    u_choice = _u01_from_u32(_stable_u32(base, "choose"))
    band = soft.ideal if (u_choice < prefer_ideal_prob) else soft.allowed
    a, b = band

    # Draw 2: uniform inside band
    u = _u01_from_u32(_stable_u32(base, "u"))
    return a + (b - a) * u
