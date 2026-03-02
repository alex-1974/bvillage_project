# bvillage/core/quality/physical_plausibility_validator.py

"""
PhysicalPlausibilityValidator (PPV)
===================================

Purpose
-------
A deterministic, conservative plausibility gate for "building physics" with an MVP
focus on structural mechanics. It is NOT a full engineering verification. It does
not repair geometry. It only emits Issues + metrics.

Key design principles
---------------------
1) Timeless physics layer:
   - independent of epoch/region/culture
   - checks universal mechanics (bending/deflection/shear/buckling/bearing)

2) Historical construction behavior is NOT here:
   - conservative sizing, redundancy preference, "fear factor" belongs to a separate
     ConstructionCulturePolicy / ConstructionCultureValidator.

3) Works with domain artifacts when available:
   - if a domain provides a frame/structure plan in notes, PPV uses it.
   - otherwise PPV can still run limited sanity checks (and will warn).

Expected integrations
---------------------
- Domains should put structural members into notes, e.g.
  notes["domains"][domain_id]["frameplan"]["members"] = [ ... ]
  members should include span, section, role, and material_id (or defaultable).

- Materials come from bvillage.core.materials.material_registry (MaterialClass).
  Rendering params are irrelevant to PPV; PPV uses physical strengths.

Outputs
-------
- PhysicalPlausibilityReport with list[Issue], metrics, optional per_member results.

MVP Checks included
-------------------
- GeometrySanityCheck
- StructuralBeamCheck (bending + deflection + optional shear)
- BearingCheck (bearing stress + minimum bearing length)
- PostSlendernessCheck (warning-only slenderness heuristic)

Future checks (plugins)
-----------------------
- Daylight / ventilation / thermal heuristics, climate-specific load models, etc.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

__all__ = ['run_ppv', 'extract_members_from_notes', 'Issue', 'PhysicsPolicy', 'PhysicalPlausibilityReport', 'StructuralMember']

# ---- Optional import: Material registry (keep soft dependency friendly) ----
try:
    from bvillage.core.materials.material_registry import MATERIALS, MaterialClass
except Exception:  # pragma: no cover
    MATERIALS = {}
    MaterialClass = Any  # type: ignore

# =============================================================================
# Public data structures
# =============================================================================

@dataclass(frozen=True, slots=True)
class Issue:
    code: str                # e.g. "H_PHYS_BEAM_BENDING_FAIL"
    severity: str            # "H" (hard), "S" (soft), "G" (guidance)
    message: str
    member_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True, slots=True)
class PhysicsPolicy:
    # Serviceability limits (deflection)
    deflection_limit_ratio_floor: float = 250.0   # L/250
    deflection_limit_ratio_roof: float = 200.0    # L/200

    # Utilization thresholds (stress/allowable)
    utilization_warn: float = 0.80
    utilization_fail: float = 1.00

    # Conservative load presets (kN/m²) — MVP
    g_dead_kN_m2_roof: float = 0.8
    q_snow_kN_m2: float = 0.75
    g_dead_kN_m2_floor: float = 0.5
    q_live_kN_m2_floor: float = 1.5

    # Timber / generic fallback material values (N/mm², density in kg/m³)
    default_E_N_mm2: float = 11000.0
    default_fb_allow_N_mm2: float = 10.0
    default_fv_allow_N_mm2: float = 1.0
    default_fc90_allow_N_mm2: float = 2.0
    default_density_kg_m3: float = 500.0

    # Bearing / geometry sanity
    min_bearing_len_mm: float = 40.0
    min_member_thickness_mm: float = 60.0

    # Slenderness heuristic thresholds
    slenderness_warn: float = 120.0
    slenderness_fail: float = 200.0  # hard-fail only for absurd cases in MVP

    # Load model fallback tributary width (m) if unknown
    default_tributary_width_m: float = 1.0

@dataclass(slots=True)
class PhysicalPlausibilityReport:
    issues: list[Issue]
    metrics: dict[str, float] = field(default_factory=dict)
    per_member: dict[str, dict[str, Any]] = field(default_factory=dict)

    def has_hard_fail(self) -> bool:
        return any(i.severity == "H" for i in self.issues)

# =============================================================================
# Internal member abstraction (adapter-friendly)
# =============================================================================

@dataclass(frozen=True, slots=True)
class StructuralMember:
    """
    A minimal structural member record PPV can evaluate.

    Units:
    - span_mm: mm
    - section_width_mm/section_height_mm: mm (rectangular section assumption in MVP)
    - bearing_len_mm: mm (if member sits on support)
    - tributary_width_m: meters (how much area contributes to this member)
    """
    id: str
    role: str  # "beam" | "purlin" | "joist" | "post" | "rafter" | ...
    span_mm: float
    section_width_mm: float
    section_height_mm: float

    material_id: str | None = None

    # load context
    usage: str = "roof"  # "roof" | "floor" | "unknown"
    tributary_width_m: float | None = None

    # bearing/support info (optional)
    bearing_len_mm: float | None = None  # contact length at support

    # allow attaching raw domain data for debugging
    raw: dict[str, Any] = field(default_factory=dict)

# =============================================================================
# Check plugin interface
# =============================================================================

class PhysicalCheck(Protocol):
    name: str
    def run(
        self,
        ctx: Any,
        structure: Any,
        pol: PhysicsPolicy,
        members: list[StructuralMember],
    ) -> tuple[list[Issue], dict[str, float], dict[str, dict[str, Any]]]:
        ...

# =============================================================================
# Public API
# =============================================================================

def run_physical_plausibility(
    ctx: Any,
    structure: Any,
    *,
    policy: PhysicsPolicy | None = None,
    domain_id: str | None = None,
) -> PhysicalPlausibilityReport:
    """
    Run PPV for a given structure.

    Parameters
    ----------
    ctx: any
        Your generation context (style/climate presets may live here).
    structure: any
        Your structure plan object (expected to carry notes with domain artifacts).
    policy: PhysicsPolicy | None
        Optional override. If None, defaults are used.
    domain_id: str | None
        If set, attempt to read members from notes["domains"][domain_id].
        If None, PPV tries to discover a single domain artifact if possible.

    Returns
    -------
    PhysicalPlausibilityReport
    """
    pol = policy or PhysicsPolicy()

    members, discovery_issues = _extract_members(structure, pol, domain_id=domain_id)
    issues: list[Issue] = list(discovery_issues)

    checks: list[PhysicalCheck] = [
        GeometrySanityCheck(),
        StructuralBeamCheck(),
        BearingCheck(),
        PostSlendernessCheck(),
    ]

    metrics: dict[str, float] = {}
    per_member: dict[str, dict[str, Any]] = {}

    for chk in checks:
        chk_issues, chk_metrics, chk_pm = chk.run(ctx, structure, pol, members)
        issues.extend(chk_issues)
        # namespace metrics by check name
        for k, v in chk_metrics.items():
            metrics[f"{chk.name}.{k}"] = v
        for mid, data in chk_pm.items():
            per_member.setdefault(mid, {}).update({f"{chk.name}.{k}": v for k, v in data.items()})

    # global maxima convenience
    _compute_global_maxima(metrics, per_member)

    return PhysicalPlausibilityReport(issues=issues, metrics=metrics, per_member=per_member)

# =============================================================================
# Extraction helpers (domain artifact -> StructuralMember)
# =============================================================================

def _extract_members(
    structure: Any,
    pol: PhysicsPolicy,
    *,
    domain_id: str | None,
) -> tuple[list[StructuralMember], list[Issue]]:
    """
    Extract StructuralMember list from structure notes.

    Supported schema (minimal):
    structure.notes["domains"][domain]["frameplan"]["members"] = [
      {
        "id": "...",
        "role": "beam",
        "span_mm": 6000,
        "section_width_mm": 140,
        "section_height_mm": 280,
        "material_id": "timber_oak_structural",
        "usage": "roof",
        "tributary_width_m": 1.2,
        "bearing_len_mm": 60,
      }, ...
    ]

    If members cannot be found, returns empty list + a warning Issue.
    """
    notes = getattr(structure, "notes", None) or getattr(structure, "Notes", None)
    if not isinstance(notes, dict):
        return [], [Issue(
            code="S_PHYS_NO_NOTES",
            severity="S",
            message="Structure has no notes dict; PPV could not access domain artifacts.",
        )]

    domains = notes.get("domains")
    if not isinstance(domains, dict) or not domains:
        return [], [Issue(
            code="S_PHYS_NO_DOMAIN_ARTIFACTS",
            severity="S",
            message="No notes['domains'] artifacts found; PPV could not extract structural members.",
        )]

    use_domain = domain_id
    if use_domain is None:
        # pick a single domain if there's exactly one
        if len(domains) == 1:
            use_domain = next(iter(domains.keys()))
        else:
            return [], [Issue(
                code="S_PHYS_DOMAIN_AMBIGUOUS",
                severity="S",
                message="Multiple domains present; pass domain_id to PPV to select which artifacts to validate.",
                details={"domains": list(domains.keys())},
            )]

    d = domains.get(use_domain, {})
    fp = d.get("frameplan") or d.get("structplan") or {}
    members_raw = fp.get("members")

    if not isinstance(members_raw, list) or not members_raw:
        return [], [Issue(
            code="S_PHYS_NO_MEMBERS",
            severity="S",
            message=f"No members found under notes['domains']['{use_domain}']['frameplan']['members'].",
        )]

    members: list[StructuralMember] = []
    issues: list[Issue] = []

    for i, m in enumerate(members_raw):
        if not isinstance(m, dict):
            issues.append(Issue(
                code="S_PHYS_MEMBER_SCHEMA",
                severity="S",
                message="Member is not a dict; skipped.",
                details={"index": i},
            ))
            continue

        mid = str(m.get("id", f"member_{i:04d}"))
        role = str(m.get("role", "unknown"))
        span_mm = float(m.get("span_mm", 0.0))
        section_width_mm = float(m.get("section_width_mm", 0.0))
        section_height_mm = float(m.get("section_height_mm", 0.0))

        if span_mm <= 0 or section_width_mm <= 0 or section_height_mm <= 0:
            issues.append(Issue(
                code="S_PHYS_MEMBER_INCOMPLETE",
                severity="S",
                message="Member missing span/section; skipped structural checks for this member.",
                member_id=mid,
                details={"span_mm": span_mm, "section_width_mm": section_width_mm, "section_height_mm": section_height_mm},
            ))
            # still keep it for sanity check visibility
        members.append(StructuralMember(
            id=mid,
            role=role,
            span_mm=span_mm,
            section_width_mm=section_width_mm,
            section_height_mm=section_height_mm,
            material_id=m.get("material_id"),
            usage=str(m.get("usage", "unknown")),
            tributary_width_m=m.get("tributary_width_m"),
            bearing_len_mm=m.get("bearing_len_mm"),
            raw=m,
        ))

    # If load model is missing for many members, warn once
    if any(mem.tributary_width_m is None for mem in members):
        issues.append(Issue(
            code="S_PHYS_LOADMODEL_PARTIAL",
            severity="S",
            message="Some members have no tributary_width_m; PPV will use a conservative default and results may be noisy.",
            details={"default_tributary_width_m": pol.default_tributary_width_m},
        ))

    return members, issues

# =============================================================================
# Check implementations
# =============================================================================

class GeometrySanityCheck:
    name = "GeometrySanity"

    def run(self, ctx, structure, pol: PhysicsPolicy, members: list[StructuralMember]):
        issues: list[Issue] = []
        metrics: dict[str, float] = {}
        pm: dict[str, dict[str, Any]] = {}

        min_thk = pol.min_member_thickness_mm
        bad = 0

        for m in members:
            if m.section_width_mm <= 0 or m.section_height_mm <= 0:
                continue

            if min(m.section_width_mm, m.section_height_mm) < min_thk:
                bad += 1
                issues.append(Issue(
                    code="S_PHYS_MIN_THICKNESS",
                    severity="S",
                    message=f"Member section thinner than minimum {min_thk:.0f} mm.",
                    member_id=m.id,
                    details={"section_width_mm": m.section_width_mm, "section_height_mm": m.section_height_mm, "min_mm": min_thk},
                ))
            pm[m.id] = {"section_width_mm": m.section_width_mm, "section_height_mm": m.section_height_mm, "span_mm": m.span_mm}

        metrics["thin_members"] = float(bad)
        return issues, metrics, pm

class StructuralBeamCheck:
    name = "StructuralBeam"

    def run(self, ctx, structure, pol: PhysicsPolicy, members: list[StructuralMember]):
        issues: list[Issue] = []
        metrics: dict[str, float] = {"max_utilization": 0.0, "max_deflection_mm": 0.0}
        pm: dict[str, dict[str, Any]] = {}

        for m in members:
            if m.role not in {"beam", "purlin", "joist", "rafter", "girder", "plate"}:
                continue
            if m.span_mm <= 0 or m.section_width_mm <= 0 or m.section_height_mm <= 0:
                continue

            mat = _resolve_material(m, pol)
            tw_m = float(m.tributary_width_m if m.tributary_width_m is not None else pol.default_tributary_width_m)
            w_N_per_mm = _line_load_N_per_mm(m.usage, pol, tw_m)

            L = m.span_mm
            b = m.section_width_mm
            h = m.section_height_mm

            # Section properties for rectangle
            I = b * (h ** 3) / 12.0
            W = b * (h ** 2) / 6.0

            # Bending
            M_max = w_N_per_mm * (L ** 2) / 8.0  # N*mm
            sigma = M_max / max(W, 1e-9)         # N/mm²
            util_bend = sigma / max(mat.fb_allow_N_mm2, 1e-9)

            # Deflection (simply supported, UDL)
            delta = (5.0 * w_N_per_mm * (L ** 4)) / (384.0 * mat.E_N_mm2 * max(I, 1e-9))

            # Optional shear check (rectangle approx)
            V_max = w_N_per_mm * L / 2.0
            tau = 1.5 * V_max / max(b * h, 1e-9)
            util_shear = tau / max(mat.fv_allow_N_mm2, 1e-9)

            # Serviceability limit depends on usage
            limit_ratio = pol.deflection_limit_ratio_roof if m.usage == "roof" else pol.deflection_limit_ratio_floor
            delta_limit = L / limit_ratio

            # Record maxima
            metrics["max_utilization"] = max(metrics["max_utilization"], util_bend, util_shear)
            metrics["max_deflection_mm"] = max(metrics["max_deflection_mm"], delta)

            pm[m.id] = {
                "material": mat.id if hasattr(mat, "id") else str(m.material_id),
                "tributary_width_m": tw_m,
                "w_N_per_mm": w_N_per_mm,
                "sigma_N_mm2": sigma,
                "tau_N_mm2": tau,
                "util_bend": util_bend,
                "util_shear": util_shear,
                "deflection_mm": delta,
                "deflection_limit_mm": delta_limit,
            }

            # Fail / warn logic
            if util_bend >= pol.utilization_fail:
                issues.append(Issue(
                    code="H_PHYS_BEAM_BENDING_FAIL",
                    severity="H",
                    message="Beam bending utilization exceeds allowable (physically implausible).",
                    member_id=m.id,
                    details={"util_bend": util_bend, "sigma": sigma, "fb_allow": mat.fb_allow_N_mm2},
                ))
            elif util_bend >= pol.utilization_warn:
                issues.append(Issue(
                    code="S_PHYS_UTILIZATION_HIGH",
                    severity="S",
                    message="Beam bending utilization is high.",
                    member_id=m.id,
                    details={"util_bend": util_bend},
                ))

            if util_shear >= pol.utilization_fail:
                issues.append(Issue(
                    code="H_PHYS_BEAM_SHEAR_FAIL",
                    severity="H",
                    message="Beam shear utilization exceeds allowable (physically implausible).",
                    member_id=m.id,
                    details={"util_shear": util_shear, "tau": tau, "fv_allow": mat.fv_allow_N_mm2},
                ))
            elif util_shear >= pol.utilization_warn:
                issues.append(Issue(
                    code="S_PHYS_SHEAR_HIGH",
                    severity="S",
                    message="Beam shear utilization is high.",
                    member_id=m.id,
                    details={"util_shear": util_shear},
                ))

            if delta > delta_limit:
                issues.append(Issue(
                    code="S_PHYS_DEFLECTION_HIGH",
                    severity="S",
                    message="Deflection exceeds serviceability heuristic limit.",
                    member_id=m.id,
                    details={"deflection_mm": delta, "limit_mm": delta_limit, "limit_ratio": limit_ratio},
                ))

        return issues, metrics, pm

class BearingCheck:
    name = "Bearing"

    def run(self, ctx, structure, pol: PhysicsPolicy, members: list[StructuralMember]):
        issues: list[Issue] = []
        metrics: dict[str, float] = {"max_bearing_util": 0.0}
        pm: dict[str, dict[str, Any]] = {}

        for m in members:
            if m.role not in {"beam", "purlin", "joist", "rafter", "girder", "plate"}:
                continue
            if m.span_mm <= 0 or m.section_width_mm <= 0 or m.section_height_mm <= 0:
                continue

            bearing_len = m.bearing_len_mm
            if bearing_len is None:
                continue  # not enough info; skip quietly

            if bearing_len < pol.min_bearing_len_mm:
                issues.append(Issue(
                    code="S_PHYS_BEARING_TOO_SHORT",
                    severity="S",
                    message=f"Bearing length below minimum {pol.min_bearing_len_mm:.0f} mm.",
                    member_id=m.id,
                    details={"bearing_len_mm": bearing_len, "min_mm": pol.min_bearing_len_mm},
                ))

            mat = _resolve_material(m, pol)
            tw_m = float(m.tributary_width_m if m.tributary_width_m is not None else pol.default_tributary_width_m)
            w_N_per_mm = _line_load_N_per_mm(m.usage, pol, tw_m)

            L = m.span_mm
            # reaction per support (simply supported, UDL)
            R = (w_N_per_mm * L) / 2.0  # N

            A_bearing = max(m.section_width_mm * bearing_len, 1e-9)  # mm²
            sigma_c90 = R / A_bearing  # N/mm²
            util = sigma_c90 / max(mat.fc90_allow_N_mm2, 1e-9)

            metrics["max_bearing_util"] = max(metrics["max_bearing_util"], util)
            pm[m.id] = {
                "bearing_len_mm": bearing_len,
                "reaction_N": R,
                "sigma_c90": sigma_c90,
                "util_bearing": util,
                "fc90_allow": mat.fc90_allow_N_mm2,
            }

            if util >= pol.utilization_fail:
                issues.append(Issue(
                    code="H_PHYS_BEARING_FAIL",
                    severity="H",
                    message="Bearing stress exceeds allowable (risk of crushing at support).",
                    member_id=m.id,
                    details={"util_bearing": util, "sigma_c90": sigma_c90},
                ))
            elif util >= pol.utilization_warn:
                issues.append(Issue(
                    code="S_PHYS_BEARING_HIGH",
                    severity="S",
                    message="Bearing utilization is high.",
                    member_id=m.id,
                    details={"util_bearing": util},
                ))

        return issues, metrics, pm

class PostSlendernessCheck:
    name = "PostSlenderness"

    def run(self, ctx, structure, pol: PhysicsPolicy, members: list[StructuralMember]):
        issues: list[Issue] = []
        metrics: dict[str, float] = {"max_slenderness": 0.0}
        pm: dict[str, dict[str, Any]] = {}

        for m in members:
            if m.role not in {"post", "column", "stud"}:
                continue
            if m.span_mm <= 0 or m.section_width_mm <= 0 or m.section_height_mm <= 0:
                continue

            L = m.span_mm  # treat as effective length in MVP (mm)
            b = m.section_width_mm
            h = m.section_height_mm

            # Use weaker axis radius of gyration (conservative)
            I_min = min(b * (h ** 3), h * (b ** 3)) / 12.0
            A = b * h
            r = (I_min / max(A, 1e-9)) ** 0.5
            slender = L / max(r, 1e-9)

            metrics["max_slenderness"] = max(metrics["max_slenderness"], slender)
            pm[m.id] = {"slenderness": slender, "L_mm": L, "r_mm": r}

            if slender >= pol.slenderness_fail:
                issues.append(Issue(
                    code="H_PHYS_POST_BUCKLING_FAIL",
                    severity="H",
                    message="Post is extremely slender (high buckling risk).",
                    member_id=m.id,
                    details={"slenderness": slender, "threshold": pol.slenderness_fail},
                ))
            elif slender >= pol.slenderness_warn:
                issues.append(Issue(
                    code="S_PHYS_SLENDERNESS_HIGH",
                    severity="S",
                    message="Post slenderness is high (buckling risk; consider larger section or bracing).",
                    member_id=m.id,
                    details={"slenderness": slender, "threshold": pol.slenderness_warn},
                ))

        return issues, metrics, pm

# =============================================================================
# Physics helpers
# =============================================================================

@dataclass(frozen=True, slots=True)
class _FallbackMaterial:
    id: str = "fallback_default"
    E_N_mm2: float = 11000.0
    density_kg_m3: float = 500.0
    fb_allow_N_mm2: float = 10.0
    fv_allow_N_mm2: float = 1.0
    fc90_allow_N_mm2: float = 2.0

def _resolve_material(m: StructuralMember, pol: PhysicsPolicy) -> Any:
    """
    Resolve material from MATERIALS registry using material_id.
    If missing, return conservative fallback.
    """
    mid = m.material_id
    if mid and isinstance(MATERIALS, dict) and mid in MATERIALS:
        return MATERIALS[mid]
    # fallback with policy numbers
    return _FallbackMaterial(
        E_N_mm2=pol.default_E_N_mm2,
        density_kg_m3=pol.default_density_kg_m3,
        fb_allow_N_mm2=pol.default_fb_allow_N_mm2,
        fv_allow_N_mm2=pol.default_fv_allow_N_mm2,
        fc90_allow_N_mm2=pol.default_fc90_allow_N_mm2,
    )

def _line_load_N_per_mm(usage: str, pol: PhysicsPolicy, tributary_width_m: float) -> float:
    """
    Convert area load (kN/m²) to line load (N/mm) using tributary width (m).
    """
    if usage == "floor":
        g = pol.g_dead_kN_m2_floor
        q = pol.q_live_kN_m2_floor
    else:
        # default to roof model
        g = pol.g_dead_kN_m2_roof
        q = pol.q_snow_kN_m2

    w_kN_per_m = (g + q) * tributary_width_m  # kN/m
    w_N_per_mm = (w_kN_per_m * 1000.0) / 1000.0  # (kN->N) and (m->mm) cancels nicely
    return w_N_per_mm

def _compute_global_maxima(metrics: dict[str, float], per_member: dict[str, dict[str, Any]]) -> None:
    """
    Convenience aggregate metrics from per-member fields.
    """
    max_util = 0.0
    max_defl = 0.0
    for mid, d in per_member.items():
        ub = d.get("StructuralBeam.util_bend")
        us = d.get("StructuralBeam.util_shear")
        df = d.get("StructuralBeam.deflection_mm")
        if isinstance(ub, (int, float)):
            max_util = max(max_util, float(ub))
        if isinstance(us, (int, float)):
            max_util = max(max_util, float(us))
        if isinstance(df, (int, float)):
            max_defl = max(max_defl, float(df))

    metrics["global.max_utilization"] = max_util
    metrics["global.max_deflection_mm"] = max_defl

# =============================================================================
# End
# =============================================================================
