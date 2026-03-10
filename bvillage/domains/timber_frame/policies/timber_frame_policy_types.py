from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True, slots=True)
class TimberFramePolicySpec:

    binder_max: float

    bay_width: float = 3.645
    building_width: float = 7.2
    plate_height: float = 2.6

    bay_count: int = 5
    gable_mode: str = "end_frame"

    default_jamb_thickness: float = 0.20

    post_section_width: float = 0.20
    post_section_depth: float = 0.20

    plate_section_width: float = 0.18
    plate_section_depth: float = 0.18

    opening_jamb_width: float = 0.18
    opening_jamb_depth: float = 0.18

    braces_enable: bool = True
    brace_section_width: float = 0.12
    brace_section_depth: float = 0.12

    brace_min_cell_width: float = 0.80
    brace_min_cell_height: float = 0.80

    target_gefach_width: float = 1.35
    target_gefach_jitter: float = 0.10

    z_merge_tol: float = 0.01

    roof_pitch_deg: float = 50.0

    post_section: Tuple[float, float] = (0.20, 0.20)

    default_infill_material_role: str = "INFILL_BRICK"
