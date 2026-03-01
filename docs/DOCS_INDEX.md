# BVILLAGE – Documentation Index

---
tier: 3
authority: OPERATIONAL
change-frequency: on-document-change
change-rule: Update when documents are added, superseded, or reorganized. Status field must be kept current.
referenced-by: SYS_WORKFLOW.md, DEV_ROADMAP.md
references: —
---

This index is the entry point for the documentation system. It defines reading order, document status, and the relationship between documents. Read this before reading anything else.

---

## Reading order — new contributor

Read in this sequence. Each document assumes the ones before it.

1. **SYS_PRINCIPLES.md** — why the system is designed this way. The decisions that are no longer up for debate.
2. **SYS_VISION.md** — where the system is going. The large picture that governs architectural decisions today.
3. **SYS_CONCEPTS.md** — what the system is and how it thinks. The conceptual model.
4. **SYS_CONTRACT.md** — what every module must and must not do. The enforceable rules.
5. **ARCH_POLICIES.md** — how building variation is structured. The policy axis system.
6. **ARCH_TAXONOMY.md** — the catalogue of known building types and their IDs.
7. **ARCH_MATERIALS.md** — the material system: physical and visual parameters.
8. **ENG_CODING_GUIDE.md** — how to write Python in this project.
9. **ENG_BUILDER_CONTRACT.md** — specific rules for Blender builder modules.
10. **ENG_AI_CONTRIBUTION_RULES.md** — mandatory integrity rules for AI-assisted contributions.

---

## Reading order — development session

For a focused coding session, the minimum context is:

1. SYS_CONTRACT.md (rules)
2. ENG_CODING_GUIDE.md (conventions)
3. ARCH_SCAN output (current codebase state)
4. Relevant domain or type files as needed

---

## Document status

### Active — current architecture

| Document | Tier | Purpose |
|----------|------|---------|
| SYS_PRINCIPLES.md | 1 — Canonical | Foundational decisions. Changes require CHANGELOG entry. |
| SYS_CONCEPTS.md | 1 — Canonical | Conceptual model. Changes require CHANGELOG entry. |
| SYS_CONTRACT.md | 1 — Canonical | Enforceable rules. Changes require schema review. |
| SYS_VISION.md | 2 — Reference | Large-picture vision and long-range architectural intent. Living document — grows with research and discussion. |
| ARCH_POLICIES.md | 2 — Reference | Policy axis system. Expandable by new axes. |
| ARCH_TAXONOMY.md | 2 — Reference | Building type catalogue. Expandable by new entries. |
| ARCH_MATERIALS.md | 2 — Reference | Material system. Expandable by new species and subtypes. |
| ENG_CODING_GUIDE.md | 3 — Operational | Python conventions. Additions welcome; changes require team decision. |
| ENG_BUILDER_CONTRACT.md | 3 — Operational | Builder rules. Changes only on schema increment. |
| ENG_PERFORMANCE_GUIDE.md | 3 — Operational | Performance patterns. Independent of architecture. |
| ENG_AI_CONTRIBUTION_RULES.md | 3 — Operational | Mandatory integrity rules for AI-assisted contributions. Session continuity protocol. |
| DEV_ROADMAP.md | 3 — Operational | Tasks and milestones. Frequently updated. |
| SYS_WORKFLOW.md | 3 — Operational | Collaboration process. Rarely changes. |
| SYS_NAMING_POLICY.md | 3 — Operational | File and function naming rules. Enforced by ARCH_SCAN. |
| DOCS_INDEX.md | 3 — Operational | This document. |

### Superseded — replaced by active documents

These documents remain in the repository for reference. They must not be edited. New code must not reference them.

| Document | Superseded by |
|----------|--------------|
| SYS_FOUNDATION.md | SYS_PRINCIPLES.md + SYS_CONCEPTS.md |
| GENERATION_MODEL.md | ARCH_POLICIES.md + SYS_CONCEPTS.md §3 |
| POLICY_AXIS_TAXONOMY.md | ARCH_POLICIES.md |
| Material_System_v0_4_0.md | ARCH_MATERIALS.md |

---

## Tier definitions

| Tier | Authority | What it contains | Change frequency |
|------|-----------|-----------------|-----------------|
| 1 — Canonical | Decisions that govern all other documents | Principles, concepts, contract | Rare — requires CHANGELOG |
| 2 — Reference | Architectural knowledge that grows with research | Taxonomy, policies, materials | On feature — expandable |
| 3 — Operational | Working instructions and process | Guides, roadmap, workflow | As needed |

Tier 1 governs Tier 2. Tier 2 governs Tier 3. In any conflict, the higher tier wins.

`SYS_VISION.md` is a Tier 2 document with a special role: it records intent that has not yet hardened into contract. When a vision item stabilizes into an architectural decision, it migrates into a Tier 1 document. SYS_VISION.md is the incubator, not the authority.

---

## Document ownership

Every document declares its own `tier`, `authority`, `change-frequency`, and `change-rule` in its front matter. Those declarations are authoritative for that document. This index reflects them — it does not override them.
