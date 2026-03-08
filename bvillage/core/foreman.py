"""
bvillage/core/foreman.py

Foreman orchestrates the BVILLAGE generation pipeline.

Core principle:
Core must NOT know any architectural domain (fachwerk, stone, etc.).

The Foreman only interacts with:

- Context
- ProviderRegistry
- Contracts
"""

from __future__ import annotations

from typing import Any

from bvillage.core.context import Context
from bvillage.core.registry import ProviderRegistry
from bvillage.core.errors import GenerationError
from bvillage.core.validate import validate_pipeline


def generate(ctx: Context) -> dict[str, Any]:
    """
    Main entry point of the BVILLAGE engine.

    Pipeline:

        Context
            ↓
        ProviderRegistry.resolve()
            ↓
        Provider.generate()
            ↓
        validate_pipeline()
            ↓
        return result
    """

    provider = ProviderRegistry.resolve(ctx)

    if provider is None:
        raise GenerationError(
            f"No provider found for context: {ctx}"
        )

    result = provider.generate(ctx)

    validate_pipeline(result)

    return result
