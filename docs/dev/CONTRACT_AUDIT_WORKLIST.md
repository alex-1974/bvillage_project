# CONTRACT AUDIT WORKLIST

## Scope

This worklist records the practical contract consolidation carried out in the BVILLAGE codebase for the active Fachwerk / Hallenhaus pipeline.

It follows the architectural rule:

> Contracts must live at the lowest layer where they remain valid.

Layer hierarchy:

```text
Core → Domain → Type
```

This document is an implementation audit, not a Tier-1 authority document.

---

## Working architectural decisions used in this audit

1. `schema_version = 4` is the current operative truth for the active Hallenhaus frameplan pipeline.
2. Canonical full validation belongs at the **artifact production point** (Architect), not in the Blender builder.
3. Blender builders may keep **boundary guards** for safe rendering, but must not carry the primary structural validation path.
4. Domain-layer validation may only contain **domain-wide** and **schema-near** rules.
5. Hallenhaus-specific frame-layout validation belongs in the **Type** layer.
6. Redundant parallel contract paths with no active source usage are removal candidates.

---

## Audit table

| Datei | Symbol / Entry | Ist-Zustand | Klasse | Zielort | Problem | Priorität | Aktion / Ergebnis |
|---|---|---|---|---|---|---|---|
| `bvillage/core/policy_stack.py` | `resolve_policy_stack` | aktiver Core-Policy-Pfad | Core Contract | `bvillage/core/policy_stack.py` | kein aktuelles Problem sichtbar | hoch | behalten |
| `bvillage/core/policy_types.py` | `ResolvedPolicy`, `ConstraintSpec`, `RangeHardSpec`, `RangeSoftSpec` | aktiver Core-Policy-Pfad | Core Contract | `bvillage/core/policy_types.py` | kein aktuelles Problem sichtbar | hoch | behalten |
| `bvillage/types/fachwerkhaus/hallenhaus/validate.py` | `validate_type` | Type-Validation vorhanden | Type Validator | `bvillage/types/fachwerkhaus/hallenhaus/validate.py` | grundsätzlich passend platziert | hoch | behalten |
| `bvillage/domains/fachwerk/validation/frameplan_checks.py` | `run_arch_checks`, `log_arch_checks` | aktiver leichter Architekt-Validator | Domain Validator | `bvillage/domains/fachwerk/validation/frameplan_checks.py` | nutzte eigenes `CheckIssue` statt globalem `Issue` | kritisch | **erledigt** — auf globales `Issue` umgestellt |
| `bvillage/domains/fachwerk/blender/build_frame.py` | Vollvalidierungs-Call im Builder | Builder trug redundante Vollvalidierung | Renderer Boundary | `bvillage/domains/fachwerk/blender/build_frame.py` | Builder war letzter harter Gültigkeitsort für gemischte Regeln | kritisch | **erledigt** — Vollvalidierung entfernt, nur Boundary Guards bleiben |
| `bvillage/domains/fachwerk/core/frameplan_contract.py` | `audit_frameplan_contract` | ungenutzter redundanter Auditpfad | Dead Path Candidate | entfernt | konkurrierende Contractwelt ohne aktive Source-Nutzung | kritisch | **erledigt** — Datei entfernt |
| `bvillage/domains/fachwerk/core/contract_frameplan_langhaus.py` | gemischter Contract-Container | mischte Schema, Domain, Type | Mixed Contract File | ersetzt / entfernt | Domain- und Type-Wissen in einer Datei | kritisch | **erledigt** — physisch aufgespalten und entfernt |
| `bvillage/domains/fachwerk/core/schema_member_tids_fachwerk.py` | `ALLOWED_POST_TIDS`, `ALLOWED_RAIL_TIDS`, `ALLOWED_BRACE_TIDS` | fachwerkweite TID-Whitelist | Domain Contract | `bvillage/domains/fachwerk/core/schema_member_tids_fachwerk.py` | kein aktuelles Problem sichtbar | hoch | **neu sauber etabliert** |
| `bvillage/types/fachwerkhaus/hallenhaus/schema_frame_roles.py` | `FrameRole`, `ALLOWED_FRAME_ROLES` | Hallenhaus-spezifische Frame-Rollen | Type Contract | `bvillage/types/fachwerkhaus/hallenhaus/schema_frame_roles.py` | war zuvor im Domain-Contract versteckt | hoch | **neu sauber etabliert** |
| `bvillage/types/fachwerkhaus/hallenhaus/schema_frameplan_langhaus.py` | `FramePlanLanghaus`, `SCHEMA_VERSION_LANGHAUS` | Hallenhaus-FramePlan-Schema | Type Contract | `bvillage/types/fachwerkhaus/hallenhaus/schema_frameplan_langhaus.py` | war zuvor mit Domainregeln vermischt | hoch | **neu sauber etabliert** |
| `bvillage/types/fachwerkhaus/hallenhaus/validate_frameplan_type.py` | `validate_frameplan_langhaus_type` | Hallenhaus-FrameLayout-/Type-Validation | Type Validator | `bvillage/types/fachwerkhaus/hallenhaus/validate_frameplan_type.py` | war zuvor im Domain-Validator enthalten | kritisch | **neu sauber etabliert** |
| `bvillage/domains/fachwerk/core/validate_frameplan_fachwerk.py` | `validate_frameplan_langhaus_schema`, `validate_frameplan_langhaus_domain` | schema-nahe + fachwerkweite Validierung | Domain Validator | `bvillage/domains/fachwerk/core/validate_frameplan_fachwerk.py` | hieß zuvor irreführend `validate_frameplan_langhaus.py` | hoch | **erledigt** — umbenannt und bereinigt |
| `bvillage/types/fachwerkhaus/hallenhaus/architect.py` | Voll-Gate-Punkt | validiert FramePlan jetzt am Erzeugungspunkt | Type orchestration / gate | `bvillage/types/fachwerkhaus/hallenhaus/architect.py` | zuvor nur Sanity-Checks + späterer Builder-Gate | kritisch | **erledigt** — kanonischer Voll-Gate-Punkt im Architekten |

---

## Additional findings from the audit

- `frameplan_checks.py` now uses the global `Issue` dataclass from `bvillage/core/model.py`.
- The canonical full gate for the active Hallenhaus frameplan now lives in the Architect, directly after frameplan creation.
- `build_frame.py` now keeps only renderer-side boundary guards (`notes`, `frameplan`, `vec3`) and geometry emission.
- `frameplan_contract.py` had no active source usage and was therefore removed as a dead redundant path.
- `contract_frameplan_langhaus.py` was split into separate files for:
  - Fachwerk domain member TID rules
  - Hallenhaus frame roles
  - Hallenhaus frameplan schema
- Type validation was moved out of the domain validator into the Hallenhaus type layer.
- The former mixed validator was first split functionally, then physically separated by layer.
- The remaining active contract-/validation-related source files are now:

```text
bvillage/core/policy_stack.py
bvillage/core/policy_types.py
bvillage/domains/fachwerk/core/schema_member_tids_fachwerk.py
bvillage/domains/fachwerk/core/validate_frameplan_fachwerk.py
bvillage/types/fachwerkhaus/hallenhaus/schema_frame_roles.py
bvillage/types/fachwerkhaus/hallenhaus/schema_frameplan_langhaus.py
bvillage/types/fachwerkhaus/hallenhaus/validate_frameplan_type.py
```

---

## Active target state after this consolidation round

```text
Architect
   ├─ run_arch_checks()                    # lightweight Issue-based sanity checks
   ├─ validate_frameplan_langhaus_schema() # schema-near validation
   ├─ validate_frameplan_langhaus_domain() # fachwerk domain validation
   └─ validate_frameplan_langhaus_type()   # hallenhaus type validation
            │
            ▼
      FramePlan (canonical)
            │
            ▼
Builder
   └─ boundary guards + rendering only
```

---

## Open follow-up items

1. The function names in `validate_frameplan_fachwerk.py` still carry the `langhaus` qualifier and may later be renamed for stricter semantic consistency.
2. The Markdown architecture documents should be updated so the written contract map matches the now-cleaner code reality.
3. A future audit round can scan the remaining Blender `SchemaError` raises to distinguish boundary guards from any hidden structural assumptions.

---

## End of worklist
