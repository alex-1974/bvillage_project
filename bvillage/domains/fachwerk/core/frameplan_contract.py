# bvillage/domains/fachwerk/core/frameplan_contract.py

"""
bvillage.domains.fachwerk.core.frameplan_contract
=================================================

Contract gate for FramePlan artifacts.

Goals
- Validate members-first artifacts for Blender builders.
- Enforce stable structural semantics via ontology TIDs (tid).
- Keep checks fast (settlement scale).

Rules
- Structural semantics MUST use `tid` (ontology term id).
- `role` is legacy / material-only metadata and must not drive geometry.
- Opening jambs use tid=POST_JAMB with side="L"|"R".
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Iterable, Optional

from bvillage.core.ontology.structural_terms import (
    VALID_TIDS,
    POST_PRIMARY,
    POST_JAMB,
    POST_INTERIOR,
    BEAM_EAVES_PLATE,
    BEAM_LINTEL,
    BEAM_WINDOW_SILL,
    BRACE_DIAGONAL,
    INFILL_CELL,
)

LOG = logging.getLogger(__name__)

WALLS = ("N", "S", "E", "W")


# ---------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------

@dataclass(slots=True, frozen=True)
class ContractReport:
    ok: bool
    hard: list[str]
    soft: list[str]
    stats: dict[str, Any]


# ---------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------

def _is_finite(x: Any) -> bool:
    try:
        v = float(x)
    except Exception:
        return False
    return v == v and v not in (float("inf"), float("-inf"))


def _members(fp: dict[str, Any]) -> Optional[dict[str, Any]]:
    m = fp.get("members")
    return m if isinstance(m, dict) else None


def _iter_members(members: dict[str, Any], key: str) -> Iterable[dict[str, Any]]:
    arr = members.get(key)
    if not isinstance(arr, list):
        return
    for x in arr:
        if isinstance(x, dict):
            yield x


def _count_by_tid(members: dict[str, Any]) -> dict[str, int]:
    out: dict[str, int] = {}
    for k in ("posts", "rails", "braces", "infills"):
        for m in _iter_members(members, k):
            tid = m.get("tid")
            if not isinstance(tid, str) or not tid:
                continue
            out[tid] = out.get(tid, 0) + 1
    return out


def _index_opening_members(
    members: dict[str, Any],
) -> tuple[
    dict[str, list[dict[str, Any]]],   # jamb_l_by_wall
    dict[str, list[dict[str, Any]]],   # jamb_r_by_wall
    dict[str, list[dict[str, Any]]],   # lintel_by_wall
    dict[str, list[dict[str, Any]]],   # sill_by_wall
]:
    # O(n) indexing to avoid O(n*m) scans across openings × members.
    jamb_l: dict[str, list[dict[str, Any]]] = {w: [] for w in WALLS}
    jamb_r: dict[str, list[dict[str, Any]]] = {w: [] for w in WALLS}
    lintel: dict[str, list[dict[str, Any]]] = {w: [] for w in WALLS}
    sill:   dict[str, list[dict[str, Any]]] = {w: [] for w in WALLS}

    for m in _iter_members(members, "posts"):
        w = m.get("wall")
        if w not in WALLS:
            continue
        if m.get("tid") != POST_JAMB:
            continue
        side = m.get("side")
        if side == "L":
            jamb_l[w].append(m)
        elif side == "R":
            jamb_r[w].append(m)

    for m in _iter_members(members, "rails"):
        w = m.get("wall")
        if w not in WALLS:
            continue
        tid = m.get("tid")
        if tid == BEAM_LINTEL:
            lintel[w].append(m)
        elif tid == BEAM_WINDOW_SILL:
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
    jamb_l, jamb_r, lintel, sill = _index_opening_members(members)

    missing_jambs = 0
    missing_lintels = 0
    missing_sills = 0

    for i, o in enumerate(openings):
        if not isinstance(o, dict):
            continue
        name = o.get("name") or o.get("id") or f"opening[{i}]"
        wall = o.get("wall")
        if wall not in WALLS:
            hard.append(f"opening '{name}': invalid/missing wall")
            continue

        # We only check existence per opening name; matching is by "opening" field when present.
        # If member lacks "opening", it still counts (coarser check).
        def _has_member(arr: list[dict[str, Any]], *, side_required: Optional[str] = None) -> bool:
            for m in arr:
                if not isinstance(m, dict):
                    continue
                if side_required is not None and m.get("side") != side_required:
                    continue
                mo = m.get("opening")
                if mo is None:
                    return True
                if mo == name:
                    return True
            return False

        if not _has_member(jamb_l[wall], side_required="L") or not _has_member(jamb_r[wall], side_required="R"):
            missing_jambs += 1

        if not _has_member(lintel[wall]):
            missing_lintels += 1

        if o.get("typ") == "window":
            if not _has_member(sill[wall]):
                missing_sills += 1

    stats["openings_missing_jambs"] = missing_jambs
    stats["openings_missing_lintels"] = missing_lintels
    stats["openings_missing_sills"] = missing_sills

    if missing_jambs:
        hard.append(f"opening completeness: {missing_jambs} opening(s) missing jamb L/R members")
    if missing_lintels:
        hard.append(f"opening completeness: {missing_lintels} opening(s) missing lintel members")
    if missing_sills:
        soft.append(f"opening completeness: {missing_sills} window(s) missing sill members (soft)")


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def audit_frameplan_contract(fp: dict[str, Any], house: dict[str, Any], *, strict: bool = False) -> ContractReport:
    """
    Validate FramePlan + house metadata for rendering.

    Hard checks:
    - members dict exists
    - members.* are lists of dicts
    - every member has valid tid in ontology
    - minimal PRIMARY_POST presence
    - minimal EAVES_PLATE presence (for v0.4.x Fachwerk pipeline)
    - opening completeness (jamb L/R + lintel, optional sill)

    Returns ContractReport; if strict=True raises ValueError on hard violations.
    """
    hard: list[str] = []
    soft: list[str] = []
    stats: dict[str, Any] = {}

    mem = _members(fp)
    if mem is None:
        hard.append("missing required dict field fp['members'] (members-first required)")
        rep = ContractReport(ok=False, hard=hard, soft=soft, stats=stats)
        if strict:
            raise ValueError("\n".join(hard))
        return rep

    # Normalize member containers (type checks only)
    for key in ("posts", "rails", "braces", "infills"):
        arr = mem.get(key)
        if not isinstance(arr, list):
            hard.append(f"members.{key} must be a list")
            continue
        for i, m in enumerate(arr):
            if not isinstance(m, dict):
                hard.append(f"members.{key}[{i}] must be an object")
                continue
            tid = m.get("tid")
            if not isinstance(tid, str) or not tid:
                hard.append(f"members.{key}[{i}] missing required string field 'tid'")
                continue
            if tid not in VALID_TIDS:
                hard.append(f"members.{key}[{i}] unknown tid '{tid}'")

            # Minimal field sanity on common members
            if tid in (POST_PRIMARY, POST_JAMB, POST_INTERIOR):
                if m.get("wall") not in WALLS and m.get("wall") != "MID":
                    hard.append(f"members.{key}[{i}] post has invalid wall {m.get('wall')!r}")
                if not (_is_finite(m.get("u")) and _is_finite(m.get("z0")) and _is_finite(m.get("z1"))):
                    hard.append(f"members.{key}[{i}] post has non-finite u/z0/z1")

                if tid == POST_JAMB:
                    if m.get("side") not in ("L", "R"):
                        hard.append(f"members.{key}[{i}] opening jamb requires side in {{'L','R'}}")

            if tid in (BEAM_EAVES_PLATE, BEAM_LINTEL, BEAM_WINDOW_SILL):
                if m.get("wall") not in WALLS:
                    hard.append(f"members.{key}[{i}] rail/beam has invalid wall {m.get('wall')!r}")
                if not (_is_finite(m.get("u0")) and _is_finite(m.get("u1")) and _is_finite(m.get("z"))):
                    hard.append(f"members.{key}[{i}] rail/beam has non-finite u0/u1/z")

            if tid == BRACE_DIAGONAL:
                if m.get("wall") not in WALLS:
                    hard.append(f"members.{key}[{i}] brace has invalid wall {m.get('wall')!r}")

            if tid == INFILL_CELL:
                if m.get("wall") not in WALLS:
                    hard.append(f"members.{key}[{i}] infill has invalid wall {m.get('wall')!r}")

    # Stats
    stats["members_tid_counts"] = _count_by_tid(mem)
    stats["members_posts"] = len(mem.get("posts") or [])
    stats["members_rails"] = len(mem.get("rails") or [])
    stats["members_braces"] = len(mem.get("braces") or [])
    stats["members_infills"] = len(mem.get("infills") or [])

    # Minimal guarantees for current Fachwerk pipeline
    posts = mem.get("posts") or []
    rails = mem.get("rails") or []

    if not any(isinstance(m, dict) and m.get("tid") == POST_PRIMARY for m in posts):
        hard.append("members-first required: missing/empty members.posts with tid=post.primary")

    if not any(isinstance(m, dict) and m.get("tid") == BEAM_EAVES_PLATE for m in rails):
        hard.append("members-first required: missing/empty members.rails with tid=beam.eaves_plate")

    # Opening completeness (uses fp['openings'] list if present)
    openings = fp.get("openings") or []
    if isinstance(openings, list) and openings:
        _opening_completeness_checks(openings=openings, members=mem, hard=hard, soft=soft, stats=stats)

    ok = (len(hard) == 0)
    rep = ContractReport(ok=ok, hard=hard, soft=soft, stats=stats)

    if strict and not ok:
        raise ValueError("FramePlan contract violations:\n" + "\n".join(hard))

    return rep


def assert_frameplan_contract(fp: dict[str, Any], house: dict[str, Any]) -> None:
    """Strict contract assertion helper."""
    audit_frameplan_contract(fp, house, strict=True)
