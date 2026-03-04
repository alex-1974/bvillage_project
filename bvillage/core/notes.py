# bvillage/core/notes.py

"""
bvillage.core.notes
===================

Purpose
-------
Stable schema for storing "hybrid notes" on planning artifacts.

Why
---
We store derived artifacts (frameplans, reports, domain metadata) inside
StructurePlan.notes to support:
- Blender build pipeline
- debugging and reporting
- long-lived compatibility across refactors

Schema
------
notes is a dict. The preferred structured schema is:

notes["domains"][<domain_name>][<artifact_name>] = payload

Example:
notes["domains"]["fachwerk"]["frameplan"] = {...}

Back-compat Aliases
-------------------
During migration we also store common legacy keys, e.g.:
- notes["frameplan"]
- notes["fachwerk.frameplan"]

Helpers in this module make the behavior consistent and future-proof.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from .hot_path import hot, hot_api

DOMAINS_KEY = "domains"


# ------------------------------------------------------------
# Internal helper
# ------------------------------------------------------------

def _normalize_artifact_param(
    *,
    artifact: Optional[str],
    name: Optional[str],
    func: str,
) -> str:
    """
    Normalize parameter naming.

    Preferred: artifact
    Legacy: name
    """
    if artifact is None:
        artifact = name
    elif name is not None and name != artifact:
        raise ValueError(
            f"{func}: conflicting artifact identifiers "
            f"(artifact={artifact!r}, name={name!r})"
        )

    if artifact is None:
        raise TypeError(
            f"{func}: missing required argument 'artifact' "
            f"(or legacy 'name')"
        )

    return artifact


# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------

# HOT PATH — pipeline backbone; called frequently across stages
@hot_api
def ensure_domains(notes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure notes contains notes["domains"] as a dict and return it.
    """
    d = notes.get(DOMAINS_KEY)
    if not isinstance(d, dict):
        d = {}
        notes[DOMAINS_KEY] = d
    return d

# HOT PATH — pipeline backbone; called frequently across stages
@hot_api
def set_domain_artifact(
    notes: Dict[str, Any],
    *,
    domain: str,
    artifact: Optional[str] = None,
    name: Optional[str] = None,
    payload: Any,
    legacy_aliases: Tuple[str, ...] = (),
) -> None:
    """
    Store payload under the structured domains schema, optionally with legacy aliases.

    Preferred parameter:
        artifact="frameplan"

    Legacy parameter (still supported):
        name="frameplan"
    """
    artifact = _normalize_artifact_param(
        artifact=artifact,
        name=name,
        func="set_domain_artifact",
    )

    domains = ensure_domains(notes)
    dom = domains.get(domain)
    if not isinstance(dom, dict):
        dom = {}
        domains[domain] = dom

    dom[artifact] = payload

    # legacy aliases (flat keys)
    for k in legacy_aliases:
        notes[k] = payload

# HOT PATH — pipeline backbone; called frequently across stages
@hot_api
def get_domain_artifact(
    notes: Dict[str, Any],
    *,
    domain: str,
    artifact: Optional[str] = None,
    name: Optional[str] = None,
    legacy_aliases: Tuple[str, ...] = (),
) -> Optional[Any]:
    """
    Retrieve payload from structured domains schema, with fallback to legacy aliases.

    Preferred parameter:
        artifact="frameplan"

    Legacy parameter (still supported):
        name="frameplan"
    """
    artifact = _normalize_artifact_param(
        artifact=artifact,
        name=name,
        func="get_domain_artifact",
    )

    domains = notes.get(DOMAINS_KEY)
    if isinstance(domains, dict):
        dom = domains.get(domain)
        if isinstance(dom, dict) and artifact in dom:
            return dom.get(artifact)

    # fallback to legacy flat keys
    for k in legacy_aliases:
        if k in notes:
            return notes.get(k)

    return None
