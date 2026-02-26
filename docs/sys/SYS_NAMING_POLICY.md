# BVILLAGE Naming Policy
Version: 0.1
Status: ACTIVE

## 0. Goal
A file or function name must clearly communicate:
1) Layer (core / type / domain-core / domain-blender / tests)
2) Role (plan / derive / build / validate / audit / report / policy / schema / mesh)
3) Aspect (frameplan / openings / axes_u / infills / roof / etc.)

Names must remain understandable after long development pauses.

---

## 1. Layer Responsibilities

### core/
Engine-agnostic, stable, no Blender imports.

### types/<type_id>/
Topological planning and orchestration.

### domains/<domain>/core/
Constructive derivation of structural artifacts.

### domains/<domain>/blender/
Blender geometry emission only.

### tests/
Blender-free deterministic tests.

---

## 2. File Naming Pattern

Standard pattern:

<role>_<aspect>.py

Allowed roles:
- plan_
- derive_
- build_
- validate_
- audit_
- report_
- policy_
- schema_
- mesh_

Forbidden generic names:
- utils.py
- helpers.py
- common.py

(Exception: legacy files must be scheduled for refactor.)

---

## 3. Role Semantics (Contract)

### plan_
Semantic planning only. No Blender code.

### derive_
Constructive artifact computation. No Blender code.

### build_
Blender emission only. No structural inference.

### validate_
Returns Issue objects. No mutation.

### audit_
Checks + report. No mutation.

### report_
Pure formatting.

### policy_
Parameter container / configuration logic.

### mesh_
Low-level Blender mesh helpers.

---

## 4. Function Naming

Pattern:

<verb>_<object>_<qualifier>()

Allowed verbs:
- plan_
- derive_
- build_
- normalize_
- validate_
- audit_
- assert_

Public API per module: max 1–3 functions.
Helper functions must be private (leading underscore).

---

## 5. Path Header Rule

Every Python file must start with:

# bvillage/<exact/path>.py

No docstring may precede this line.

---

## 6. Migration Rule

Existing files that violate this convention must be renamed in a controlled refactor phase.
No mixed conventions are allowed in new files.

---

## 7. Review Rule

A name is acceptable only if:
- Layer is obvious
- Role is obvious
- Aspect is obvious
- No architectural boundary is blurred

Naming clarity is part of architectural stability.

