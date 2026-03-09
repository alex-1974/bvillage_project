# bvillage/core/schema_archetypes.py

"""
BVILLAGE Archetype Schema

Stable machine identifiers for architectural archetypes.

IDs follow the pattern:

    <DOMAIN>-<FAMILY>-<VARIANT>

Example:

    FW-LH-ND

Meaning:

    Domain  : FW  (timber frame)
    Family  : LH  (longhouse)
    Variant : ND  (niederdeutsch)

These IDs are used for plugin dispatch.

Human readable names are defined separately here.
"""

from __future__ import annotations


ARCHETYPE_DISPLAY_NAMES: dict[str, str] = {

    # --- Longhouse family (Fachwerk) ---

    "FW-LH-ND": "Niederdeutsches Hallenhaus",

    "FW-LH-2S": "Zweiständerhaus",
    "FW-LH-3S": "Dreiständerhaus",
    "FW-LH-4S": "Vierständerhaus",

    "FW-LH-GULF": "Gulfhaus",
    "FW-LH-HAUB": "Haubarg",
    "FW-LH-MITT": "Mittertennhaus",

    # --- Townhouse family ---

    "FW-STG-GIE": "Giebelständiges Stadthaus",
}
