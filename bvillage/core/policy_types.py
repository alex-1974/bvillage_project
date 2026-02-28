# bvillage/core/policy_types.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple

Range2 = Tuple[float, float]


@dataclass(frozen=True, slots=True)
class RangeHardSpec:
    min_v: float
    max_v: float


@dataclass(frozen=True, slots=True)
class RangeSoftSpec:
    ideal: Range2
    allowed: Range2
    weight: float = 1.0


@dataclass(frozen=True, slots=True)
class ConstraintSpec:
    hard: RangeHardSpec | None
    soft: RangeSoftSpec | None
    unit: str = "m"
    code_prefix: str = "POL"


@dataclass(frozen=True, slots=True)
class FachwerkPolicySpec:
    # minimal subset that the fachwerk frameplan builder needs
    b_max: float
    default_jamb_t: float = 0.20


@dataclass(frozen=True, slots=True)
class ResolvedPolicy:
    schema: int
    # constraints by name (stable keys)
    constraints: Dict[str, ConstraintSpec]
    # domain inputs
    fachwerk: FachwerkPolicySpec
