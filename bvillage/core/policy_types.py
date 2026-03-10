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
class ResolvedPolicy:
    schema: int
    constraints: Dict[str, ConstraintSpec]
    domain: object

    @property
    def fachwerk(self) -> object:
        """
        Compatibility alias for the current timber-frame stack.

        WHY:
        The architecture is moving toward generic domain policy access
        (`resolved_policy.domain`), but parts of the active timber-frame
        pipeline still read `resolved_policy.fachwerk`.
        """
        return self.domain
