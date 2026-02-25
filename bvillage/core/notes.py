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


DOMAINS_KEY = "domains"


def ensure_domains(notes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure notes contains notes["domains"] as a dict and return it.
    """
    d = notes.get(DOMAINS_KEY)
    if not isinstance(d, dict):
        d = {}
        notes[DOMAINS_KEY] = d
    return d


def set_domain_artifact(
    notes: Dict[str, Any],
    *,
    domain: str,
    name: str,
    payload: Any,
    legacy_aliases: Tuple[str, ...] = (),
) -> None:
    """
    Store payload under the structured domains schema, optionally with legacy aliases.

    Parameters
    ----------
    notes:
        Target notes dict (mutated).
    domain:
        Domain name, e.g. "fachwerk".
    name:
        Artifact name, e.g. "frameplan".
    payload:
        JSON-like dict payload (recommended).
    legacy_aliases:
        Additional top-level keys to set for back-compat.
    """
    domains = ensure_domains(notes)
    dom = domains.get(domain)
    if not isinstance(dom, dict):
        dom = {}
        domains[domain] = dom

    dom[name] = payload

    # legacy aliases
    for k in legacy_aliases:
        notes[k] = payload


def get_domain_artifact(
    notes: Dict[str, Any],
    *,
    domain: str,
    name: str,
    legacy_aliases: Tuple[str, ...] = (),
) -> Optional[Any]:
    """
    Retrieve payload from structured domains schema, with fallback to legacy aliases.
    """
    domains = notes.get(DOMAINS_KEY)
    if isinstance(domains, dict):
        dom = domains.get(domain)
        if isinstance(dom, dict) and name in dom:
            return dom.get(name)

    # fallback
    for k in legacy_aliases:
        if k in notes:
            return notes.get(k)

    return None
