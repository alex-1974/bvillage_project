# BVILLAGE CONTRACT MATRIX

## Purpose

This document lists the currently relevant contract and contract-like structures in the active BVILLAGE codebase and maps them to their correct architectural layer.

It reflects the state **after the recent Fachwerk / Hallenhaus contract consolidation round**.

The matrix follows the architectural rule:

> Contracts must live at the lowest layer where they remain valid.

Layer hierarchy:

```text
Core → Domain → Type
```

---

# Contract Layers

| Layer | Responsibility |
|---|---|
| Core | engine-wide artifacts and policy contracts |
| Domain | construction-system contracts and domain validation |
| Type | archetype-specific schema and validation |

---

# CORE CONTRACTS

These contracts define engine artifacts used across the system.

Location:

```text
bvillage/core
```

| Contract | Current Location | Correct Location | Status |
|---|---|---|---|
| `Context` | `core/model.py` | `core/model.py` | OK |
| `StructurePlan` | `core/model.py` | `core/model.py` | OK |
| `InteriorPlan` | `core/model.py` | `core/model.py` | OK |
| `OpeningsPlan` | `core/model.py` | `core/model.py` | OK |
| `Issue` | `core/model.py` | `core/model.py` | OK |
| `ResolvedPolicy` | `core/policy_types.py` | `core/policy_types.py` | OK |
| `ConstraintSpec` | `core/policy_types.py` | `core/policy_types.py` | OK |
| `RangeHardSpec` | `core/policy_types.py` | `core/policy_types.py` | OK |
| `RangeSoftSpec` | `core/policy_types.py` | `core/policy_types.py` | OK |
| `resolve_policy_stack*` | `core/policy_stack.py` | `core/policy_stack.py` | OK |

These remain canonical global contracts and policy machinery. fileciteturn0file10turn0file1

---

# CORE ONTOLOGY CONTRACTS

Location:

```text
bvillage/core/ontology/structural_terms.py
```

| Contract | Role | Status |
|---|---|---|
| Structural Term IDs | canonical semantic identifiers | canonical |
| `POST_PRIMARY` | ontology identifier | OK |
| `POST_HALL` | ontology identifier | OK |
| `BEAM_EAVES_PLATE` | ontology identifier | OK |
| `BEAM_HALL_PLATE` | ontology identifier | OK |
| `BEAM_TIE` | ontology identifier | OK |
| `BRACE_DIAGONAL` | ontology identifier | OK |
| `BRACE_KNEE` | ontology identifier | OK |

Ontology identifiers remain globally stable and are consumed by domain contracts. fileciteturn0file1turn0file10

---

# DOMAIN CONTRACTS — FACHWERK

Location:

```text
bvillage/domains/fachwerk/core
```

| Contract | Current Location | Correct Location | Status |
|---|---|---|---|
| Fachwerk member TID allow-lists | `domains/fachwerk/core/schema_member_tids_fachwerk.py` | `domains/fachwerk/core/schema_member_tids_fachwerk.py` | OK |
| Fachwerk frameplan schema/domain validation | `domains/fachwerk/core/validate_frameplan_fachwerk.py` | `domains/fachwerk/core/validate_frameplan_fachwerk.py` | OK |

### What these domain contracts now cover

- domain-wide allowed member TIDs for Fachwerk posts, rails, and braces
- schema-near validation of the active frameplan payload
- fachwerk-specific member validation
- minimum domain expectations such as non-empty posts and rails

### What they no longer contain

- Hallenhaus-specific frame roles
- Hallenhaus-specific frame-layout validation
- inactive audit paths

This resolves the previous mixed domain/type contract situation. fileciteturn0file1

---

# DOMAIN VALIDATORS

Location:

```text
bvillage/domains/fachwerk/validation
```

| Validator | Current Location | Correct Location | Status |
|---|---|---|---|
| `run_arch_checks` / `log_arch_checks` | `domains/fachwerk/validation/frameplan_checks.py` | `domains/fachwerk/validation/frameplan_checks.py` | OK |

### Current role

This file is now clearly a **lightweight domain sanity validator**, not a parallel contract system.

It:
- returns global `Issue` objects
- checks coarse architectural minima
- logs diagnostics

It no longer uses its own custom `CheckIssue` contract. fileciteturn3file0turn0file10turn0file15

---

# TYPE CONTRACTS — HALLENHAUS

Location:

```text
bvillage/types/fachwerkhaus/hallenhaus
```

| Contract | Current Location | Correct Location | Status |
|---|---|---|---|
| Hallenhaus frame roles | `types/fachwerkhaus/hallenhaus/schema_frame_roles.py` | `types/fachwerkhaus/hallenhaus/schema_frame_roles.py` | OK |
| Hallenhaus frameplan schema | `types/fachwerkhaus/hallenhaus/schema_frameplan_langhaus.py` | `types/fachwerkhaus/hallenhaus/schema_frameplan_langhaus.py` | OK |
| Hallenhaus frameplan type validation | `types/fachwerkhaus/hallenhaus/validate_frameplan_type.py` | `types/fachwerkhaus/hallenhaus/validate_frameplan_type.py` | OK |
| Hallenhaus type validation | `types/fachwerkhaus/hallenhaus/validate.py` | `types/fachwerkhaus/hallenhaus/validate.py` | OK |

### What these type contracts cover

- Hallenhaus-specific frame roles
- Hallenhaus-specific frame-layout semantics
- Hallenhaus-specific frameplan payload structure
- archetype-specific validation separate from Fachwerk domain rules

This matches the intended Type layer much more closely than before. fileciteturn0file0turn0file1

---

# ACTIVE GATE / VALIDATION FLOW

The active validation chain for the Hallenhaus frameplan is now:

```text
architect.py
  ├─ run_arch_checks()                    # lightweight Issue-based sanity checks
  ├─ validate_frameplan_langhaus_schema() # schema-near validation
  ├─ validate_frameplan_langhaus_domain() # fachwerk domain validation
  └─ validate_frameplan_langhaus_type()   # hallenhaus type validation
            │
            ▼
      canonical FramePlan
            │
            ▼
build_frame.py
  └─ boundary guards + rendering only
```

This means the canonical hard gate now lives at the artifact production point (Architect), while the Blender builder no longer carries the primary structural validation path. That aligns better with the system contract that renderers should not become the primary source of structural truth. fileciteturn0file10

---

# BUILDER CONSUMERS

These modules consume contracts but do not define them:

- `domains/fachwerk/blender/build_frame.py`
- `domains/fachwerk/blender/braces.py`
- `domains/fachwerk/blender/infills.py`
- `domains/fachwerk/blender/opening_frames.py`

Their remaining `SchemaError` usage is acceptable insofar as it acts as renderer-side boundary guarding for malformed payloads, not as the canonical validation path.

---

# REMOVED REDUNDANT PATHS

| Contract / File | Status | Note |
|---|---|---|
| `domains/fachwerk/core/frameplan_contract.py` | removed | redundant inactive audit path |
| `domains/fachwerk/core/contract_frameplan_langhaus.py` | removed | mixed domain/type contract replaced by split files |
| Builder-side full call to `validate_frameplan_langhaus(...)` | removed | canonical full validation moved to Architect |
| Custom `CheckIssue` in `frameplan_checks.py` | removed | replaced by global `Issue` |

---

# SUMMARY

After the consolidation round, the contract picture is substantially cleaner:

| Category | Scope | Location |
|---|---|---|
| Core Contracts | engine-wide artifacts and policy contracts | `core/` |
| Domain Contracts | fachwerk construction rules and schema-near validation | `domains/fachwerk/core/` |
| Domain Validators | lightweight sanity checks and logging | `domains/fachwerk/validation/` |
| Type Contracts | hallenhaus-specific schema and frame roles | `types/fachwerkhaus/hallenhaus/` |
| Type Validators | hallenhaus-specific frameplan/type checks | `types/fachwerkhaus/hallenhaus/` |

This is not yet the final end-state for the whole repository, but the most problematic Fachwerk / Hallenhaus contract knot has been untangled.

---

# End of Document
