# BVILLAGE – Naming Policy

---
tier: 3
authority: OPERATIONAL
change-frequency: rare
change-rule: Changes require explicit team decision. Role semantics changes affect all existing module names — treat as a refactor trigger.
referenced-by: ENG_CODING_GUIDE.md, SYS_CONTRACT.md §11
references: SYS_CONTRACT.md §10, §11
---

This document defines naming conventions for all Python files and functions in BVILLAGE. The rules themselves are stated in SYS_CONTRACT.md §10–11. This document explains the reasoning behind each role and provides the review criteria that make the rules applicable in practice.

---

## 1. Goal

A file or function name must clearly communicate three things:

1. **Layer** — where in the architecture this code lives (core / type / domain-core / domain-blender / tests)
2. **Role** — what this code does (plan / derive / build / validate / audit / report / policy / schema / mesh)
3. **Aspect** — which part of the building it concerns (frameplan / openings / axes_u / infills / roof / ...)

Names must remain understandable after long development pauses and across AI-assisted sessions. A name that requires context to interpret is a weak name.

---

## 2. Layer responsibilities

| Layer | Path pattern | Responsibility |
|-------|-------------|----------------|
| `core/` | `bvillage/core/` | Engine-agnostic stable data models and utilities. No Blender imports. |
| `type/` | `bvillage/types/<type_id>/` | Topological planning and orchestration for a specific archetype. |
| `domain-core/` | `bvillage/domains/<domain>/core/` | Constructive derivation of structural artifacts. No Blender imports. |
| `domain-blender/` | `bvillage/domains/<domain>/blender/` | Blender geometry emission only. No structural inference. |
| `tests/` | `bvillage/tests/` | Blender-free deterministic tests. |

---

## 3. File naming

Pattern: `<role>_<aspect>.py`

Allowed roles: `plan_`, `derive_`, `build_`, `validate_`, `audit_`, `report_`, `policy_`, `schema_`, `mesh_`

Forbidden generic names: `utils.py`, `helpers.py`, `common.py`, `check.py` — these communicate nothing about layer, role, or aspect.

---

## 4. Role semantics

Each role carries a strict architectural contract. The role prefix signals that contract to any reader.

| Role | Contract |
|------|----------|
| `plan_` | Semantic planning only. No Blender code. No structural member generation. |
| `derive_` | Constructive artifact computation. Pure function preferred. No Blender code. |
| `build_` | Blender emission only. No structural inference. Reads members, builds meshes. |
| `validate_` | Returns `Issue` objects. No mutation of any input. |
| `audit_` | Checks and report combined. No mutation. Does not raise. |
| `report_` | Pure formatting. Input → string or structured output. |
| `policy_` | Parameter container or configuration logic. No generation code. |
| `schema_` | Data model definitions. Dataclasses, type aliases, constants. |
| `mesh_` | Low-level Blender mesh helpers. Called only from `build_` modules. |

Violating the role contract — e.g. a `build_` module that computes structural dimensions — is an architectural violation, not a style issue.

---

## 5. Function naming

Pattern: `<verb>_<object>_<qualifier>()`

| Verb | Meaning |
|------|---------|
| `plan_` | Produces a semantic plan. No structural artifacts. |
| `derive_` | Computes data from inputs. Pure. |
| `build_` | Emits Blender geometry. |
| `normalize_` | Transforms data into canonical form. |
| `validate_` | Returns Issue objects. No raise. |
| `audit_` | Returns a report. No raise. No mutation. |
| `assert_` | Enforces an invariant. May raise from BVillageError hierarchy. |

Public API per module: maximum three functions. All other functions are private (leading underscore).

---

## 6. Path header rule

Every `.py` file must start with its canonical project path as the first line:

```python
# bvillage/domains/fachwerk/core/derive_frameplan.py
```

No docstring may precede this line. During refactors, this line must be updated to match the new location. See SYS_CONTRACT.md §10.

---

## 7. Migration

Existing files that violate this convention must be renamed in the controlled refactor window defined in the roadmap. No mixed conventions are allowed in new files. New files must follow this policy from the first commit.

---

## 8. Review test

A name passes review only if all three questions have obvious answers without reading the file:

- Which layer does this code belong to?
- What does this code do?
- Which part of the building does it concern?

Naming clarity is part of architectural stability. A codebase where names require explanation is a codebase that accumulates hidden coupling.
