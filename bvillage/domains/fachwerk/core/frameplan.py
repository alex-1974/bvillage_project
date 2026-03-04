# bvillage/domains/fachwerk/core/frameplan.py

"""
bvillage.domains.fachwerk.core.frameplan
=======================================

Build a Fachwerk frameplan artifact.

Units: meters.

This module is pure planning/data:
- It computes normalized openings, vertical axes (u), and z-axes.
- It returns a FramePlan dataclass and dict payload for notes storage.

Schema
------
frameplan_to_dict() emits a stable schema used by Blender builders.

As of schema_version=2, the artifact contains:
- "members": structural truth (posts/rails/braces/infills)
  Blender must build members, not derive structural geometry from axes.

Notes
-----
- axes_u / axes_z remain as planning geometry and for contract/validation.
- members.* are the canonical "what to build" lists.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Tuple
from random import Random

from bvillage.core.geom_eps import EPS_MERGE
from bvillage.core.model import StructurePlan
from bvillage.domains.fachwerk.core.openings_norm import (
    OpeningFinal,
    normalize_openings_from_plan,
)
from bvillage.domains.fachwerk.core.axes_u import compute_vertical_axes
from bvillage.domains.fachwerk.core.axes_z import compute_z_axes
from bvillage.domains.fachwerk.core.wall_tags import compute_wall_tags, suggest_front_wall


WidthType = Literal["axis", "clear"]


@dataclass(frozen=True, slots=True)
class FramePolicy:
    """
    Fachwerk engine policy parameters.

    Units: meters.
    """
    binder_max: float
    default_jamb_thickness: float = 0.20
    style_z_levels: List[float] = None  # type: ignore[assignment]

    # z-axis post-processing parameters (merge, min band thickness, etc.)
    z_merge_tol: float = EPS_MERGE
    z_band_min: float = 0.15
    z_band_target_min: float = 0.25

    # How to interpret opening width (axis vs clear)
    width_type: WidthType = "axis"

    # --- members policy knobs ---
    post_section_width: float = 0.20
    post_section_depth: float = 0.20

    plate_section_width: float = 0.18
    plate_section_depth: float = 0.18

    opening_jamb_width: float = 0.18
    opening_jamb_depth: float = 0.18

    gate_lintel_width: float = 0.20
    gate_lintel_depth: float = 0.20
    window_lintel_width: float = 0.16
    window_lintel_depth: float = 0.18
    window_sill_width: float = 0.16
    window_sill_depth: float = 0.18

    braces_enable: bool = True
    brace_section_width: float = 0.12
    brace_section_depth: float = 0.12
    brace_min_cell_width: float = 0.80
    brace_min_cell_height: float = 0.80
    
    # --- historical gefach targeting ---
    target_gefach_width: float = 1.35
    target_gefach_jitter: float = 0.10

    def __post_init__(self):
        if self.style_z_levels is None:
            object.__setattr__(self, "style_z_levels", [0.0, 0.9, 1.6, 2.2])


@dataclass(frozen=True, slots=True)
class FramePlan:
    """
    Derived planning artifact for the Fachwerk frame build.

    Fields:
    - L/W: footprint dims
    - H_e: wall/eaves height
    - z0: ground base
    """
    L: float
    W: float
    H_e: float
    z0: float

    openings_final: List[OpeningFinal]

    vertical_axes: Dict[str, Dict[str, List[float]]]
    z_axes: List[float]
    z_clusters: List[List[float]]
    z_repair_log: List[str]

    wall_tags: Dict[str, List[str]]
    front_wall: str

    policy: Optional[FramePolicy] = None


def _infer_wall_height(structure: StructurePlan) -> Tuple[float, float]:
    """
    Infer z0 and H_e from structure plan.
    Falls back to conservative defaults if not present.
    """
    z0 = 0.0
    H_e = 2.6

    # Defensive: not all structure plans may carry these yet
    try:
        if getattr(structure, "z0", None) is not None:
            z0 = float(structure.z0)
    except Exception:
        pass

    try:
        if getattr(structure, "eaves_height", None) is not None:
            H_e = float(structure.eaves_height)
        elif getattr(structure, "wall_height", None) is not None:
            H_e = float(structure.wall_height)
    except Exception:
        pass

    return z0, H_e

def _binder_u_from_grid(structure: StructurePlan) -> List[float]:
    """
    Convert grid axes_u (0..L) to wall-u coordinates (-L/2..+L/2).
    Only meaningful for N/S walls.
    """
    L = float(structure.footprint.length)
    halfL = 0.5 * L

    grid = getattr(structure, "grid", None)
    axes_u = getattr(grid, "axes_u", None) if grid is not None else None
    if not isinstance(axes_u, (list, tuple)) or len(axes_u) < 2:
        return []

    # convert x -> u
    out = [float(x) - halfL for x in axes_u]

    # drop endpoints (corners) because they're already in primary axes
    eps = 1e-6
    out = [u for u in out if (u > -halfL + eps) and (u < +halfL - eps)]
    return out

def build_frameplan(
    *,
    structure: StructurePlan,
    openings: Any,
    policy: FramePolicy,
    seed: int,
) -> FramePlan:
    """
    Build frameplan artifact for the given structure and openings.

    Deterministic:
      - Any micro-variation is controlled via the provided `seed`.
    """
    L = float(structure.footprint.length)
    W = float(structure.footprint.width)

    z0, H_e = _infer_wall_height(structure)

    openings_final = normalize_openings_from_plan(
        openings,
        default_jamb_thickness=float(policy.default_jamb_thickness),
        width_type=policy.width_type,
    )

    # 1) Base vertical axes (primary + opening anchors)
    vertical_axes = compute_vertical_axes(
        L=L,
        W=W,
        binder_max=float(policy.binder_max),
        openings=list(openings_final),
    )

    # 2) Binder axes from planner grid (optional)
    binder_u = _binder_u_from_grid(structure)

    # 3) Secondary axis adjustment (Hallenhaus MVP), deterministic via `seed`
    vertical_axes = _adjust_secondary_axes_by_target(
        vertical_axes,
        target_width=float(policy.target_gefach_width),
        jitter=float(policy.target_gefach_jitter),
        binder_u=binder_u,
        seed=int(seed),
    )

    # 4) Z axes
    z_axes, z_clusters, z_repair_log = compute_z_axes(
        z0=z0,
        H_e=H_e,
        style_z_levels=list(policy.style_z_levels),
        z_merge_tol=float(policy.z_merge_tol),
        z_band_min=float(policy.z_band_min),
        z_band_target_min=float(policy.z_band_target_min),
        openings=list(openings_final),
    )

    wall_tags = compute_wall_tags(openings_final)
    front_wall = suggest_front_wall(wall_tags)

    return FramePlan(
        L=L,
        W=W,
        H_e=H_e,
        z0=z0,
        openings_final=list(openings_final),
        vertical_axes=vertical_axes,
        z_axes=z_axes,
        z_clusters=z_clusters,
        z_repair_log=z_repair_log,
        wall_tags=wall_tags,
        front_wall=front_wall,
        policy=policy,
    )

def _adjust_secondary_axes_by_target(
    axes: Dict[str, Dict[str, List[float]]],
    *,
    target_width: float,
    jitter: float,
    binder_u: List[float],
    seed: int,
    merge_tol: float = 1e-4,
) -> Dict[str, Dict[str, List[float]]]:

    """
    Hallenhaus MVP: make N/S wall bay segmentation respect binder axes.

    Anchors for segmentation on N/S:
      - primary axes (usually corners)
      - opening axes (opening edges)
      - binder axes (grid axes_u mapped to u)

    Then subdivide spans between anchors to approximate target_width.
    """
    rng = Random(seed)
     
    def _merge_axis(vals: List[float]) -> List[float]:
        if not vals:
            return []
        vals = sorted(vals)
        out = [vals[0]]
        for v in vals[1:]:
            if abs(v - out[-1]) <= merge_tol:
                continue
            out.append(v)
        return out

    new_axes: Dict[str, Dict[str, List[float]]] = {}

    for wall, data in axes.items():
        primary = list(data.get("primary", []))
        opening = list(data.get("opening", []))

        # only adjust long walls
        if wall not in ("N", "S"):
            new_axes[wall] = data
            continue

        # anchors = primary + opening + binder
        anchors = _merge_axis(primary + opening + list(binder_u))

        # keep originals stable
        adjusted = list(anchors)

        for i in range(len(anchors) - 1):
            u0 = anchors[i]
            u1 = anchors[i + 1]
            span = u1 - u0
            if span <= target_width:
                continue

            # historically moderated subdivision per binder bay

            # small bays → no additional post
            if span <= 1.6:
                continue

            # medium binder bay → one middle post
            elif span <= 2.8:
                n = 2

            # very large bay (rare in hallenhaus) → max two posts
            else:
                n = 3

            for k in range(1, n):
                pos = u0 + (span * k / n)

                if jitter > 0.0:
                    pos += (rng.random() - 0.5) * 2.0 * jitter

                adjusted.append(pos)

        adjusted = _merge_axis(adjusted)

        new_axes[wall] = {
            "primary": primary,
            "opening": opening,
            "secondary": sorted(set(adjusted) - set(primary) - set(opening)),
            "all": adjusted,
        }

    return new_axes

def frameplan_to_dict(fp: FramePlan) -> Dict[str, Any]:
    """
    Convert FramePlan to a JSON-like dict for notes storage (stable schema).

    schema_version=3: members-first + ontology TIDs.
    Structural semantics use `tid` (ontology).
    """
    from bvillage.core.ontology.structural_terms import (
        POST_PRIMARY,
        POST_JAMB,
        BEAM_EAVES_PLATE,
        BEAM_LINTEL,
        BEAM_WINDOW_SILL,
        BRACE_DIAGONAL,
        INFILL_CELL,
    )

    pol = fp.policy
    if pol is None:
        pol = FramePolicy(binder_max=0.0)

    # ------------------------------------------------------------
    # Infer "z_plate" as the highest z-axis below H_e (as in v2 file)
    # ------------------------------------------------------------
    eps = 1e-6
    try:
        z_plate = max(z for z in fp.z_axes if float(z) < float(fp.H_e) - eps)
    except Exception:
        z_plate = float(fp.H_e)

    # ------------------------------------------------------------
    # 1) Primary posts
    # ------------------------------------------------------------
    primary_posts: List[Dict[str, Any]] = []
    for wall in ("N", "S", "E", "W"):
        w = fp.vertical_axes.get(wall, {})
        for u in w.get("primary", []):
            primary_posts.append(
                {
                    "tid": POST_PRIMARY,
                    # legacy/material only (do NOT drive geometry by role)
                    "role": "PRIMARY_POST",
                    "wall": wall,
                    "u": float(u),
                    "z0": float(fp.z0),
                    "z1": float(fp.H_e),
                    "profile": {"w": float(pol.post_section_width), "d": float(pol.post_section_depth)},
                    "material_id": "timber.oak",
                }
            )

    # ------------------------------------------------------------
    # 2) Opening members: jambs + lintel + optional sill
    # ------------------------------------------------------------
    opening_posts: List[Dict[str, Any]] = []
    opening_rails: List[Dict[str, Any]] = []
    for o in fp.openings_final:
        opening_posts.append(
            {
                "tid": POST_JAMB,
                "role": "OPENING_JAMB_L",  # legacy/material only
                "side": "L",
                "wall": o.wall,
                "u": float(o.u0),
                "z0": float(o.z0),
                "z1": float(o.z1),
                "profile": {"w": float(pol.opening_jamb_width), "d": float(pol.opening_jamb_depth)},
                "opening": o.name,
                "material_id": "timber.oak",
            }
        )
        opening_posts.append(
            {
                "tid": POST_JAMB,
                "role": "OPENING_JAMB_R",
                "side": "R",
                "wall": o.wall,
                "u": float(o.u1),
                "z0": float(o.z0),
                "z1": float(o.z1),
                "profile": {"w": float(pol.opening_jamb_width), "d": float(pol.opening_jamb_depth)},
                "opening": o.name,
                "material_id": "timber.oak",
            }
        )

        # lintel
        opening_rails.append(
            {
                "tid": BEAM_LINTEL,
                "role": "OPENING_LINTEL",
                "wall": o.wall,
                "u0": float(o.u0),
                "u1": float(o.u1),
                "z": float(o.z1),
                "profile": {"w": float(pol.window_lintel_width), "d": float(pol.window_lintel_depth)},
                "opening": o.name,
                "material_id": "timber.oak",
            }
        )

        # sill only for windows
        if o.typ == "window":
            opening_rails.append(
                {
                    "tid": BEAM_WINDOW_SILL,
                    "role": "OPENING_SILL",
                    "wall": o.wall,
                    "u0": float(o.u0),
                    "u1": float(o.u1),
                    "z": float(o.z0),
                    "profile": {"w": float(pol.window_sill_width), "d": float(pol.window_sill_depth)},
                    "opening": o.name,
                    "material_id": "timber.oak",
                }
            )

    # ------------------------------------------------------------
    # 3) Eaves plates (N/S in current MVP)
    # ------------------------------------------------------------
    plate_rails: List[Dict[str, Any]] = []
    for wall in ("S", "N"):
        w = fp.vertical_axes.get(wall, {})
        prim = w.get("primary", [])
        if not prim:
            continue
        u0 = float(min(prim))
        u1 = float(max(prim))
        plate_rails.append(
            {
                "tid": BEAM_EAVES_PLATE,
                "role": f"EAVES_PLATE_{wall}",  # legacy/material only
                "wall": wall,
                "u0": u0,
                "u1": u1,
                "z": float(z_plate),
                "profile": {"w": float(pol.plate_section_width), "d": float(pol.plate_section_depth)},
                "material_id": "timber.oak",
            }
        )

    # ------------------------------------------------------------
    # 4) Infills (simple between primary posts, up to z_plate)
    # ------------------------------------------------------------
    infills: List[Dict[str, Any]] = []
    for wall in ("N", "S", "E", "W"):
        w = fp.vertical_axes.get(wall, {})
        prim = list(w.get("primary", []))
        if len(prim) < 2:
            continue
        prim.sort()
        for i in range(len(prim) - 1):
            infills.append(
                {
                    "tid": INFILL_CELL,
                    "role": "INFILL_CELL",  # will be rewritten to material-role in infills builder
                    "wall": wall,
                    "u0": float(prim[i]),
                    "u1": float(prim[i + 1]),
                    "z0": float(fp.z0),
                    "z1": float(z_plate),
                    "material_id": "mortar.lime_weak",
                }
            )

    # ------------------------------------------------------------
    # 5) Braces (keep existing if already present; otherwise empty)
    # ------------------------------------------------------------
    braces: List[Dict[str, Any]] = []
    for b in getattr(fp, "braces", []) or []:
        if not isinstance(b, dict):
            continue
        mm = dict(b)
        if "tid" not in mm:
            mm["tid"] = BRACE_DIAGONAL
        braces.append(mm)

    # ------------------------------------------------------------
    # Output
    # ------------------------------------------------------------
    out: Dict[str, Any] = {
        "schema_version": 3,
        "basis": {
            # Your current file already stores axes_u in the payload; basis is helpful for builders.
            "x_min": 0.0,
            "x_max": float(fp.L),
            "center_x": 0.5 * float(fp.L),
            "halfW": 0.5 * float(fp.W),
        },
        "openings": [
            {
                "name": o.name,
                "wall": o.wall,
                "typ": o.typ,
                "u0": float(o.u0),
                "u1": float(o.u1),
                "z0": float(o.z0),
                "z1": float(o.z1),
            }
            for o in fp.openings_final
        ],
        "axes_u": fp.vertical_axes,
        "axes_z": list(fp.z_axes),
        "members": {
            "posts": primary_posts + opening_posts,
            "rails": plate_rails + opening_rails,
            "braces": braces,
            "infills": infills,
        },
    }
    return out


def normalize_frameplan_dict(fp: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize frameplan dict for downstream builders.

    For schema_version >= 3:
      - members.* must exist and be lists
      - every member must have a valid 'tid' (no inference from role)
    """
    from bvillage.core.ontology.structural_terms import VALID_TIDS

    if not isinstance(fp, dict):
        raise TypeError("frameplan must be a dict")

    out = dict(fp)

    sv = out.get("schema_version", 0)
    try:
        sv_i = int(sv)
    except Exception:
        sv_i = 0
    out["schema_version"] = sv_i

    if "axes_u" not in out:
        out["axes_u"] = {}
    if "axes_z" not in out:
        out["axes_z"] = []

    members = out.get("members")
    if not isinstance(members, dict):
        members = {}
    out["members"] = members

    for k in ("posts", "rails", "braces", "infills"):
        arr = members.get(k)
        if not isinstance(arr, list):
            members[k] = []
        else:
            members[k] = [m for m in arr if isinstance(m, dict)]

    if sv_i >= 3:
        for k in ("posts", "rails", "braces", "infills"):
            for i, m in enumerate(members[k]):
                tid = m.get("tid")
                if not isinstance(tid, str) or not tid:
                    raise ValueError(f"normalize_frameplan_dict: missing required 'tid' in members.{k}[{i}]")
                if tid not in VALID_TIDS:
                    raise ValueError(f"normalize_frameplan_dict: unknown tid '{tid}' in members.{k}[{i}]")

    return out

def frameplan_report(fp: FramePlan) -> str:
    """
    Pretty report for logs / console.

    Keep stable-ish formatting (golden logs).
    """
    lines: List[str] = []
    lines.append("========== PLANNER REPORT ==========")
    lines.append(f"[Dims] L={fp.L:.3f} W={fp.W:.3f} H_e={fp.H_e:.3f} z0={fp.z0:.3f}")
    lines.append("[Z Axes] " + ", ".join(f"{float(z):.3f}" for z in fp.z_axes))

    lines.append(f"[Openings Final] n={len(fp.openings_final)}")
    for o in fp.openings_final:
        lines.append(
            f"  {o.name} {o.typ:<6} wall={o.wall} "
            f"u=[{o.u0:+.3f},{o.u1:+.3f}] (range={o.width_range:.3f} clear={o.width_clear:.3f}) "
            f"z=[{o.z0:.3f},{o.z1:.3f}]"
        )

    lines.append("[Axes Summary]")
    for wall in ("N", "S", "E", "W"):
        w = fp.vertical_axes.get(wall, {})
        primary = w.get("primary", []) or []
        opening = w.get("opening", []) or []
        secondary = w.get("secondary", []) or []
        all_u = w.get("all", []) or []
        lines.append(
            f"  Wall {wall}: primary={len(primary)} opening={len(opening)} secondary={len(secondary)} all={len(all_u)}"
        )

    lines.append(f"[Front Wall] {fp.front_wall}")

    if fp.z_repair_log:
        lines.append("[Z Repair Log]")
        for msg in fp.z_repair_log:
            lines.append(f"  - {msg}")

    return "\n".join(lines)
