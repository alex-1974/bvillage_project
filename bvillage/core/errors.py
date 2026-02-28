# bvillage/core/errors.py
"""
BVILLAGE exception hierarchy.

Design goals:
- Clear separation between contract/schema errors and operational builder errors.
- No generic RuntimeError in core pipeline.
- Layer-aware wrapping (raise ... from e).
"""

class BVillageError(Exception):
    """Base class for all BVILLAGE-specific errors."""


# ---------------------------------------------------------------------
# Contract / Schema / Structural correctness
# ---------------------------------------------------------------------

class ContractError(BVillageError):
    """Base class for contract or API violations."""


class SchemaError(ContractError):
    """FramePlan / Structure schema invalid or incomplete."""


class InvariantError(ContractError):
    """Mathematical or structural invariant violated."""


# ---------------------------------------------------------------------
# Builder / Rendering layer
# ---------------------------------------------------------------------

class BuilderError(BVillageError):
    """Base class for builder-layer failures."""


class BlenderOpError(BuilderError):
    """Blender operation failed (context, mode, data-block issues)."""


class MaterialResolveError(BuilderError):
    """Material resolution or shader construction failed."""
