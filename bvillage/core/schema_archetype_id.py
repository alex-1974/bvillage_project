# bvillage/core/schema_archetype_id.py

from __future__ import annotations

import re

__all__ = [
    "validate_archetype_id",
    "ARCHETYPE_ID_PATTERN",
]


# ------------------------------------------------------------
# Archetype ID pattern
#
# Format:
#
#   DOMAIN-TYPE-VARIANT
#
# Examples
#
#   FW-LH-ND
#   FW-LH-3S
#   FW-STG-GIE
#
# ------------------------------------------------------------

ARCHETYPE_ID_PATTERN = re.compile(
    r"^[A-Z]{2,4}-[A-Z0-9]{2,6}-[A-Z0-9]{2,6}$"
)


def validate_archetype_id(archetype_id: str) -> None:
    """
    Validate canonical archetype identifier.

    Rules
    -----
    - uppercase
    - hyphen separated
    - DOMAIN-TYPE-VARIANT pattern

    Raises
    ------
    RuntimeError if invalid
    """

    if not isinstance(archetype_id, str):
        raise RuntimeError("archetype_id must be string")

    archetype_id = archetype_id.strip()

    if not archetype_id:
        raise RuntimeError("archetype_id empty")

    if not ARCHETYPE_ID_PATTERN.match(archetype_id):
        raise RuntimeError(
            "Invalid archetype_id format:\n"
            f"  {archetype_id}\n\n"
            "Expected pattern:\n"
            "  DOMAIN-TYPE-VARIANT\n"
            "Example:\n"
            "  FW-LH-ND"
        )
