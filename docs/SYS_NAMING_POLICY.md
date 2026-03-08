# BVILLAGE – Naming Policy

---
tier: 3
authority: OPERATIONAL
change-frequency: rare
change-rule: Changes require explicit team decision. Role semantics changes affect all existing module names — treat as a refactor trigger.
referenced-by: ENG_CODING_GUIDE.md, SYS_CONTRACT.md §12
references: SYS_CONTRACT.md §11, §12
---

This document defines naming conventions for all Python files and functions in BVILLAGE. The rules themselves are stated in SYS_CONTRACT.md §11–12. This document explains the reasoning behind each role and provides the review criteria that make the rules applicable in practice.

---

## 1. Goal

A file or function name must clearly communicate three things:

1. **Layer** — where in the architecture this code lives
2. **Role** — what this code does
3. **Aspect** — which part of the building it concerns

Names must remain understandable after long development pauses and across AI-assisted sessions. A name that requires context to interpret is a weak name.

---

## 2. Layer responsibilities

| Layer | Path pattern | Responsibility |
|---|---|---|
| `core/` | `bvillage/core/` | Engine-agnostic interfaces, data models, registry, utilities. No Blender imports. No architectural semantics. |
| `foreman/` | `bvillage/foreman/` | Coordination, plugin dispatch, conflict resolution. No structural generation. No Blender imports. |
| `types/` | `bvillage/types/<family>/` | Topology planning for a specific archetype family. One family per construction grammar. No structural members. No Blender imports. |
| `domain-core/` | `bvillage/domains/<domain>/core/` | Constructive derivation of structural artifacts. No Blender imports. |
| `domain-blender/` | `bvillage/domains/<domain>/blender/` | Blender geometry emission only. No structural inference. |
| `policies/` | `bvillage/policies/` | Domain-agnostic policy definitions. No generation code. |
| `tests/` | `bvillage/tests/` | Blender-free deterministic tests. |

### Layer boundary rules

- `core/` has no knowledge of any domain, archetype, or construction grammar.
- `foreman/` dispatches by interface only. It never imports concrete plugin implementations.
- `types/` produces `SemanticPlan`. It never generates members.
- `domain-core/` produces `FramePlan` and `RoofPlan`. It never imports Blender.
- `domain-blender/` emits geometry. It makes no structural decisions.
- `policies/` carries parameters. It contains no generation logic.

---

## 3. File naming

Pattern: `<role>_<aspect>.py`

Allowed roles: `plan_`, `derive_`, `build_`, `validate_`, `audit_`, `report_`, `policy_`, `schema_`, `mesh_`

Forbidden generic names: `utils.py`, `helpers.py`, `common.py`, `check.py` — these communicate nothing about layer, role, or aspect.

---

## 4. Role semantics

Each role carries a strict architectural contract. The role prefix signals that contract to any reader.

| Role | Contract |
|---|---|
| `plan_` | Semantic planning only. Produces `SemanticPlan`, `InteriorPlan`, or dispatch decisions. No Blender code. No structural member generation. |
| `derive_` | Constructive artifact computation. Produces `FramePlan`, `RoofPlan`, or structural data. Pure function preferred. No Blender code. |
| `build_` | Blender emission only. No structural inference. Reads members from plans, builds meshes. |
| `validate_` | Returns `Issue` objects. No mutation of any input. |
| `audit_` | Checks and report combined. No mutation. Does not raise. |
| `report_` | Pure formatting. Input → string or structured output. |
| `policy_` | Parameter container or configuration logic. No generation code. |
| `schema_` | Data model definitions. Dataclasses, type aliases, constants. Includes interface `Protocol` definitions. |
| `mesh_` | Low-level Blender mesh helpers. Called only from `build_` modules. |

Violating the role contract — e.g. a `build_` module that computes structural dimensions — is an architectural violation, not a style issue.

---

## 5. Pipeline role convention

The pipeline roles defined in SYS_CONCEPTS.md §3 are the conceptual vocabulary of the system. They appear in documentation, comments, and discussions. They do not directly determine file names — file names follow the `<role>_<aspect>.py` pattern above.

The mapping between pipeline roles and file roles:

| Pipeline role | File role | Example file |
|---|---|---|
| Commissioner | — | implemented in `SettlementBuilder` caller code |
| Foreman | `plan_` | `foreman/plan_dispatch.py` |
| Topology Planner | `plan_` | `types/fw_longhouse/plan_topology.py` |
| Frame Producer | `derive_` | `domains/fachwerk/core/derive_frameplan_boxframe.py` |
| Roof Producer | `derive_` | `domains/fachwerk/core/derive_roofplan.py` |
| Joiner | `plan_` | `domains/fachwerk/core/plan_interior.py` |
| Inspector | `validate_` | `core/validate_physics.py` |
| Appraiser | `audit_` | `core/audit_candidates.py` |
| Renderer | `build_` | `domains/fachwerk/blender/build_frameplan.py` |

---

## 6. Domain-specific role naming convention

Within a domain plugin, concrete implementations of pipeline roles follow a readable naming convention that identifies both the domain and the construction grammar. This is a convention, not a contract enforced by Core.

Pattern for Frame Producers: `<ConstructionGrammar>FrameProducer`

Current timber frame implementations:

| Construction grammar | Class name |
|---|---|
| `BOX_FRAME` | `BoxFrameProducer` |
| `STOREY_FRAME` | `StoreyFrameProducer` |
| `CRUCK_FRAME` | `CruckFrameProducer` |
| `AISLED_FRAME` | `AisledFrameProducer` |
| `WALL_GRID_FRAME` | `WallGridFrameProducer` |

Pattern for Topology Planners: `<Family>TopologyPlanner`

Current timber frame families:

| Family | Class name |
|---|---|
| `fw_longhouse` | `LonghouseTopologyPlanner` |
| `fw_townhouse` | `TownhouseTopologyPlanner` |
| `fw_crosshall` | `CrosshallTopologyPlanner` |
| `fw_courtyard` | `CourtyardTopologyPlanner` |
| `fw_cruck` | `CruckTopologyPlanner` |
| `fw_aisled` | `AisledTopologyPlanner` |

These names are domain-internal. Core knows only the interfaces `IFrameProducer` and `ITopologyPlanner`. A developer outside the fachwerk domain does not need to know these names.

---

## 7. Function naming

Pattern: `<verb>_<object>_<qualifier>()`

| Verb | Meaning |
|---|---|
| `plan_` | Produces a semantic plan. No structural artifacts. |
| `derive_` | Computes structural data from inputs. Pure. |
| `build_` | Emits Blender geometry. |
| `normalize_` | Transforms data into canonical form. |
| `validate_` | Returns Issue objects. No raise. |
| `audit_` | Returns a report. No raise. No mutation. |
| `assert_` | Enforces an invariant. May raise from BVillageError hierarchy. |

Public API per module: maximum three functions. All other functions are private (leading underscore).

---

## 8. Path header rule

Every `.py` file must start with its canonical project path as the first line:

```python
# bvillage/domains/fachwerk/core/derive_frameplan_boxframe.py
```

No docstring may precede this line. During refactors, this line must be updated to match the new location. See SYS_CONTRACT.md §11.

---

## 9. Migration

Existing files that violate this convention must be renamed in the controlled refactor window defined in the roadmap. No mixed conventions are allowed in new files. New files must follow this policy from the first commit.

---

## 10. Review test

A name passes review only if all three questions have obvious answers without reading the file:

- Which layer does this code belong to?
- What does this code do?
- Which part of the building does it concern?

Naming clarity is part of architectural stability. A codebase where names require explanation is a codebase that accumulates hidden coupling.
