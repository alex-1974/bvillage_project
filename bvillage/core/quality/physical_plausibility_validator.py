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

Contracts (SYS_CONTRACT.md)
---------------------------
- Validators emit core.model.Issue objects.
- Validators must not mutate geometry.
- Determinism: no global RNG; stable iteration ordering.

Outputs
-------
- PhysicalPlausibilityReport with:
  - issues: list[core.model.Issue]
  - metrics: dict[str, float]
  - per_member: dict[str, dict[str, Any]]
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from bvillage.core.model import Issue


__all__ = [
    "PhysicsPolicy",
    "StructuralMember",
    "PhysicalPlausibilityReport",
    "run_physical_plausibility",
]


# ============================================================
# Data models
# ============================================================

@dataclass(frozen=True, slots=True)
class PhysicsPolicy:
    # Deflection limits: L / ratio
    deflection_limit_ratio_floor: float = 250.0
    deflection_limit_ratio_roof: float = 200.0

    # Utilization thresholds
    utilization_warn: float = 0.8
    utilization_fail: float = 1.0

    # Loads (kN/m²)
    g_dead_kN_m2_roof: float = 0.8
    q_snow_kN_m2: float = 0.75
    g_dead_kN_m2_floor: float = 0.5
    q_live_kN_m2_floor: float = 1.5

    # Fallback material props (if material registry lookup fails)
    default_E_N_mm2: float = 11000.0
    default_fb_allow_N_mm2: float = 10.0
    default_fv_allow_N_mm2: float = 1.0
    default_fc90_allow_N_mm2: float = 2.0
    default_density_kg_m3: float = 500.0

    # Geometry heuristics
    min_bearing_len_mm: float = 40.0
    min_member_thickness_mm: float = 60.0

    # Slenderness heuristic (warning-only in MVP)
    slenderness_warn: float = 120.0
    slenderness_fail: float = 200.0

    # Default tributary width for line-load derivation
    default_tributary_width_m: float = 1.0


@dataclass(frozen=True, slots=True)
class StructuralMember:
    id: str
    role: str
    span_mm: float
    section_width_mm: float
    section_height_mm: float
    material_id: str | None = None
    usage: str = "roof"  # "roof" | "floor" | etc.
    tributary_width_m: float | None = None
    bearing_len_mm: float | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class PhysicalPlausibilityReport:
    issues: list[Issue]
    metrics: dict[str, float] = field(default_factory=dict)
    per_member: dict[str, dict[str, Any]] = field(default_factory=dict)

    def has_hard_fail(self) -> bool:
        # Canonical severities: HARD / SOFT / SUGGEST
        for i in self.issues:
            if i.severity == "HARD":
                return True
        return False


class PhysicalCheck(Protocol):
    def run(
        self,
        ctx: Any,
        structure: Any,
        pol: PhysicsPolicy,
        members: list[StructuralMember],
    ) -> tuple[list[Issue], dict[str, float], dict[str, dict[str, Any]]]:
        ...


# ============================================================
# Issue helpers (core schema)
# ============================================================

def _mk_issue(
    *,
    code: str,
    severity: str,
    message: str,
    member_id: str | None = None,
    suggested_repairs: tuple[str, ...] = (),
) -> Issue:
    related: tuple[str, ...] = ()
    if member_id is not None:
        related = (member_id,)
    return Issue(
        code=str(code),
        severity=str(severity),
        message=str(message),
        related_ids=related,
        suggested_repairs=tuple(str(x) for x in suggested_repairs),
    )


# ============================================================
# Materials (fallback model)
# ============================================================

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
    Resolve material from registry if available; otherwise return fallback.

    This intentionally avoids importing renderer code and keeps core deterministic.
    """
    # Import lazily to avoid circular deps in early bootstrap scenarios.
    try:
        from bvillage.core.materials.material_registry import get_material_class  # type: ignore
    except Exception:
        get_material_class = None  # type: ignore

    if m.material_id and get_material_class is not None:
        try:
            return get_material_class(m.material_id)
        except Exception:
            # fall back below
            pass

    return _FallbackMaterial(
        E_N_mm2=float(pol.default_E_N_mm2),
        density_kg_m3=float(pol.default_density_kg_m3),
        fb_allow_N_mm2=float(pol.default_fb_allow_N_mm2),
        fv_allow_N_mm2=float(pol.default_fv_allow_N_mm2),
        fc90_allow_N_mm2=float(pol.default_fc90_allow_N_mm2),
    )


# ============================================================
# Loads
# ============================================================

def _line_load_N_per_mm(usage: str, pol: PhysicsPolicy, tributary_width_m: float) -> float:
    """
    Convert area loads (kN/m²) to line load (N/mm):
      w = (g + q) * tributary_width   [kN/m² * m] = kN/m
      kN/m -> N/mm: multiply by 1000 (N/kN) and divide by 1000 (mm/m) => N/mm
      so numerically: w_N_per_mm = (g+q) * tributary_width_m
    """
    if usage == "floor":
        g = float(pol.g_dead_kN_m2_floor)
        q = float(pol.q_live_kN_m2_floor)
    else:
        # default: roof
        g = float(pol.g_dead_kN_m2_roof)
        q = float(pol.q_snow_kN_m2)

    return (g + q) * float(tributary_width_m)


# ============================================================
# Member extraction
# ============================================================

def _extract_members(
    structure: Any,
    pol: PhysicsPolicy,
    *,
    domain_id: str | None,
) -> tuple[list[StructuralMember], list[Issue]]:
    """
    Extract members from notes domain artifacts.

    Expected:
      structure.notes["domains"][domain_id]["frameplan"]["members"] = [ ... ]
    """
    issues: list[Issue] = []
    members: list[StructuralMember] = []

    notes = getattr(structure, "notes", None)
    if not isinstance(notes, dict):
        issues.append(
            _mk_issue(
                code="PPV.NO_NOTES",
                severity="SUGGEST",
                message="StructurePlan.notes missing or invalid; PPV could not extract members.",
            )
        )
        return members, issues

    domains = notes.get("domains")
    if not isinstance(domains, dict):
        issues.append(
            _mk_issue(
                code="PPV.NO_DOMAINS",
                severity="SUGGEST",
                message="notes['domains'] missing; PPV could not extract members.",
            )
        )
        return members, issues

    did = domain_id or "fachwerk"
    dom = domains.get(did)
    if not isinstance(dom, dict):
        issues.append(
            _mk_issue(
                code="PPV.NO_DOMAIN",
                severity="SUGGEST",
                message=f"notes['domains']['{did}'] missing; PPV could not extract members.",
            )
        )
        return members, issues

    fp = dom.get("frameplan")
    if not isinstance(fp, dict):
        issues.append(
            _mk_issue(
                code="PPV.NO_FRAMEPLAN",
                severity="SUGGEST",
                message=f"Domain '{did}' has no frameplan artifact; PPV could not extract members.",
            )
        )
        return members, issues

    raw_members = fp.get("members")
    if not isinstance(raw_members, list):
        issues.append(
            _mk_issue(
                code="PPV.NO_MEMBERS",
                severity="SUGGEST",
                message=f"Frameplan in domain '{did}' has no members list; PPV could not run structural checks.",
            )
        )
        return members, issues

    for rm in raw_members:
        if not isinstance(rm, dict):
            continue

        try:
            mid = str(rm.get("id"))
            role = str(rm.get("kind") or rm.get("role") or "unknown")
            span_mm = float(rm.get("span_mm", 0.0))
            sw = float(rm.get("section_width_mm", 0.0))
            sh = float(rm.get("section_height_mm", 0.0))
            material_id = rm.get("material_id")
            usage = str(rm.get("usage", "roof"))
            trib = rm.get("tributary_width_m")
            trib_m = None if trib is None else float(trib)
            bearing = rm.get("bearing_len_mm")
            bearing_mm = None if bearing is None else float(bearing)
        except Exception:
            continue

        members.append(
            StructuralMember(
                id=mid,
                role=role,
                span_mm=span_mm,
                section_width_mm=sw,
                section_height_mm=sh,
                material_id=None if material_id is None else str(material_id),
                usage=usage,
                tributary_width_m=trib_m,
                bearing_len_mm=bearing_mm,
                raw=rm,
            )
        )

    if not members:
        issues.append(
            _mk_issue(
                code="PPV.MEMBERS_EMPTY",
                severity="SUGGEST",
                message=f"Frameplan in domain '{did}' produced an empty members list.",
            )
        )

    return members, issues


# ============================================================
# Checks
# ============================================================

class GeometrySanityCheck:
    def run(
        self,
        ctx: Any,
        structure: Any,
        pol: PhysicsPolicy,
        members: list[StructuralMember],
    ) -> tuple[list[Issue], dict[str, float], dict[str, dict[str, Any]]]:
        issues: list[Issue] = []
        metrics: dict[str, float] = {}
        per_member: dict[str, dict[str, Any]] = {}

        bad = 0
        for m in members:
            if m.span_mm <= 0 or m.section_width_mm <= 0 or m.section_height_mm <= 0:
                bad += 1
                issues.append(
                    _mk_issue(
                        code="PPV.GEOM.INVALID_MEMBER",
                        severity="SOFT",
                        message=(
                            f"Member '{m.id}' has invalid geometry "
                            f"(span_mm={m.span_mm}, w_mm={m.section_width_mm}, h_mm={m.section_height_mm})."
                        ),
                        member_id=m.id,
                    )
                )

            if m.section_width_mm < pol.min_member_thickness_mm or m.section_height_mm < pol.min_member_thickness_mm:
                issues.append(
                    _mk_issue(
                        code="PPV.GEOM.THIN_MEMBER",
                        severity="SUGGEST",
                        message=(
                            f"Member '{m.id}' thickness below heuristic minimum "
                            f"({pol.min_member_thickness_mm}mm)."
                        ),
                        member_id=m.id,
                    )
                )

        metrics["invalid_member_count"] = float(bad)
        return issues, metrics, per_member


class StructuralBeamCheck:
    def run(
        self,
        ctx: Any,
        structure: Any,
        pol: PhysicsPolicy,
        members: list[StructuralMember],
    ) -> tuple[list[Issue], dict[str, float], dict[str, dict[str, Any]]]:
        issues: list[Issue] = []
        metrics: dict[str, float] = {}
        per_member: dict[str, dict[str, Any]] = {}

        max_util = 0.0

        for m in members:
            if m.span_mm <= 0 or m.section_width_mm <= 0 or m.section_height_mm <= 0:
                continue

            mat = _resolve_material(m, pol)

            E = float(getattr(mat, "E_N_mm2", pol.default_E_N_mm2))
            fb_allow = float(getattr(mat, "fb_allow_N_mm2", pol.default_fb_allow_N_mm2))

            # Rectangular section properties
            b = float(m.section_width_mm)
            h = float(m.section_height_mm)
            L = float(m.span_mm)

            I = b * (h**3) / 12.0  # mm^4
            S = b * (h**2) / 6.0   # mm^3

            trib = float(m.tributary_width_m) if m.tributary_width_m is not None else float(pol.default_tributary_width_m)
            w = _line_load_N_per_mm(m.usage, pol, trib)  # N/mm

            # Simply supported beam under uniform load:
            # M_max = w L^2 / 8  [N*mm]
            M = w * (L**2) / 8.0

            # sigma = M / S  [N/mm^2]
            sigma = M / S
            util_bend = sigma / fb_allow if fb_allow > 0 else 999.0

            # deflection: delta = 5 w L^4 / (384 E I) [mm]
            delta = (5.0 * w * (L**4)) / (384.0 * E * I) if (E > 0 and I > 0) else 0.0

            limit_ratio = float(pol.deflection_limit_ratio_floor if m.usage == "floor" else pol.deflection_limit_ratio_roof)
            delta_allow = L / limit_ratio if limit_ratio > 0 else 0.0
            util_defl = (delta / delta_allow) if delta_allow > 0 else 0.0

            util = max(util_bend, util_defl)
            max_util = max(max_util, util)

            per_member[m.id] = {
                "usage": m.usage,
                "trib_m": trib,
                "w_N_per_mm": w,
                "sigma_N_mm2": sigma,
                "fb_allow_N_mm2": fb_allow,
                "util_bend": util_bend,
                "delta_mm": delta,
                "delta_allow_mm": delta_allow,
                "util_deflection": util_defl,
                "util_max": util,
            }

            if util >= pol.utilization_fail:
                issues.append(
                    _mk_issue(
                        code="PPV.BEAM.UTIL_FAIL",
                        severity="HARD",
                        message=f"Member '{m.id}' exceeds utilization (util={util:.3f} >= {pol.utilization_fail}).",
                        member_id=m.id,
                    )
                )
            elif util >= pol.utilization_warn:
                issues.append(
                    _mk_issue(
                        code="PPV.BEAM.UTIL_WARN",
                        severity="SOFT",
                        message=f"Member '{m.id}' high utilization (util={util:.3f} >= {pol.utilization_warn}).",
                        member_id=m.id,
                    )
                )

        metrics["max_utilization"] = float(max_util)
        return issues, metrics, per_member


class BearingCheck:
    def run(
        self,
        ctx: Any,
        structure: Any,
        pol: PhysicsPolicy,
        members: list[StructuralMember],
    ) -> tuple[list[Issue], dict[str, float], dict[str, dict[str, Any]]]:
        issues: list[Issue] = []
        metrics: dict[str, float] = {}
        per_member: dict[str, dict[str, Any]] = {}

        bad = 0
        for m in members:
            bearing = float(m.bearing_len_mm) if m.bearing_len_mm is not None else float(pol.min_bearing_len_mm)
            if bearing < pol.min_bearing_len_mm:
                bad += 1
                issues.append(
                    _mk_issue(
                        code="PPV.BEARING.MIN_LEN",
                        severity="SOFT",
                        message=(
                            f"Member '{m.id}' bearing length below minimum "
                            f"({bearing:.1f}mm < {pol.min_bearing_len_mm}mm)."
                        ),
                        member_id=m.id,
                    )
                )

            per_member[m.id] = {
                "bearing_len_mm": bearing,
                "min_bearing_len_mm": float(pol.min_bearing_len_mm),
            }

        metrics["bearing_len_violations"] = float(bad)
        return issues, metrics, per_member


class PostSlendernessCheck:
    def run(
        self,
        ctx: Any,
        structure: Any,
        pol: PhysicsPolicy,
        members: list[StructuralMember],
    ) -> tuple[list[Issue], dict[str, float], dict[str, dict[str, Any]]]:
        issues: list[Issue] = []
        metrics: dict[str, float] = {}
        per_member: dict[str, dict[str, Any]] = {}

        warn = 0
        fail = 0

        for m in members:
            # Only posts (heuristic): role contains "post" / "ständer"
            r = m.role.lower()
            if ("post" not in r) and ("ständer" not in r) and ("staender" not in r):
                continue

            # Very rough: slenderness = L / min(b, h)
            t = min(float(m.section_width_mm), float(m.section_height_mm))
            if t <= 0:
                continue

            slender = float(m.span_mm) / t if t > 0 else 0.0

            per_member[m.id] = {
                "slenderness": slender,
                "warn": float(pol.slenderness_warn),
                "fail": float(pol.slenderness_fail),
            }

            # MVP: warning-only heuristic (SOFT / SUGGEST), no engineering buckling calc
            if slender >= pol.slenderness_fail:
                fail += 1
                issues.append(
                    _mk_issue(
                        code="PPV.POST.SLENDER_FAIL",
                        severity="SOFT",
                        message=f"Post '{m.id}' very slender (λ={slender:.1f} >= {pol.slenderness_fail}).",
                        member_id=m.id,
                    )
                )
            elif slender >= pol.slenderness_warn:
                warn += 1
                issues.append(
                    _mk_issue(
                        code="PPV.POST.SLENDER_WARN",
                        severity="SUGGEST",
                        message=f"Post '{m.id}' slenderness warning (λ={slender:.1f} >= {pol.slenderness_warn}).",
                        member_id=m.id,
                    )
                )

        metrics["post_slender_warn"] = float(warn)
        metrics["post_slender_fail"] = float(fail)
        return issues, metrics, per_member


# ============================================================
# Aggregation helpers
# ============================================================

def _compute_global_maxima(metrics: dict[str, float], per_member: dict[str, dict[str, Any]]) -> None:
    # Keep deterministic: iterate sorted keys
    max_util = metrics.get("max_utilization", 0.0)
    for mid in sorted(per_member.keys()):
        util = per_member[mid].get("util_max")
        if isinstance(util, (int, float)):
            max_util = max(max_util, float(util))
    metrics["max_utilization"] = float(max_util)


# ============================================================
# Public entry
# ============================================================

def run_physical_plausibility(
    ctx: Any,
    structure: Any,
    *,
    policy: PhysicsPolicy | None = None,
    domain_id: str | None = None,
) -> PhysicalPlausibilityReport:
    pol = policy or PhysicsPolicy()

    members, issues = _extract_members(structure, pol, domain_id=domain_id)

    # Run checks (stable order)
    checks: tuple[PhysicalCheck, ...] = (
        GeometrySanityCheck(),
        StructuralBeamCheck(),
        BearingCheck(),
        PostSlendernessCheck(),
    )

    metrics: dict[str, float] = {}
    per_member: dict[str, dict[str, Any]] = {}

    for chk in checks:
        c_issues, c_metrics, c_pm = chk.run(ctx, structure, pol, members)

        # Extend in stable order (already stable by iteration)
        issues.extend(c_issues)

        # Merge metrics (last write wins per key; checks ordered)
        for k, v in c_metrics.items():
            metrics[str(k)] = float(v)

        # Merge per-member (merge dicts per member id)
        for mid, payload in c_pm.items():
            if mid not in per_member:
                per_member[mid] = {}
            if isinstance(payload, dict):
                for k, v in payload.items():
                    per_member[mid][str(k)] = v

    _compute_global_maxima(metrics, per_member)

    # Ensure issues list is deterministic: sort by (severity, code, related_id, message)
    def _issue_key(i: Issue) -> tuple[str, str, str, str]:
        rid = i.related_ids[0] if i.related_ids else ""
        return (i.severity, i.code, rid, i.message)

    issues.sort(key=_issue_key)

    return PhysicalPlausibilityReport(
        issues=issues,
        metrics=metrics,
        per_member=per_member,
    )
