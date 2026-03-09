"""
Compatibility shim.

Old entry point: bvillage.core.foreman.generate()

New entry point: SiteManager.build()
"""

from __future__ import annotations

from bvillage.core.site_manager import SiteManager


def generate(ctx):
    return SiteManager().build(ctx)
