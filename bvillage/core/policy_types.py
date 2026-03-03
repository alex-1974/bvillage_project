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
    """
    Domain inputs for the Fachwerk stack.

    All defaults must be policy-level defaults.
    Blender must not invent structural/material defaults.
    """

    # --- structural rhythm ---
    binder_max: float

    # --- openings normalization ---
    default_jamb_thickness: float = 0.20

    # --- member profile defaults ---
    post_section_width: float = 0.20
    post_section_depth: float = 0.20

    plate_section_width: float = 0.18
    plate_section_depth: float = 0.18

    opening_jamb_width: float = 0.18
    opening_jamb_depth: float = 0.18

    # --- braces ---
    braces_enable: bool = True
    brace_section_width: float = 0.12
    brace_section_depth: float = 0.12
    brace_min_cell_width: float = 0.80
    brace_min_cell_height: float = 0.80

    # --- historical gefach targeting ---
    target_gefach_width: float = 1.35
    target_gefach_jitter: float = 0.10

    # --- numerics ---
    z_merge_tol: float = 0.01

    # --- renderer-facing (policy-driven) ---
    roof_pitch_deg: float = 50.0

    # fallback member profile tuple (used by Blender mapping only)
    post_section: Tuple[float, float] = (0.20, 0.20)

    # NEW: infill material default (policy-driven, not Blender literal)
    default_infill_material_role: str = "INFILL_BRICK"

@dataclass(frozen=True, slots=True)
class ResolvedPolicy:
    schema: int
    # constraints by name (stable keys)
    constraints: Dict[str, ConstraintSpec]
    # domain inputs
    fachwerk: FachwerkPolicySpec
