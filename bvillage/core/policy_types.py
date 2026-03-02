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

    Defaults mirror current bvillage.domains.fachwerk.core.frameplan.FramePolicy defaults
    (plus renderer-facing fields that are currently defaulted in the Blender layer).
    """

    # --- structural rhythm / subdivision ---
    binder_max: float

    # --- openings normalization (domain) ---
    default_jamb_thickness: float = 0.20  # m  :contentReference[oaicite:3]{index=3}

    # --- member profile defaults (domain) ---
    post_section_width: float = 0.20  # m  :contentReference[oaicite:4]{index=4}
    post_section_depth: float = 0.20  # m  :contentReference[oaicite:5]{index=5}

    plate_section_width: float = 0.18  # m  :contentReference[oaicite:6]{index=6}
    plate_section_depth: float = 0.18  # m  (matches pattern; depth used by members) :contentReference[oaicite:7]{index=7}

    opening_jamb_width: float = 0.18  # m  :contentReference[oaicite:8]{index=8}
    opening_jamb_depth: float = 0.18  # m  :contentReference[oaicite:9]{index=9}

    # --- braces (domain) ---
    braces_enable: bool = True  # :contentReference[oaicite:10]{index=10}
    brace_section_width: float = 0.12  # m :contentReference[oaicite:11]{index=11}
    brace_section_depth: float = 0.12  # m :contentReference[oaicite:12]{index=12}
    brace_min_cell_width: float = 0.80  # m :contentReference[oaicite:13]{index=13}
    brace_min_cell_height: float = 0.80  # m :contentReference[oaicite:14]{index=14}

    # --- historical gefach targeting (domain) ---
    target_gefach_width: float = 1.35  # m :contentReference[oaicite:15]{index=15}
    target_gefach_jitter: float = 0.10  # m :contentReference[oaicite:16]{index=16}

    # --- numerics / merge thresholds (domain) ---
    z_merge_tol: float = 0.01  # m (FramePolicy has z_merge_tol; used in normalization/merging) :contentReference[oaicite:17]{index=17}

    # --- renderer-facing (currently defaulted in Blender layer; must become policy-driven) ---
    roof_pitch_deg: float = 50.0  # deg (Blender roof currently uses defaults; move policy-side)
    # Fallback profile tuple for Blender mapping when a member lacks explicit "profile"
    post_section: Tuple[float, float] = (0.20, 0.20)  # (w, d) meters


@dataclass(frozen=True, slots=True)
class ResolvedPolicy:
    schema: int
    # constraints by name (stable keys)
    constraints: Dict[str, ConstraintSpec]
    # domain inputs
    fachwerk: FachwerkPolicySpec
