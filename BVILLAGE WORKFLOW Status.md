# BVILLAGE – WORKFLOW
Status: Active
Scope: Internal research collaboration (human + AI)

This document defines how the project is operated.
It prevents chaos during experimental phases.

------------------------------------------------------------
0. PRINCIPLE
------------------------------------------------------------

The chat is a tool.
The repository is the source of truth.

No architectural decision lives only in chat.

------------------------------------------------------------
1. DOCUMENT ROLES
------------------------------------------------------------

PROJECT_MASTER.md
- Long-term architectural truth.
- Changes rarely.
- Only updated when structural direction changes.

ARCHITECTURE_RULES.md
- Hard constraints.
- Only changed intentionally.
- Never edited during debugging.

TODO.md
- Single active work queue.
- Updated when:
  - new structural task emerges
  - task changes scope
  - task completed

CHANGELOG.md
- Written only when:
  - structural behavior changes
  - builder logic changes
  - schema changes
  - deterministic behavior changes
- Not for micro-edits or typo fixes.

REPRO_CASES.md
- Updated when:
  - a bug is fixed
  - a structural refactor might regress behavior
  - a new fragile edge-case is discovered

WORKFLOW.md
- Updated only when collaboration process changes.

------------------------------------------------------------
2. WHEN TO UPDATE WHAT
------------------------------------------------------------

During experimentation:
- Update TODO.md frequently.
- Do NOT update CHANGELOG.md yet.

After structural refactor is complete:
- Write a CHANGELOG entry.
- Possibly update PROJECT_MASTER snapshot.

When fixing a bug:
- Add REPRO case.
- Only after fix confirmed, update CHANGELOG.

When changing architectural direction:
- Update PROJECT_MASTER.md.
- Possibly update ARCHITECTURE_RULES.md.
- Add decision summary to CHANGELOG.

------------------------------------------------------------
3. TASK LIFECYCLE
------------------------------------------------------------

1. Task appears → added to TODO.md.
2. Work in experimental mode.
3. Once stable:
   - Remove from TODO.md.
   - Add entry to CHANGELOG.md.
4. If fragile behavior involved:
   - Add REPRO_CASE entry.

Rule:
No structural change without CHANGELOG entry.

------------------------------------------------------------
4. CHAT USAGE MODE
------------------------------------------------------------

Each new chat should begin with:

PROJECT: bvillage
VERSION: x.y.z
SNAPSHOT:
(current 3–5 line state)
CURRENT TASK:
(one concrete task)

Avoid:
- long historical explanations
- mixing architecture + debugging in same session

Declare working mode:
- ARCHITECTURE
- REFACTOR
- DEBUG
- RESEARCH

------------------------------------------------------------
5. EXPERIMENT PHASE RULES
------------------------------------------------------------

Allowed:
- Refactor domain heuristics
- Adjust policy parameters
- Change builder internals

Not allowed:
- Silent change of structural truth
- Removing determinism
- Mutating core data models
- Bypassing notes schema

------------------------------------------------------------
6. VERSIONING STRATEGY (LIGHTWEIGHT)
------------------------------------------------------------

Use semantic style:

MAJOR: structural direction changes
MINOR: new constructive features
PATCH: bugfix / determinism fix

Version only updated when CHANGELOG entry written.

------------------------------------------------------------
7. FILE HYGIENE
------------------------------------------------------------

- No print() in core/domain.
- Logging only through configured logger.
- No temporary debug hacks left uncommented.
- No structural fallback logic in builder.
- Every .py file must start with a canonical path comment.
- Path comment must match repository location exactly.
- During refactors, this line must be updated.

------------------------------------------------------------
8. SNAPSHOT DISCIPLINE
------------------------------------------------------------

Maintain short SNAPSHOT block in PROJECT_MASTER:

Example:

=== SNAPSHOT 6.4.x ===
FramePlan authoritative.
Builder refactor in progress.
Posts now axes_u-driven.
=== END SNAPSHOT ===

This block is used to bootstrap new chats.

------------------------------------------------------------
9. DECISION DISCIPLINE
------------------------------------------------------------

If a structural decision is made in chat:

Before coding:
- Summarize decision.
- Add TODO entry.
- Only then implement.

Architecture must be explicit.

------------------------------------------------------------
10. PRINCIPLE OF CALM DEVELOPMENT
------------------------------------------------------------

The project is allowed to be incomplete.
It is not allowed to be inconsistent.
