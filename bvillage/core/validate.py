# bvillage/core/validate.py

"""
Central Validation Aggregation
==============================

Stable Public API:
    validate(ctx, structure, interior) -> tuple[Issue]

Notes:
- ctx and interior are accepted for API stability.
- Currently only structure.notes artifacts are evaluated.
"""

from __future__ import annotations

from typing import List, Tuple, Dict, Any

from bvillage.core.model import Issue


__all__ = [
    "validate",
]


# ============================================================
# Helpers
# ============================================================

def _artifact_issues_to_core(payload: Dict[str, Any]) -> List[Issue]:
    issues: List[Issue] = []

    raw = payload.get("issues")
    if not isinstance(raw, list):
        return issues

    for entry in raw:
        if not isinstance(entry, dict):
            continue

        issues.append(
            Issue(
                code=str(entry.get("code", "UNKNOWN")),
                severity=str(entry.get("severity", "SUGGEST")),
                message=str(entry.get("message", "")),
                related_ids=tuple(entry.get("related_ids", [])),
                suggested_repairs=tuple(entry.get("suggested_repairs", [])),
            )
        )

    return issues


def _issue_sort_key(i: Issue) -> Tuple[str, str, str, str]:
    rid = i.related_ids[0] if i.related_ids else ""
    return (i.severity, i.code, rid, i.message)


# ============================================================
# Public API (STABLE)
# ============================================================

def validate(ctx: Any, structure: Any, interior: Any) -> Tuple[Issue, ...]:
    """
    Central validation entry point.

    Signature must remain stable:
        validate(ctx, structure, interior)

    Currently:
        - collects PPV issues from structure.notes
        - deterministic ordering
    """

    issues: List[Issue] = []

    notes = getattr(structure, "notes", None)
    if isinstance(notes, dict):

        domains = notes.get("domains")
        if isinstance(domains, dict):

            # ---- PPV artifact ----
            core_dom = domains.get("core")
            if isinstance(core_dom, dict):
                ppv = core_dom.get("ppv")
                if isinstance(ppv, dict):
                    issues.extend(_artifact_issues_to_core(ppv))

    issues.sort(key=_issue_sort_key)

    return tuple(issues)
