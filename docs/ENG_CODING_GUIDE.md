# BVILLAGE – Coding Guide

---
tier: 3
authority: OPERATIONAL
change-frequency: as-needed
change-rule: Additions welcome. Changes to decided conventions require explicit team decision and CHANGELOG entry.
referenced-by: ENG_BUILDER_CONTRACT.md, DOCS_INDEX.md
references: SYS_CONTRACT.md §5, §10, §11, §12, SYS_NAMING_POLICY.md
---

This guide defines how we write Python in BVILLAGE. It covers conventions, patterns, and decisions that apply across the entire codebase. Rules already defined in SYS_CONTRACT are referenced here but not repeated.

Prerequisites: Read SYS_CONTRACT.md and SYS_NAMING_POLICY.md first. This guide assumes familiarity with both.

---

## 1. Environment

**Python minimum version: 3.12**

Required for: `slots=True` on dataclasses, `X | Y` union syntax, `match` statement, `tomllib`, improved error messages. The project currently runs on 3.13 — 3.12 is the minimum to ensure broad compatibility while using all modern syntax.

**Dependencies policy:**

- Core and Domain-core: stdlib only. No external dependencies.
- Numpy is not a current dependency. It may be introduced in Domain-core when a concrete, measured performance need justifies it — not before.
- Blender (`bpy`): renderer modules only. Never imported in Core, Domain-core, or type modules.
- External libraries require an explicit architecture decision and a CHANGELOG entry.

---

## 2. Functions

### Single responsibility

Every function has exactly one testable purpose. If the docstring contains "and", the function is too large. If a function cannot be tested without setting up more than one external condition, it is too large.

Public functions per module: maximum three. All other functions are private (leading underscore).

```python
# Wrong — two responsibilities
def derive_and_validate_posts(axes, openings, policy):
    ...

# Right — separated
def derive_posts(axes, openings, policy) -> tuple[Post, ...]:
    ...

def validate_posts(posts, structure) -> tuple[Issue, ...]:
    ...
```

### Performance tiers

Two tiers exist in BVILLAGE with different priorities:

**Hot path functions** — called repeatedly during generation (member derivation, axis merging, policy resolution). Mark explicitly:

```python
# HOT PATH — keep allocation-free, no logging, no defensive checks
def _merge_axes(primary: tuple[float, ...], secondary: tuple[float, ...], tol: float) -> tuple[float, ...]:
    ...
```

Hot path rules: no f-strings, no logging, no defensive allocation, use generators and early exit, profile before optimizing further.

**Structural functions** — complex logic called once per generation (FramePlan derivation, PolicyStack resolution, InteriorPlanner). Readability first. Document invariants fully. Performance matters only at algorithmic level — correct complexity class, no O(n²) where O(n log n) is possible.

### Pure functions as default

Core and Domain-core functions must be pure where possible: same inputs always produce same outputs, no side effects visible outside the function. Side effects — logging, Blender emission — occur only at defined stage boundaries.

A function that reads from or writes to external state must be explicitly justified.

### Generators and `yield`

Generator expressions are useful as internal construction tools. `yield` as a return mechanism is not used in BVILLAGE.

The standard arguments for generators — lazy evaluation, memory efficiency, state retention — do not apply here. The largest member collection BVILLAGE ever produces is a FramePlan with a few hundred elements. Memory is not the constraint. And state retention, often described as a feature, is precisely the problem: a generator can be traversed exactly once, is not hashable, cannot be stored in a frozen dataclass, and cannot be compared for equality. Everything determinism and immutability require is incompatible with generators as return values.

**The rule:** generator expressions are allowed inside a function as a construction aid. They must be materialized before crossing any function boundary.

```python
# Correct — generator expression used internally, materialized before return
def derive_posts(axes: tuple[float, ...], policy: ResolvedPolicy) -> tuple[Post, ...]:
    return tuple(
        Post(wall=w, u=u, z0=z0, z1=z1, role=_role(u, policy))
        for w, u, z0, z1 in _axis_combinations(axes, policy)
        if not _in_opening(u, opening_union)
    )

# Correct — early exit via generator expression
has_conflict = any(collides(m, opening) for m in members for opening in openings)

# Wrong — generator as return value
def derive_posts(...) -> Generator[Post, None, None]:
    for axis in axes:
        yield Post(...)
```

`itertools` is permitted where it clarifies intent: `chain` to concatenate member groups, `pairwise` for adjacent axis pairs, `groupby` for wall-grouped operations. Always materialize into `tuple` or `dict` before the value leaves the function.

### Concurrency

`asyncio` is not used. The pipeline is sequential by design — each stage waits for the previous. Cooperative multitasking adds complexity without benefit and introduces non-deterministic scheduling when multiple tasks are simultaneously ready.

Future settlement-scale parallelism, if needed, uses `ProcessPoolExecutor`: each process receives a deterministic seed, works independently, and results are merged in sorted order. This preserves determinism. That decision belongs to a future roadmap item, not the current architecture.

---

## 3. Type hints

Type hints are mandatory on all public functions and dataclass fields. They are not optional, not "where they add clarity" — always.

```python
# Wrong
def derive_posts(axes, openings, policy):
    ...

# Right
def derive_posts(
    axes: tuple[float, ...],
    openings: tuple[Opening, ...],
    policy: ResolvedPolicy,
) -> tuple[Post, ...]:
    ...
```

Use `X | Y` union syntax, not `Union[X, Y]`. Use `tuple[X, ...]` for homogeneous immutable sequences, `tuple[X, Y, Z]` for fixed-length heterogeneous tuples. Use `list[X]`, `dict[K, V]`, `set[X]` directly — never `typing.List`, `typing.Dict`, `typing.Tuple`, `typing.Set`. These are legacy aliases deprecated since Python 3.9.

Run `mypy` on Core and Domain-core. Blender modules are excluded from mypy due to bpy stub limitations.

---

## 4. Data structures

### Dataclasses

`@dataclass(frozen=True, slots=True)` is the default for all value objects in Core and Domain-core.

- `frozen=True` — enforces immutability, enables hashing, catches mutation bugs at runtime and statically.
- `slots=True` — reduces memory overhead, speeds up attribute access. Relevant when thousands of Member instances exist simultaneously at settlement scale.

```python
@dataclass(frozen=True, slots=True)
class Post:
    wall: str
    u: float
    z0: float
    z1: float
    role: str
    material_id: str
```

Mutable dataclasses are permitted only during construction within a single function scope, and only when converting to a frozen dataclass at return.

### Tuple vs. list

`tuple` for all completed collections in Core data structures. `list` only during construction within a function, converted to `tuple` before return or storage.

Rationale: A `members` collection in FramePlan is complete after derivation — it does not grow. `frozen=True` on a dataclass protects the attribute reference but not the contents of a `list`. `tuple` makes immutability genuine.

```python
# Construction — list is fine here
posts: list[Post] = []
for axis in sorted_axes:
    posts.append(_derive_post(axis, policy))

# Storage — always tuple
return FramePlan(posts=tuple(posts), rails=tuple(rails), ...)
```

### Dicts

Use `dict` for lookup tables and artifact storage (notes schema). Keys must be strings. Dict iteration order is guaranteed in Python 3.7+ but must never be relied upon for structural decisions — always sort explicitly when order matters.

### Sets

Use `set` for membership tests where order is irrelevant. Never use sets where deterministic ordering is required — convert to sorted tuple before any structural use.

---

## 5. Floats

All geometric values use Python `float` — IEEE 754 double precision (64-bit). This is sufficient for architectural dimensions at any plausible scale.

**Never compare floats with `==`.** All comparisons go through `geom_eps` (defined centrally in `bvillage/core/geom_eps.py`). No module defines its own epsilon value — SYS_CONTRACT §6.1.

```python
# Wrong
if u == axis:
    ...

# Right
if abs(u - axis) < geom_eps.AXIS_MERGE_TOL:
    ...
```

`decimal.Decimal` is not used — too slow, not necessary for geometry. `numpy.float64` is not used in Core — no numpy dependency in Core.

---

## 6. Immutability and collections

`frozen=True` on a dataclass does not protect mutable contents. When a dataclass field contains a collection, use `tuple`, not `list`. If a field must be a dict, document why mutation protection is not required.

For deeply nested structures, freeze at every level. A `FramePlan` containing a `tuple[Post, ...]` where `Post` is also frozen provides genuine structural immutability.

---

## 7. Seed system

Seeds are never raw integers. All seed handling uses the `Seed` wrapper:

```python
@dataclass(frozen=True, slots=True)
class Seed:
    world: int
    settlement: int
    house_salt: int

    def derive(self, component: str) -> int:
        """Derives a deterministic child seed for a named sub-component.

        Args:
            component: Stable name identifying the sub-component.
                       Must not change between versions without explicit decision.

        Returns:
            A deterministic integer seed for the named component.
        """
        import hashlib
        key = f"{self.world}:{self.settlement}:{self.house_salt}:{component}"
        return int(hashlib.shake_128(key.encode()).hexdigest(8), 16)
```

Usage:

```python
rng = Random(seed.derive("posts"))
rng_material = Random(seed.derive("material.oak"))
rng_roof = Random(seed.derive("roof.pitch"))
```

Component names are stable identifiers — changing them changes output for that seed. They follow the naming convention `<layer>.<aspect>`.

No module may call `random.random()`, `random.seed()`, or any global RNG function. All randomness flows through `Seed.derive()`.

---

## 8. Exception hierarchy

Project-specific exceptions signal contract violations and architectural failures. Never use `ValueError` or `AssertionError` for contract violations — they are indistinguishable from bugs.

```
BVillageError(Exception)
  ├── ContractError              # Layer boundary violation, role violation
  │     ├── LayerBoundaryError  # Core imports bpy, builder modifies FramePlan
  │     └── SchemaError         # FramePlan missing required members
  ├── DeterminismError           # Global RNG used, unstable iteration order
  ├── MaterialError              # Unregistered material ID
  └── PolicyError                # Unknown patch key, silent fallback attempted
```

`assert_*` functions raise from this hierarchy. `validate_*` functions return `Issue` objects — they never raise.

```python
def assert_members_complete(fp: FramePlan) -> None:
    """Asserts that the FramePlan contains all required member types.

    Raises:
        SchemaError: if posts, rails, or braces are absent.
    """
    if not fp.posts:
        raise SchemaError("FramePlan has no posts — contract violation")
```

---

## 9. Invariants — preconditions and postconditions

All stage entry points document their invariants explicitly in the docstring. Invariants define what a function requires to be true on entry (preconditions) and what it guarantees to be true on exit (postconditions).

```python
def derive_frameplan(
    structure: StructurePlan,
    policy: ResolvedPolicy,
) -> FramePlan:
    """Derives the structural FramePlan from a validated structure and policy.

    Preconditions:
        - structure.walls is non-empty
        - policy has passed invariant validation (resolve_policy_stack postcondition)
        - All opening demands reference walls present in structure

    Postconditions:
        - Every wall in structure has at least one post
        - Every opening demand appears as an opening in the FramePlan
        - fp.posts, fp.rails, fp.braces are non-empty tuples
        - All member coordinates are within structure bounds

    Raises:
        SchemaError: if postconditions cannot be satisfied given the input.
    """
```

Preconditions are checked at stage boundaries by `assert_*` functions. Postconditions are verified by the next stage's precondition checks — this creates a chain of verified handoffs across the pipeline.

---

## 10. Documentation

### Docstring format

Google-style docstrings on all public functions and classes. Private functions receive a docstring only when the logic is non-obvious.

Structure:

```python
def resolve_policy_stack(ctx: BuildContext) -> ResolvedPolicy:
    """Resolves the full policy stack for a given build context.

    Applies BaseTypePolicy, optional modifier policies, StylePolicy,
    CulturePolicy, and NoisePolicy in order. Each policy is a delta
    on the canonical parameter tree.

    Args:
        ctx: The build context containing archetype ID, region, epoch,
             wealth, settlement type, and seed.

    Returns:
        A fully resolved, validated ResolvedPolicy ready for planning.

    Raises:
        PolicyError: if an unknown patch key is encountered.
        PolicyError: if invariant validation fails after resolution.

    Preconditions:
        - ctx.archetype_id is registered in the type registry
        - ctx.seed is a valid Seed instance

    Postconditions:
        - All canonical parameters have resolved values
        - Invariant validation has passed
    """
```

### What belongs in a docstring

- What the function does — one sentence, active voice
- Args: name, type if not obvious from hint, meaning
- Returns: type and meaning
- Raises: which exceptions and under what condition
- Preconditions and Postconditions for stage functions
- Not: implementation details, performance notes, change history

### Module-level docstrings

Every module has a one-line module docstring stating its role and layer:

```python
# bvillage/domains/fachwerk/core/derive_frameplan.py
"""Derives the Fachwerk FramePlan from a resolved StructurePlan and policy."""
```

### `__all__`

Every module defines `__all__` explicitly. This documents the public API and prevents accidental exposure of implementation details.

```python
__all__ = ["derive_frameplan"]
```

---

## 11. Core patterns

### Compute → Validate → Emit

Never build and decide simultaneously. Collect all data first, validate as a batch, then emit.

```python
# Wrong — build while deciding
for axis in axes:
    post = Post(...)
    if conflicts(post, openings):
        continue
    emit_post(post)

# Right — compute, validate, emit
candidates = tuple(_derive_post(axis, policy) for axis in axes)
valid = tuple(p for p in candidates if not _conflicts(p, openings))
assert_posts_sufficient(valid, structure)
return valid
```

This pattern makes each stage testable in isolation and prevents partial state from propagating.

### Sort once → linear merge

Never sort inside a loop. Collect, sort once, merge in one pass.

```python
# Wrong — O(n²)
for opening in openings:
    for axis in axes:
        if overlaps(opening, axis):
            ...

# Right — O(n log n) + O(n)
sorted_openings = sorted(openings, key=lambda o: o.u0)
sorted_axes = sorted(axes)
# single linear merge pass
```

This pattern applies everywhere axes, z-levels, and opening intervals interact.

### Interval union before conflict checks

Unionize intervals before checking conflicts. Never check each member against each opening separately.

```python
# Derive union of opening intervals per wall
opening_union = _union_intervals([(o.u0, o.u1) for o in openings if o.wall == wall])

# Check members against disjoint union — O(n) not O(n²)
for post in posts:
    if _in_union(post.u, opening_union):
        # handle conflict
```

### Generators and early exit

Use generators for pipeline stages where not all elements may be needed. Use `any()`, `all()`, `next(..., None)` for early exit.

```python
# Early exit — stops at first conflict
has_conflict = any(collides(m, opening) for m in members for opening in openings)

# Generator pipeline — lazy, composable
valid_members = (m for m in candidates if not _in_opening(m, opening_union))
```

Use `itertools` for standard operations: `chain` for concatenating member groups, `pairwise` for adjacent axis pairs, `groupby` for wall-grouped operations.

### `match` for structural dispatch

Use Python's `match` statement for dispatching on role, member type, or issue severity. It is more explicit than `if/elif` chains and statically checkable.

```python
match member.role:
    case "corner":
        section = policy.corner_section
    case "stud":
        section = policy.stud_section
    case "king_post":
        section = policy.king_post_section
    case _:
        raise SchemaError(f"Unknown member role: {member.role!r}")
```

---

## 12. Testing

### What gets tested

Every function with a postcondition gets a test. The test verifies the postcondition, not the implementation.

Mandatory test coverage:
- All `derive_*` functions: output structure, member counts, coordinate correctness
- All `validate_*` functions: known-good input passes, known-bad input produces correct Issue
- All `assert_*` functions: violation raises correct exception type
- All `resolve_*` functions: determinism (same input → identical output across runs)
- Pipeline stages: precondition → postcondition chain

### Blender-free tests

All Core, Domain-core, and type module tests run without Blender. Tests that require `bpy` are isolated in `tests/blender/` and run separately.

### Determinism tests

Every deterministic function has a snapshot test:

```python
def test_derive_frameplan_deterministic():
    fp1 = derive_frameplan(structure, policy, seed=Seed(1, 1, 42))
    fp2 = derive_frameplan(structure, policy, seed=Seed(1, 1, 42))
    assert fp1 == fp2  # frozen dataclass equality
```

Golden snapshots for known seeds (e.g. Hallenhaus seed=123) must not change without an explicit CHANGELOG entry — SYS_CONTRACT §8.2.

### Test naming

```
test_<function>_<condition>_<expected>
```

Examples:
- `test_derive_posts_no_openings_returns_full_grid`
- `test_validate_posts_missing_corner_returns_hard_issue`
- `test_assert_members_complete_empty_posts_raises_schema_error`

---

## 13. Logging

### Level semantics

| Level | When to use |
|-------|-------------|
| `DEBUG` | Internal values: axis coordinates, member parameters, policy patch values, seed derivations. Never active in production. |
| `INFO` | Stage completions: "PolicyStack resolved", "FramePlan generated: 47 members". Useful during development of new house types. |
| `WARNING` | Repairs, SOFT Issues, availability warnings, unexpected but handled states. Always active. Always includes context. |
| `ERROR` | HARD Issues, contract violations, generation stopped. Always active. |
| `CRITICAL` | Not used. Raise instead. |

### Logger naming

Loggers follow the module hierarchy via `__name__`:

```python
import logging
log = logging.getLogger(__name__)
# Results in: bvillage.domains.fachwerk.core.derive_frameplan
```

This enables granular runtime control:

```python
# Production — warnings and errors only
logging.getLogger("bvillage").setLevel(logging.WARNING)

# Development — full pipeline trace
logging.getLogger("bvillage").setLevel(logging.INFO)

# Targeted debugging of one subsystem
logging.getLogger("bvillage.domains.fachwerk").setLevel(logging.DEBUG)
logging.getLogger("bvillage").setLevel(logging.WARNING)
```

**Two legitimate exceptions to `__name__`:**

*Configuration functions* — `logging_conf.py` intentionally uses `getLogger("bvillage")` to configure the project root logger. A hardcoded name is correct here because the goal is to target a specific logger tree by name, not to identify the calling module. The signal: `setLevel`, `addHandler`, or `removeHandler` is called on the same variable.

*Tests* — hardcoded logger names in tests are deliberate. Tests for logging configuration must reference specific logger names to assert correct behaviour (e.g. `getLogger("bvillage.test")`). The `__name__` rule does not apply in `tests/`.

The ARCH_SCAN enforces this distinction automatically.

### Lazy evaluation — mandatory in hot paths

Never construct log strings unconditionally. The logger checks the level, but string construction happens before the check.

```python
# Wrong — string always constructed
log.debug(f"post at u={u:.4f}, wall={wall}, role={role}")

# Right — string only constructed if DEBUG is active
log.debug("post at u=%s, wall=%s, role=%s", u, wall, role)
```

This is especially important in hot path functions where DEBUG may be active during development.

### WARNING context

Every WARNING log includes: what was repaired or unexpected, where (wall, member, stage), and what value resulted.

```python
log.warning(
    "z-axis repair: snapped z=%.4f to nearest grid level %.4f (wall=%s)",
    original_z, snapped_z, wall
)
```

---

## 14. Performance priorities

Optimize in this order. Do not skip levels.

**1. Algorithmic** — correct complexity class. O(n log n) where O(n²) is avoidable. Sort-once, interval-union, early exit. This is always worth doing.

**2. Data structure** — `frozen=True, slots=True`, `tuple` over `list`, `set` for membership. These are defaults, not optimizations.

**3. Measured** — profile first with `cProfile` or `time.perf_counter`. Optimize only what profiling identifies as a bottleneck. Document what was measured and what changed.

Micro-optimizations (local variable binding, itertools replacement of manual loops) only after profiling confirms a hot spot. Readability is not sacrificed for speculative performance gains.

---

## 15. What good code looks like

A function is acceptable when:

- Type hints are complete on all parameters and return value
- Docstring states what it does, its preconditions and postconditions, and what it raises
- It has exactly one testable purpose
- It is pure or its side effects are explicit and justified
- It uses `tuple` for completed collections
- It does not construct log strings unconditionally
- A test exists that verifies its postcondition

A module is acceptable when:
- `__all__` is defined
- It has at most three public functions
- Its name follows `<role>_<aspect>.py`
- It does not import across layer boundaries
- The first line is the canonical path comment

---

## 16. AI-assisted development

BVILLAGE uses AI for code generation. All rules governing AI-assisted
contributions — integrity constraints, stop conditions, vocabulary discipline,
session continuity, and the HANDOFF protocol — are defined in:

**`ENG_AI_CONTRIBUTION_RULES.md`** (Tier 3 — Operational, Mandatory)

That document is the single source of truth for AI contribution behavior.
The rules are not repeated here. In any conflict between a convention in
this guide and a rule in `ENG_AI_CONTRIBUTION_RULES.md`, the latter governs.
