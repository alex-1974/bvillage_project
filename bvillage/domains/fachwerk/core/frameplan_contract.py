# bvillage/domains/fachwerk/core/frameplan_contract.py

#
# Fachwerk FramePlan Contract Audit (v2)
#
# Purpose:
#   Pre-flight quality gate for FramePlan + house data.
#   Ensures geometric, topological and semantic consistency BEFORE Blender build.
#
# Philosophy:
#   - Pure data audit (no Blender imports)
#   - schema_version >= 2: members-first is enforced
#   - axes_u / axes_z remain as geometric & bounds guards
#
# Severity:
#   - hard: build must be considered invalid (strict=True can raise)
#   - soft: warnings (plausibility, duplicates, missing profiles if defaults exist)

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any
import math

__all__ = ['audit_frameplan_contract', 'assert_frameplan_contract', 'ContractReport']

LOG = logging.getLogger("bvillage.domains.fachwerk.core.frameplan_contract")

WALLS = ("N", "S", "E", "W")

# Tolerances (meters) for matching members to openings
TOL_U = 0.005   # 5 mm
TOL_Z = 0.005   # 5 mm
TOL_SPAN = 0.005

# ------------------------------------------------------------
# Report model
# ------------------------------------------------------------

@dataclass(slots=True)
class ContractReport:
    ok: bool
    hard: list[str]
    soft: list[str]
    stats: dict[str, Any]

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def _is_monotonic(values: list[float]) -> bool:
    return all(values[i] < values[i + 1] for i in range(len(values) - 1))

def _is_finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False

def _f(x: Any, default: float | None = None) -> float | None:
    try:
        if x is None:
            return default
        return float(x)
    except Exception:
        return default

def _near(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol

def _span_near(a0: float, a1: float, b0: float, b1: float, tol: float) -> bool:
    return _near(a0, b0, tol) and _near(a1, b1, tol)

def _profile_ok(p: Any) -> bool:
    if not isinstance(p, dict):
        return False
    w = p.get("w")
    d = p.get("d")
    return _is_finite(w) and _is_finite(d) and float(w) > 0.0 and float(d) > 0.0

def _role_counts(members: dict[str, Any]) -> dict[str, int]:
    out: dict[str, int] = {}
    for k in ("posts", "rails", "braces", "infills"):
        arr = members.get(k) or []
        if not isinstance(arr, list):
            continue
        for m in arr:
            if not isinstance(m, dict):
                continue
            r = str(m.get("role", ""))
            if not r:
                continue
            out[r] = out.get(r, 0) + 1
    return out

def _dedupe_key_post(m: dict[str, Any]) -> Tuple:
    return (
        "post",
        m.get("role"),
        m.get("wall"),
        round(float(m.get("u", 0.0)) * 1000.0),
        round(float(m.get("z0", 0.0)) * 1000.0),
        round(float(m.get("z1", 0.0)) * 1000.0),
    )

def _dedupe_key_rail(m: dict[str, Any]) -> Tuple:
    return (
        "rail",
        m.get("role"),
        m.get("wall"),
        round(float(m.get("u0", 0.0)) * 1000.0),
        round(float(m.get("u1", 0.0)) * 1000.0),
        round(float(m.get("z", 0.0)) * 1000.0),
    )

def _dedupe_key_brace(m: dict[str, Any]) -> Tuple:
    return (
        "brace",
        m.get("role"),
        m.get("wall"),
        round(float(m.get("u0", 0.0)) * 1000.0),
        round(float(m.get("z0", 0.0)) * 1000.0),
        round(float(m.get("u1", 0.0)) * 1000.0),
        round(float(m.get("z1", 0.0)) * 1000.0),
    )

def _dedupe_key_infill(m: dict[str, Any]) -> Tuple:
    return (
        "infill",
        m.get("role"),
        m.get("wall"),
        round(float(m.get("u0", 0.0)) * 1000.0),
        round(float(m.get("u1", 0.0)) * 1000.0),
        round(float(m.get("z0", 0.0)) * 1000.0),
        round(float(m.get("z1", 0.0)) * 1000.0),
    )

def _find_openings_list(fp: dict[str, Any]) -> list[dict[str, Any]]:
    openings = fp.get("openings") or []
    if isinstance(openings, list):
        return [o for o in openings if isinstance(o, dict)]
    if isinstance(openings, dict):
        return [o for o in openings.values() if isinstance(o, dict)]
    return []

def _wall_u_range(axes_u: dict[str, Any], wall: str) -> tuple[float, float | None]:
    w = axes_u.get(wall)
    if not isinstance(w, dict):
        return None
    u_all = w.get("all") or []
    if not isinstance(u_all, list) or len(u_all) < 2:
        return None
    try:
        mn = min(float(x) for x in u_all)
        mx = max(float(x) for x in u_all)
        return (mn, mx)
    except Exception:
        return None

def _members(fp: dict[str, Any]) -> dict[str, Any | None]:
    m = fp.get("members")
    return m if isinstance(m, dict) else None

def _iter_members(members: dict[str, Any], key: str) -> tuple[dict[str, Any], ...]:
    # WHY: returns tuple (not generator) so callers need no list() wrapping
    # and the result is stable for snapshot tests and iteration in _opening_completeness_checks.
    arr = members.get(key) or []
    if not isinstance(arr, list):
        return ()
    return tuple(x for x in arr if isinstance(x, dict))

def _match_opening_name(member: dict[str, Any], opening_name: str) -> bool:
    return str(member.get("opening", "")) == str(opening_name)

def _index_opening_members(
    members: dict[str, Any],
) -> tuple[
    dict[str, list[dict[str, Any]]],   # jamb_l_by_wall
    dict[str, list[dict[str, Any]]],   # jamb_r_by_wall
    dict[str, list[dict[str, Any]]],   # lintel_by_wall
    dict[str, list[dict[str, Any]]],   # sill_by_wall
]:
    # WHY: Pre-index posts and rails by wall and role once — O(n+m) total
    # instead of O(n*m) from scanning all members for each opening.
    # At settlement scale with 50 openings × 200 members this is a 10× speedup.
    jamb_l: dict[str, list[dict[str, Any]]] = {w: [] for w in WALLS}
    jamb_r: dict[str, list[dict[str, Any]]] = {w: [] for w in WALLS}
    lintel: dict[str, list[dict[str, Any]]] = {w: [] for w in WALLS}
    sill:   dict[str, list[dict[str, Any]]] = {w: [] for w in WALLS}

    for m in _iter_members(members, "posts"):
        w = m.get("wall")
        if w not in WALLS:
            continue
        role = m.get("role")
        if role == "OPENING_JAMB_L":
            jamb_l[w].append(m)
        elif role == "OPENING_JAMB_R":
            jamb_r[w].append(m)

    for m in _iter_members(members, "rails"):
        w = m.get("wall")
        if w not in WALLS:
            continue
        role = m.get("role")
        if role == "OPENING_LINTEL":
            lintel[w].append(m)
        elif role == "OPENING_SILL":
            sill[w].append(m)

    return jamb_l, jamb_r, lintel, sill

def _opening_completeness_checks(
    *,
    openings: list[dict[str, Any]],
    members: dict[str, Any],
    hard: list[str],
    soft: list[str],
    stats: dict[str, Any],
) -> None:
    # Build wall-grouped index once — O(posts + rails).
    # Per-opening lookups then scan only the relevant wall bucket.
    jamb_l_idx, jamb_r_idx, lintel_idx, sill_idx = _index_opening_members(members)

    per_opening: dict[str, Any] = {}

    for o in openings:
        name = str(o.get("name", "?"))
        typ = str(o.get("type") or o.get("typ") or "")
        wall = o.get("wall")
        u0 = _f(o.get("u0"))
        u1 = _f(o.get("u1"))
        z0 = _f(o.get("z0"))
        z1 = _f(o.get("z1"))

        missing: list[str] = []
        ok = True

        if wall not in WALLS or u0 is None or u1 is None or z0 is None or z1 is None:
            hard.append(f"opening {name}: missing required keys for semantic match (wall/u0/u1/z0/z1)")
            per_opening[name] = {"ok": False, "missing": ["META_INVALID"]}
            continue

        wall_jamb_l = jamb_l_idx[wall]
        wall_jamb_r = jamb_r_idx[wall]
        wall_lintel = lintel_idx[wall]
        wall_sill   = sill_idx[wall]

        jamb_l = [
            m for m in wall_jamb_l
            if _match_opening_name(m, name) or _near(float(m.get("u", 1e9)), float(u0), TOL_U)
        ]
        jamb_r = [
            m for m in wall_jamb_r
            if _match_opening_name(m, name) or _near(float(m.get("u", 1e9)), float(u1), TOL_U)
        ]

        if len(jamb_l) != 1:
            ok = False
            missing.append("OPENING_JAMB_L" if len(jamb_l) == 0 else "OPENING_JAMB_L_DUP")
        if len(jamb_r) != 1:
            ok = False
            missing.append("OPENING_JAMB_R" if len(jamb_r) == 0 else "OPENING_JAMB_R_DUP")

        lintel = [
            m for m in wall_lintel
            if (
                _match_opening_name(m, name)
                or (
                    _span_near(float(m.get("u0", 1e9)), float(m.get("u1", -1e9)), float(u0), float(u1), TOL_SPAN)
                    and _near(float(m.get("z", 1e9)), float(z1), TOL_Z)
                )
            )
        ]
        if len(lintel) != 1:
            ok = False
            missing.append("OPENING_LINTEL" if len(lintel) == 0 else "OPENING_LINTEL_DUP")

        if typ == "window":
            sill = [
                m for m in wall_sill
                if (
                    _match_opening_name(m, name)
                    or (
                        _span_near(float(m.get("u0", 1e9)), float(m.get("u1", -1e9)), float(u0), float(u1), TOL_SPAN)
                        and _near(float(m.get("z", 1e9)), float(z0), TOL_Z)
                    )
                )
            ]
            if len(sill) != 1:
                ok = False
                missing.append("OPENING_SILL" if len(sill) == 0 else "OPENING_SILL_DUP")

        if not ok:
            hard.append(f"opening {name}: missing/invalid members: {', '.join(missing)}")

        per_opening[name] = {"ok": ok, "missing": missing}

    stats["openings_members"] = per_opening

# ------------------------------------------------------------
# Main audit
# ------------------------------------------------------------

def audit_frameplan_contract(
    fp: dict[str, Any],
    house: dict[str, Any],
    *,
    strict: bool = False,
) -> ContractReport:
    """
    Pre-flight contract audit for FramePlan.

    v1 checks:
      - axis monotonicity (house.axes_u/axes_v)
      - axes_z monotonicity
      - dimension plausibility (z_plate > z0, L/W > 0)
      - opening bounds inside wall and z-range

    v2 checks (schema_version >= 2):
      - members presence
      - members.posts/rails/braces/infills presence (members-first cut)
      - member field validation (finite numeric, required keys)
      - opening semantic completeness (jambs/lintel/sill)
      - duplicates (mm-rounded keys)

    Notes:
      - No Blender imports.
      - No auto-fix; reports only.
    """

    hard: list[str] = []
    soft: list[str] = []

    schema_version = int(fp.get("schema_version", 1) or 1)

    house_axes_u = house.get("axes_u") or []   # grid axes — list[float], for monotonicity + length checks
    axes_v = house.get("axes_v") or []
    z0_build = float(house.get("z0", 0.0))
    z_plate = float(house.get("z_plate", 0.0))

    axes_u = fp.get("axes_u") or {}            # wall→axes map — dict[str, ...], for opening bounds checks
    axes_z = fp.get("axes_z") or []
    openings = _find_openings_list(fp)

    stats: dict[str, Any] = {
        "schema_version": schema_version,
        "axes_u": len(house_axes_u) if isinstance(house_axes_u, list) else "?",
        "axes_v": len(axes_v) if isinstance(axes_v, list) else "?",
        "axes_z": len(axes_z) if isinstance(axes_z, list) else "?",
        "openings": len(openings),
    }

    LOG.info(
        "FRAMEPLAN AUDIT start | schema=%d axes_u=%s axes_v=%s z_axes=%s openings=%d",
        schema_version,
        stats["axes_u"], stats["axes_v"], stats["axes_z"], stats["openings"],
    )

    # --------------------------------------------------------
    # 1) House axis sanity (v1)
    # --------------------------------------------------------

    if not isinstance(house_axes_u, list) or len(house_axes_u) < 2:
        hard.append("axes_u must contain at least 2 values")
    if not isinstance(axes_v, list) or len(axes_v) < 2:
        hard.append("axes_v must contain at least 2 values")

    if isinstance(house_axes_u, list) and len(house_axes_u) >= 2:
        try:
            ax = [float(x) for x in house_axes_u]
            if not _is_monotonic(ax):
                hard.append("axes_u must be strictly increasing")
        except Exception:
            hard.append("axes_u must be numeric")

    if isinstance(axes_v, list) and len(axes_v) >= 2:
        try:
            ay = [float(y) for y in axes_v]
            if not _is_monotonic(ay):
                hard.append("axes_v must be strictly increasing")
        except Exception:
            hard.append("axes_v must be numeric")

    if not isinstance(axes_z, list) or len(axes_z) < 2:
        hard.append("axes_z must contain at least 2 values")
    else:
        try:
            az = [float(z) for z in axes_z]
            if not _is_monotonic(az):
                hard.append("axes_z must be strictly increasing")
        except Exception:
            hard.append("axes_z must be numeric")

    # --------------------------------------------------------
    # 2) Dimension consistency (v1)
    # --------------------------------------------------------

    if isinstance(house_axes_u, list) and house_axes_u:
        try:
            L = float(house_axes_u[-1]) - float(house_axes_u[0])
            if L <= 0.0:
                hard.append("computed length L <= 0")
        except Exception:
            hard.append("computed length L invalid (axes_u not numeric)")

    if isinstance(axes_v, list) and axes_v:
        try:
            W = float(axes_v[-1]) - float(axes_v[0])
            if W <= 0.0:
                hard.append("computed width W <= 0")
        except Exception:
            hard.append("computed width W invalid (axes_v not numeric)")

    if z_plate <= z0_build:
        hard.append("z_plate must be greater than z0")

    # --------------------------------------------------------
    # 3) Opening bounds (v1)
    # --------------------------------------------------------

    z_top = None
    if isinstance(axes_z, list) and axes_z:
        try:
            z_top = float(axes_z[-1])
        except Exception:
            z_top = None

    for o in openings:
        name = o.get("name", "?")
        wall = o.get("wall")
        u0 = _f(o.get("u0"), None)
        u1 = _f(o.get("u1"), None)
        z0o = _f(o.get("z0"), None)
        z1o = _f(o.get("z1"), None)

        if u0 is None or u1 is None or z0o is None or z1o is None:
            hard.append(f"opening {name}: missing numeric u0/u1/z0/z1")
            continue

        if u0 >= u1:
            hard.append(f"opening {name}: u0 >= u1")
        if z0o >= z1o:
            hard.append(f"opening {name}: z0 >= z1")

        if not isinstance(axes_u, dict) or wall not in axes_u:
            hard.append(f"opening {name}: wall '{wall}' not in axes_u")
            continue

        w_range = _wall_u_range(axes_u, str(wall))
        if w_range is None:
            hard.append(f"opening {name}: wall '{wall}' has insufficient u-axes (missing axes_u[wall].all?)")
            continue

        wall_u_min, wall_u_max = w_range
        if u0 < wall_u_min or u1 > wall_u_max:
            hard.append(
                f"opening {name}: u-range [{u0:.3f}..{u1:.3f}] outside wall range [{wall_u_min:.3f}..{wall_u_max:.3f}]"
            )

        if z_top is not None:
            if z0o < z0_build or z1o > z_top:
                hard.append(f"opening {name}: z-range [{z0o:.3f}..{z1o:.3f}] outside building vertical range")

    # --------------------------------------------------------
    # 4) Members-first checks (v2)  [CUT]
    # --------------------------------------------------------

    if schema_version >= 2:
        mem = _members(fp)
        if mem is None:
            hard.append("schema_version>=2 requires fp['members'] dict")
        else:
            # Require members lists to exist (hard cut: Blender builds ONLY these)
            for k in ("posts", "rails", "braces", "infills"):
                if k not in mem:
                    hard.append(f"schema_version>=2 requires members['{k}'] present")

            posts = _iter_members(mem, "posts")
            rails = _iter_members(mem, "rails")
            braces = _iter_members(mem, "braces")
            infills = _iter_members(mem, "infills")

            stats["members_posts"] = len(posts)
            stats["members_rails"] = len(rails)
            stats["members_braces"] = len(braces)
            stats["members_infills"] = len(infills)
            stats["members_role_counts"] = _role_counts(mem)

            if len(posts) == 0:
                hard.append("members.posts must be non-empty for schema_version>=2")

            # -------- posts validation --------
            seen_post: set[tuple] = set()
            dup_posts = 0
            for i, m in enumerate(posts):
                role = m.get("role")
                wall = m.get("wall")
                u = m.get("u")
                z0m = m.get("z0")
                z1m = m.get("z1")

                if wall not in WALLS:
                    hard.append(f"member post[{i}]: invalid wall {wall!r}")
                if not role:
                    hard.append(f"member post[{i}]: missing role")
                if not (_is_finite(u) and _is_finite(z0m) and _is_finite(z1m)):
                    hard.append(f"member post[{i}]: non-finite u/z0/z1")
                    continue

                fu = float(u)
                fz0 = float(z0m)
                fz1 = float(z1m)

                if fz0 >= fz1:
                    hard.append(f"member post[{i}]: z0>=z1 (z0={fz0:.3f}, z1={fz1:.3f})")

                if isinstance(axes_u, dict) and wall in WALLS:
                    w_range = _wall_u_range(axes_u, str(wall))
                    if w_range is not None:
                        mn, mx = w_range
                        if fu < mn - TOL_U or fu > mx + TOL_U:
                            hard.append(
                                f"member post[{i}]: u={fu:.3f} outside wall {wall} range [{mn:.3f}..{mx:.3f}]"
                            )

                if not _profile_ok(m.get("profile")):
                    soft.append(f"member post[{i}]: missing/invalid profile (w,d)")

                k = _dedupe_key_post(m)
                if k in seen_post:
                    dup_posts += 1
                else:
                    seen_post.add(k)

            stats["members_dup_posts"] = dup_posts
            if dup_posts:
                soft.append(f"duplicate posts detected (mm-rounded): {dup_posts}")

            # -------- rails validation --------
            seen_rail: set[tuple] = set()
            dup_rails = 0
            for i, m in enumerate(rails):
                role = m.get("role")
                wall = m.get("wall")
                u0m = m.get("u0")
                u1m = m.get("u1")
                zm = m.get("z")

                if wall not in WALLS:
                    hard.append(f"member rail[{i}]: invalid wall {wall!r}")
                if not role:
                    hard.append(f"member rail[{i}]: missing role")
                if not (_is_finite(u0m) and _is_finite(u1m) and _is_finite(zm)):
                    hard.append(f"member rail[{i}]: non-finite u0/u1/z")
                    continue

                fu0 = float(u0m)
                fu1 = float(u1m)
                fz = float(zm)

                if fu0 >= fu1:
                    hard.append(f"member rail[{i}]: u0>=u1 (u0={fu0:.3f}, u1={fu1:.3f})")

                if isinstance(axes_u, dict) and wall in WALLS:
                    w_range = _wall_u_range(axes_u, str(wall))
                    if w_range is not None:
                        mn, mx = w_range
                        if fu0 < mn - TOL_U or fu1 > mx + TOL_U:
                            hard.append(
                                f"member rail[{i}]: span [{fu0:.3f}..{fu1:.3f}] outside wall {wall} range [{mn:.3f}..{mx:.3f}]"
                            )

                if z_top is not None:
                    if fz < z0_build - TOL_Z or fz > z_top + TOL_Z:
                        hard.append(f"member rail[{i}]: z={fz:.3f} outside vertical range")

                if not _profile_ok(m.get("profile")):
                    soft.append(f"member rail[{i}]: missing/invalid profile (w,d)")

                k = _dedupe_key_rail(m)
                if k in seen_rail:
                    dup_rails += 1
                else:
                    seen_rail.add(k)

            stats["members_dup_rails"] = dup_rails
            if dup_rails:
                soft.append(f"duplicate rails detected (mm-rounded): {dup_rails}")

            # -------- braces validation (members-only) --------
            seen_brace: set[tuple] = set()
            dup_braces = 0
            for i, m in enumerate(braces):
                role = m.get("role")
                wall = m.get("wall")
                u0m = m.get("u0")
                u1m = m.get("u1")
                z0m = m.get("z0")
                z1m = m.get("z1")

                if not role:
                    hard.append(f"member brace[{i}]: missing role")
                if role not in ("BRACE_DIAG",):
                    soft.append(f"member brace[{i}]: unexpected role '{role}'")

                if wall not in WALLS:
                    hard.append(f"member brace[{i}]: invalid wall {wall!r}")

                if not (_is_finite(u0m) and _is_finite(u1m) and _is_finite(z0m) and _is_finite(z1m)):
                    hard.append(f"member brace[{i}]: non-finite u0/u1/z0/z1")
                    continue

                fu0 = float(u0m)
                fu1 = float(u1m)
                fz0 = float(z0m)
                fz1 = float(z1m)

                if _near(fu0, fu1, 1e-12) or _near(fz0, fz1, 1e-12):
                    soft.append(f"member brace[{i}]: degenerate diagonal (u0==u1 or z0==z1)")

                if isinstance(axes_u, dict) and wall in WALLS:
                    w_range = _wall_u_range(axes_u, str(wall))
                    if w_range is not None:
                        mn, mx = w_range
                        if min(fu0, fu1) < mn - TOL_U or max(fu0, fu1) > mx + TOL_U:
                            hard.append(
                                f"member brace[{i}]: u-span [{min(fu0, fu1):.3f}..{max(fu0, fu1):.3f}] outside wall {wall} range [{mn:.3f}..{mx:.3f}]"
                            )

                if z_top is not None:
                    if min(fz0, fz1) < z0_build - TOL_Z or max(fz0, fz1) > z_top + TOL_Z:
                        hard.append(f"member brace[{i}]: z-span outside vertical range")

                if not _profile_ok(m.get("profile")):
                    soft.append(f"member brace[{i}]: missing/invalid profile (w,d)")

                k = _dedupe_key_brace(m)
                if k in seen_brace:
                    dup_braces += 1
                else:
                    seen_brace.add(k)

            stats["members_dup_braces"] = dup_braces
            if dup_braces:
                soft.append(f"duplicate braces detected (mm-rounded): {dup_braces}")

            # -------- infills validation (members-only) --------
            seen_infill: set[tuple] = set()
            dup_infills = 0
            for i, m in enumerate(infills):
                role = m.get("role")
                wall = m.get("wall")
                u0m = m.get("u0")
                u1m = m.get("u1")
                z0m = m.get("z0")
                z1m = m.get("z1")

                if not role:
                    hard.append(f"member infill[{i}]: missing role")
                if role != "INFILL_CELL":
                    soft.append(f"member infill[{i}]: unexpected role '{role}' (expected INFILL_CELL)")

                if wall not in WALLS:
                    hard.append(f"member infill[{i}]: invalid wall {wall!r}")

                if not (_is_finite(u0m) and _is_finite(u1m) and _is_finite(z0m) and _is_finite(z1m)):
                    hard.append(f"member infill[{i}]: non-finite u0/u1/z0/z1")
                    continue

                fu0 = float(u0m)
                fu1 = float(u1m)
                fz0 = float(z0m)
                fz1 = float(z1m)

                if fu0 >= fu1:
                    hard.append(f"member infill[{i}]: u0>=u1 (u0={fu0:.3f}, u1={fu1:.3f})")
                if fz0 >= fz1:
                    hard.append(f"member infill[{i}]: z0>=z1 (z0={fz0:.3f}, z1={fz1:.3f})")

                if isinstance(axes_u, dict) and wall in WALLS:
                    w_range = _wall_u_range(axes_u, str(wall))
                    if w_range is not None:
                        mn, mx = w_range
                        if fu0 < mn - TOL_U or fu1 > mx + TOL_U:
                            hard.append(
                                f"member infill[{i}]: span [{fu0:.3f}..{fu1:.3f}] outside wall {wall} range [{mn:.3f}..{mx:.3f}]"
                            )

                if z_top is not None:
                    if fz0 < z0_build - TOL_Z or fz1 > z_top + TOL_Z:
                        hard.append(f"member infill[{i}]: z-span outside vertical range")

                k = _dedupe_key_infill(m)
                if k in seen_infill:
                    dup_infills += 1
                else:
                    seen_infill.add(k)

            stats["members_dup_infills"] = dup_infills
            if dup_infills:
                soft.append(f"duplicate infills detected (mm-rounded): {dup_infills}")

            # Opening frame semantic completeness (hard)
            _opening_completeness_checks(
                openings=openings,
                members=mem,
                hard=hard,
                soft=soft,
                stats=stats,
            )

            # Minimal PRIMARY_POST guarantee (hard)
            primary = [m for m in posts if m.get("role") == "PRIMARY_POST"]
            if len(primary) == 0:
                hard.append("schema_version>=2 requires at least one PRIMARY_POST in members.posts")

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    ok = len(hard) == 0

    for msg in hard:
        LOG.error("FRAMEPLAN FAIL | %s", msg)
    for msg in soft:
        LOG.warning("FRAMEPLAN warn | %s", msg)

    LOG.info("FRAMEPLAN AUDIT done | ok=%s hard=%d soft=%d", ok, len(hard), len(soft))

    report = ContractReport(ok=ok, hard=hard, soft=soft, stats=stats)

    if strict and not ok:
        raise RuntimeError(f"FramePlan contract failed: hard={len(hard)}")

    return report

def assert_frameplan_contract(fp: dict[str, Any], house: dict[str, Any]) -> None:
    report = audit_frameplan_contract(fp, house, strict=False)
    if not report.ok:
        raise RuntimeError("FramePlan contract assertion failed")
