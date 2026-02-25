# tests/test_logging.py

"""
tests.test_logging
==================

Basic sanity checks for logging configuration.
"""

from __future__ import annotations

import logging

from bvillage.core.logging_conf import configure_logging


def test_configure_logging_idempotent():
    configure_logging(level="DEBUG", force=True)
    logger = logging.getLogger("bvillage.test")

    logger.debug("debug message")
    logger.info("info message")

    # Reconfigure without force should not duplicate handlers
    configure_logging(level="INFO", force=False)
    handlers_before = len(logging.getLogger("bvillage").handlers)
    configure_logging(level="INFO", force=False)
    handlers_after = len(logging.getLogger("bvillage").handlers)

    assert handlers_before == handlers_after
