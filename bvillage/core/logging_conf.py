# bvillage/core/logging_conf.py

"""
bvillage.core.logging_conf
==========================

Central logging configuration for bvillage.

Design goals
------------
- Safe to call multiple times (idempotent).
- Does not duplicate handlers on reload (important in Blender).
- Scoped to "bvillage" logger namespace.
- Can be silenced or elevated to DEBUG easily.

Public API
----------
configure_logging(level="INFO", force=False) -> None

Usage
-----
from bvillage.core.logging_conf import configure_logging
configure_logging(level="DEBUG")
"""

from __future__ import annotations

import logging
from typing import Literal


LogLevel = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]


def configure_logging(*, level: LogLevel = "INFO", force: bool = False) -> None:
    """
    Configure logging for the 'bvillage' namespace.

    Parameters
    ----------
    level:
        Logging level as string.
    force:
        If True, existing handlers are removed first (useful in Blender reload loops).

    Notes
    -----
    - Only configures the 'bvillage' logger tree.
    - Does not touch root logger.
    - Safe to call multiple times.
    """
    logger = logging.getLogger("bvillage")

    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    if force:
        for h in list(logger.handlers):
            logger.removeHandler(h)

    # Prevent duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.propagate = False
