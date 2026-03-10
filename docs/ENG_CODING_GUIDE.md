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

### Naming conventions

Python naming follows standard conventions throughout. No exceptions.

| What | Convention | Examples |
|------|-----------|---------|
| Functions | `snake_case` | `derive_posts`, `_build_opening_zones` |
| Variables | `snake_case` | `opening_zones`, `wall_by_id` |
| Classes | `PascalCase` | `FramePlan`, `ResolvedPolicy`, `BayFrame` |
| Constants | `UPPER_SNAKE_CASE` | `_QUANT = 1_000`, `AXIS_MERGE_TOL` |
| Private | leading `_` | `_derive_post_candidates`, `_QUANT` |
| Type aliases | `PascalCase` | `WallId = str`, `AxisList = tuple[float, ...]` |

`camelCase` is never used. In Python it signals foreign code — JavaScript, Java, or auto-generated bindings. BVILLAGE is Python.

One subtlety: module-level constants that are implementation details of a single module take a leading underscore even in `UPPER_SNAKE_CASE` form: `_QUANT`, `_TOL`. Constants that are part of the public API of a module do not: `AXIS_MERGE_TOL` in `geom_eps.py`.

File and function naming follows the `<role>_<aspect>.py` / `<verb>_<object>` convention defined in `SYS_NAMING_POLICY.md`. This section covers only Python identifier conventions.

### Guard clauses and early exit

Flat is better than nested. When a function must check several preconditions before doing real work, each check exits immediately on failure. The happy path runs at the outermost indentation level.

```python
# Wrong — three levels deep before real work begins
def derive_brace(wall: Wall, policy: ResolvedPolicy) -> Brace | None:
    if wall is not None:
        if len(wall.posts) >= 2:
            if policy.brace_enabled:
                return _compute_brace(wall, policy)
    return None

# Right — guards exit early, real work is flat
def derive_brace(wall: Wall, policy: ResolvedPolicy) -> Brace | None:
    if wall is None:
        return None
    if len(wall.posts) < 2:
        return None
    if not policy.brace_enabled:
        return None
    return _compute_brace(wall, policy)
```

The rule: every guard clause is one condition, one exit. The function body that follows reads without mental stack — no open `if` blocks to track, no indentation to parse.

The same principle applies in validation functions, where each failing condition appends an Issue and continues:

```python
def validate_wall(wall: Wall, structure: StructurePlan) -> tuple[Issue, ...]:
    issues: list[Issue] = []
    if not wall.posts:
        issues.append(Issue(severity="HARD", message=f"Wall {wall.id!r} has no posts"))
    if wall.width < policy.min_wall_width:
        issues.append(Issue(severity="SOFT", message=f"Wall {wall.id!r} width below minimum"))
    return tuple(issues)
```

Here there is no early exit — validation collects all problems. But each check is still flat: one condition, one append.

### Performance tiers

Two tiers exist in BVILLAGE with different priorities:

**Hot path functions** — called repeatedly during generation (member derivation, axis merging, policy resolution). Mark explicitly:

```python
# HOT PATH — keep allocation-free, no logging, no defensive checks
def _merge_axes(primary: tuple[float, ...], secondary: tuple[float, ...], tol: float) -> tuple[float, ...]:
    ...
```

Hot path rules: no f-strings, no logging, no defensive allocation, use generators and early exit, profile before optimizing further.

**Structural functions** — complex logic called once per generation (FramePlan derivation, PolicyStack resolution, Joiner). Readability first. Document invariants fully. Performance matters only at algorithmic level — correct complexity class, no O(n²) where O(n log n) is possible.

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

## 5b. String formatting

Three formatting mechanisms exist in Python. BVILLAGE uses each in exactly one context.

**f-strings** — everywhere except hot paths and logging.

```python
raise SchemaError(f"Unknown member role {member.role!r} on wall {member.wall!r}")
component_id = f"{self.world}:{self.settlement}:{self.house_salt}:{component}"
```

f-strings are readable, fast enough for non-hot-path use, and the natural choice when the expression is simple. Use `!r` for values that should be quoted in output (IDs, role names, keys) — it makes the boundary between prose and value visible.

**`%`-format** — logging only.

```python
log.debug("post at u=%s, wall=%s, role=%s", u, wall, role)
log.warning("z-axis repair: snapped %.4f → %.4f (wall=%s)", original_z, snapped_z, wall)
```

The Python logging system evaluates `%`-format arguments lazily — only if the log level is active. f-strings are evaluated unconditionally at the call site. In hot paths where DEBUG may be active during development, this difference matters. The rule is absolute: all `log.*()` calls use `%`-format, never f-strings.

**String concatenation** — never in loops.

```python
# Wrong — O(n²) allocations
result = ""
for member in members:
    result += member.id + ", "

# Right — O(n) join
result = ", ".join(m.id for m in members)
```

String objects are immutable. Each `+=` allocates a new object. `str.join()` allocates once. Outside loops, `+=` on two or three strings is fine — the cost is negligible and the code is readable.

**No string formatting in core geometry code.** String operations have no place in functions that derive axes, compute positions, or generate members. If a hot-path function is constructing strings, it is doing the wrong thing.



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

### Short-circuit evaluation

Python's `and`/`or` operators evaluate left to right and stop as soon as the result is determined. Use this deliberately.

```python
# Guard with cheap check first
if wall and wall.posts and _has_valid_span(wall, policy):
    ...

# Default without explicit None check
section = policy.override_section or _default_section(role, policy)

# First match from candidates
first_valid = next((m for m in members if _is_corner(m)), None)
```

The ordering principle: put the cheapest check first, the most expensive last. An attribute access costs nothing; a function call costs something; a function that iterates a collection costs more. Short-circuit evaluation makes ordering matter.

`next(..., None)` is the idiomatic alternative to `filter` + first element when only one result is needed. It stops at the first match — O(1) in the best case, O(n) in the worst, never allocates a filtered collection.

---

## 11b. Code signature — intention and clarity

BVILLAGE code has a recognizable style. Not clever. Not defensive. Clear and purposeful — the code of someone who knows exactly what they are building.

Three principles define it.

### Intention transparency

Code expresses *what it wants*, not *how it does it*. Names describe decisions, not operations.

```python
# Weak — describes mechanism
posts = tuple(p for p in candidates if not _in_union(p.u, opening_union))

# Strong — expresses intent
free_positions = _exclude_opening_zones(candidates, opening_union)
posts           = tuple(free_positions)
```

Function names follow the same principle: `derive_posts` not `compute_post_list`, `resolve_policy_stack` not `get_policies`, `exclude_opening_zones` not `filter_by_union`.

### Structural honesty

The pipeline structure must be visible at a glance. Each step in a complex function is a sentence — a named intermediate result that says what it is.

```python
def derive_frameplan(structure: StructurePlan, policy: ResolvedPolicy) -> FramePlan:
    post_candidates = _derive_post_candidates(structure, policy)
    opening_zones   = _build_opening_zones(structure)
    posts           = _exclude_opening_zones(post_candidates, opening_zones)
    rails           = _derive_rails(structure, policy, posts)
    braces          = _derive_braces(structure, policy, posts)
    return FramePlan(posts=posts, rails=rails, braces=braces)
```

A function that generates a building should be readable as a five-sentence summary of the generation process. A reader who knows nothing of the internals can follow it.

### Symmetry for parallel concepts

When functions operate on structurally similar things, they look structurally similar. Same verb, same parameter order, same indentation rhythm.

```python
posts  = _derive_posts(structure, policy, opening_zones)
rails  = _derive_rails(structure, policy, posts)
braces = _derive_braces(structure, policy, posts, rails)
```

Not one `derive_`, one `compute_`, one `build_` for the same operation type. The eye should land on the differences — inputs grow as the pipeline progresses — not hunt through surface variation.

### Walrus operator for single-use calculations

Use `:=` when a value is computed solely to be tested, and the name makes the condition readable:

```python
if not (candidates := _derive_candidates(structure, policy)):
    raise SchemaError(f"No post candidates for structure {structure.id!r}")
```

Do not use it when the name adds no clarity over writing two separate lines.

### Comprehensions — when yes, when no

A comprehension is readable when the expression can be spoken aloud as a single sentence without losing meaning.

```python
# Yes — one sentence, clear intent
posts = tuple(Post(wall=w, u=u, role=r) for w, u, r in _axis_triples(structure, policy))

# No — needs explanation, should be a named function
posts = tuple(
    Post(wall=w, u=u, role=r)
    for w in structure.walls
    for u in _axes_for_wall(w, policy)
    for r in (_role(u, w, policy),)
    if not _in_union(u, _opening_zones(w))
)
```

When the comprehension exceeds two logical clauses, extract the body into a named private function. The comprehension becomes the call site; the logic lives where it can be tested.

### Errors as documents

Every raised exception tells the reader what happened, what was expected, and what to do about it.

```python
raise PolicyError(
    f"Unknown patch key {key!r} in {policy_name!r}. "
    f"Valid keys: {sorted(canonical_keys)}. "
    f"Add the key to the canonical tree or remove it from the patch."
)
```

An error message that requires a debugger to interpret is an incomplete error message.

### `__post_init__` for dataclass invariants

When a dataclass has an invariant — a condition that must always hold — enforce it at construction:

```python
@dataclass(frozen=True, slots=True)
class RangeHard:
    min_v: float
    max_v: float

    def __post_init__(self) -> None:
        if self.min_v >= self.max_v:
            raise SchemaError(
                f"RangeHard: min_v={self.min_v} must be strictly less than max_v={self.max_v}"
            )
```

This guarantees that any instance in existence is valid. No external caller can create an invalid range and pass it deeper into the pipeline.

### `@property` for derived values

When a value belongs conceptually to a dataclass but is computed from its fields, use `@property` rather than a free function:

```python
@dataclass(frozen=True, slots=True)
class WallSegment:
    u_range: Range2
    z_range: Range2

    @property
    def width(self) -> float:
        return self.u_range.max_v - self.u_range.min_v

    @property
    def height(self) -> float:
        return self.z_range.max_v - self.z_range.min_v
```

The test: if a value is always derived from the same fields in the same way and has no independent existence, it belongs on the object. If it requires additional context or policy, it belongs in a `derive_*` function.

---

## 11c. Algorithmic patterns

These patterns apply to the specific problems BVILLAGE solves. They are not generic best practices — each one maps to a concrete recurring situation in the codebase.

### Binary search for interval membership — `bisect`

After building an interval union with `_union_intervals`, searching it should use binary search, not linear scan. The union is sorted and non-overlapping by construction — exactly the precondition `bisect` requires.

```python
import bisect

def _in_union(u: float, zones: tuple[tuple[float, float], ...]) -> bool:
    """Tests membership in a sorted, non-overlapping interval union.

    Uses binary search — O(log n), not O(n).
    Precondition: zones is sorted and non-overlapping (output of _build_opening_zones).
    """
    if not zones:
        return False
    lows = tuple(lo for lo, _ in zones)
    idx  = bisect.bisect_right(lows, u) - 1
    if idx < 0:
        return False
    _, hi = zones[idx]
    return u <= hi + geom_eps.AXIS_MERGE_TOL
```

At single-house scale the difference is negligible. The pattern is documented here because it is correct regardless of scale — and because the precondition (sorted, non-overlapping) is already guaranteed by the union-build step.

### Sweep-line for axis merge

Merging two sorted axis sequences into one deduplicated sequence is a sweep: sort once, then walk forward keeping only values that are further than the tolerance from the last accepted value.

```python
# HOT PATH — keep allocation-free, no logging, no defensive checks
def _merge_axes(
    primary:   tuple[float, ...],
    secondary: tuple[float, ...],
    tol:       float,
) -> tuple[float, ...]:
    """Merges two sorted axis sequences, deduplicating within tolerance.

    O(n + m) after the initial sort — single forward sweep.
    """
    merged = sorted(set(primary) | set(secondary))
    if not merged:
        return ()
    result = [merged[0]]
    for u in merged[1:]:
        if u - result[-1] > tol:
            result.append(u)
    return tuple(result)
```

The pattern: **sort once, sweep once.** Never revisit earlier elements. This applies to every axis operation in the system — axes_u, axes_z, opening interval boundaries.

### Lookup tables before the main loop

When the same lookup is performed inside a loop, build the table before the loop — not inside it.

```python
# Wrong — O(walls × members) total
for member in members:
    wall = next(w for w in structure.walls if w.id == member.wall)

# Right — O(walls) build, O(1) lookup, O(members) main pass
wall_by_id: dict[str, Wall] = {w.id: w for w in structure.walls}
for member in members:
    wall = wall_by_id[member.wall]
```

This is not an optimization — it is the correct algorithm. The lookup table expresses what the code actually needs: a map from ID to object. The loop-search version obscures this.

The pattern applies to every repeated lookup in the pipeline: walls by ID, sections by role, openings by wall, material variants by ID.

### `accumulate` for cumulative positions

Axis positions computed from spans or heights are cumulative sums. Use `itertools.accumulate` — it expresses the intent and avoids the O(n²) naive approach.

```python
from itertools import accumulate

# Bay axes from span widths
spans  = (3.2, 3.5, 3.2, 3.5, 3.2)
axes_u = (0.0,) + tuple(accumulate(spans))
# → (0.0, 3.2, 6.7, 9.9, 13.4, 16.6)

# Z-levels from storey heights
heights = (2.8, 2.6, 1.4)   # ground floor, upper floor, knee wall
axes_z  = (0.0,) + tuple(accumulate(heights))
# → (0.0, 2.8, 5.4, 6.8)
```

The naive alternative — `sum(spans[:i]) for i in range(len(spans)+1)` — recomputes the partial sum from zero each iteration: O(n²) for O(n) work.

### `defaultdict` for incremental grouping

When a grouped structure is built incrementally — one element at a time from a flat source — use `defaultdict` for the build phase and convert to a frozen structure before returning.

```python
from collections import defaultdict

# Build phase — mutable is correct here
openings_by_wall: defaultdict[str, list[Opening]] = defaultdict(list)
for opening in raw_openings:
    openings_by_wall[opening.wall].append(opening)

# Freeze before returning — sorted for determinism
return {
    wall: tuple(sorted(ops, key=lambda o: o.u_range.min_v))
    for wall, ops in openings_by_wall.items()
}
```

`defaultdict` internally; `dict[str, tuple[...]]` at the boundary. The conversion also imposes the sort that determinism requires — an unsorted group is a hidden ordering dependency.

### `zip` for parallel structures

When two sequences correspond element-by-element, `zip` makes that relationship explicit.

```python
# Pair axis intervals with their bay IDs
for (u_lo, u_hi), bay_id in zip(pairwise(axes_u), bay_ids):
    width = u_hi - u_lo
    frame = BayFrame(bay_index=bay_id, u_lo=u_lo, u_hi=u_hi, width=width)
```

`zip` signals: these two sequences are structurally coupled. A reader immediately understands the relationship without tracking an index. Never use `range(len(...))` when `zip` expresses the intent.

### Float quantization for stable keys

When float coordinates must be used as dictionary keys or set members — for deduplication outside the normal tolerance-based merge — quantize to an integer key rather than comparing with `==`.

```python
_QUANT = 1_000  # 1 mm precision at metre coordinates

def _quantize(u: float) -> int:
    """Converts a float coordinate to a stable integer key at 1mm precision."""
    return round(u * _QUANT)
```

Sets and dicts have no notion of tolerance. Two floats that are geometrically identical but differ in the last bit will be treated as distinct keys. Quantization removes the ambiguity by collapsing the precision explicitly.

Use only where deduplication is the goal. Geometric comparisons in validation and member placement still use `geom_eps` — the tolerance is the contract there, not the deduplication.

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
# Results in: bvillage.domains.timber_frame.core.derive_frameplan
```

This enables granular runtime control:

```python
# Production — warnings and errors only
logging.getLogger("bvillage").setLevel(logging.WARNING)

# Development — full pipeline trace
logging.getLogger("bvillage").setLevel(logging.INFO)

# Targeted debugging of one subsystem
logging.getLogger("bvillage.domains.timber_frame").setLevel(logging.DEBUG)
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

**4. Memoization** — `@lru_cache` for pure, seed-independent functions only.

`@lru_cache` caches return values by input hash. It is global state that persists across calls. In a generation pipeline that builds many houses, this means a result computed for house 1 may be returned to house 2 without recomputation — correct only if the function's output does not depend on the seed.

Two categories exist:

*Safe to cache* — functions whose output depends only on structural parameters, not on the seed. Material physics lookup, policy invariant validation, section area computation:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def _section_area(width_mm: float, height_mm: float) -> float:
    """Returns cross-sectional area. Pure, seed-independent."""
    return width_mm * height_mm
```

*Never cache* — functions that consume `ctx.seed` directly or indirectly. `resolve_policy_stack`, any `derive_*` function, anything involving `NoisePolicy` or material sampling. Caching these would return a result computed under one seed to a caller with a different seed — silent determinism violation.

The test before adding `@lru_cache`: does this function produce identical output for identical inputs regardless of which house, settlement, or world seed is active? If yes, and profiling confirms the function is called repeatedly with identical inputs, cache it. If any doubt — do not cache.

Document every cached function with a comment stating why it is safe:

```python
@lru_cache(maxsize=128)
def resolve_material_physics(material_id: str) -> MaterialPhysics:
    # WHY: material physics are fixed by ID — no seed dependency.
    # Safe to cache across all houses in a settlement.
    ...
```

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
