# BVILLAGE – AI Contribution Rules

---
tier: 3
authority: OPERATIONAL
change-frequency: rare
change-rule: Changes require explicit team decision. Violations of these rules risk architectural corruption and nondeterminism. Every change requires a CHANGELOG entry.
referenced-by: ENG_CODING_GUIDE.md, DOCS_INDEX.md
references: SYS_CONTRACT.md, SYS_PRINCIPLES.md, SYS_NAMING_POLICY.md
version: 0.2
status: Mandatory
---

## Purpose

This document defines mandatory integrity rules for AI-assisted contributions
to the BVILLAGE codebase.

BVILLAGE is architecture-driven, contract-bound, and deterministic.
Structural integrity has priority over temporary runtime stability.

These rules are not stylistic recommendations. They are binding constraints.

---

## I. Hard Integrity Rules

### 1. Comments Are Architectural Memory

Comments are part of the design contract.

AI must:
- Preserve all comments
- Never remove comments
- Never rewrite comments
- Never shorten comments

Allowed exception: the code change makes the comment objectively incorrect,
and the change logically requires comment adaptation.

In that case: AI annotates the proposed comment change separately
and waits for explicit confirmation before applying it.

The principle: changing a comment equals changing architecture.
Comment changes require the same explicit approval as code changes.

### 1a. AI-Authored Comments — Knowledge Transfer

AI context does not persist between sessions. Different AI instances share
no memory. Comments in code are therefore not just documentation —
they are the mechanism through which architectural reasoning survives
across sessions, across contributors, and across AI instances.

AI is expected to add explanatory comments when:
- A non-obvious implementation decision was made
- A constraint or directive shaped the code in a way that is not
  self-evident from the code alone
- A trade-off was accepted — e.g. readability over performance, or
  a structurally incomplete solution that is intentionally deferred
- A future AI or human reviewer would otherwise have to reconstruct
  the reasoning from scratch

Format for AI-authored reasoning comments:

```python
# WHY: [reason the code is written this way]
# CONSTRAINT: [what prevents the obvious alternative]
# DEFERRED: [what is intentionally not solved here, and why]
```

These comments are preserved by all subsequent contributors —
human and AI alike — under the same rules as all other comments (Rule I.1).

They are not removed when the surrounding code is refactored,
unless the reasoning they describe no longer applies.
In that case: update the comment, do not delete it silently.

The goal is a codebase where no future contributor — human or AI —
has to guess why something was done. Reasoning that lives only in
a chat session is reasoning that will be lost.

---

### 1b. Directive Comments Are Executable Constraints

Some comments are not documentation — they are behavioral directives.
They carry explicit meaning defined in ENG_CODING_GUIDE.md and must be
treated as part of the contract, not as prose.

Current directive comments:

| Directive | Meaning | AI obligation |
|---|---|---|
| `# HOT PATH` | Function is in the critical generation path. No f-strings, no logging, no defensive allocation, no unnecessary object creation. | Obey. Never add forbidden constructs to HOT PATH functions. Flag if a proposed change would violate HOT PATH constraints. |

Rules:
- AI reads directive comments before touching a function.
- AI preserves directive comments in all edits.
- AI obeys the constraints the directive imposes — not just preserves the text.
- If a task requires adding constructs that conflict with an active directive,
  AI stops and flags the conflict. It does not silently omit the directive
  or work around it.

When new directive comments are defined in ENG_CODING_GUIDE.md,
they carry the same force as existing ones. AI must consult
ENG_CODING_GUIDE.md for the current list at the start of each session.

---

### 2. Function Signatures Are Untouchable

AI must never guess or reconstruct:
- Function signatures
- Dataclass fields
- Return types
- Named parameters

If a signature is not fully visible, possibly outdated, or not clearly
defined — AI must stop and request the current definition.

No assumptions. No inferred parameters. No "probably".

---

### 3. No "Make It Run" Fixes

The following are strictly forbidden:
- Temporary defaults
- Silent fallbacks
- Dummy parameters
- Catch-all exception wrappers
- TODO-based postponements
- Hidden clamps
- Fake compatibility layers

If something breaks, it is a structural signal — not an inconvenience.
The break must be understood and resolved at its root, not patched over.

---

### 4. Tasks Must Be Fully Solved

A task is considered complete only if:
- Root cause is identified
- Architectural implications are evaluated
- Contracts remain valid
- Determinism is preserved
- No silent repair logic is introduced

Intermediate non-runnable state is acceptable.
Structural compromise is not.

---

### 5. No Stabilization Patches

AI must not:
- Add adapter layers to preserve broken APIs
- Duplicate logic to maintain compatibility
- Introduce parallel pathways
- Patch behavior without addressing cause

If a break is necessary, it must be clean and explicit.

---

### 6. No Scope Creep

AI changes only what the task specifies.

Adjacent issues — even obvious ones — are flagged, not fixed.

Completing unrequested changes is a rule violation, not a helpful shortcut.
The signal for every adjacent finding is a note, not a commit.

---

## II. Vocabulary Discipline

BVILLAGE uses precise terminology. Names carry architectural meaning.

AI uses project vocabulary exclusively. No synonyms for defined terms.

Forbidden substitutions include but are not limited to:

| Defined term | Forbidden substitute |
|---|---|
| `member` | element, component, object |
| `resolve` | calculate, compute, get |
| `derive` | compute, generate, produce |
| `domain` | system, module, layer |
| `archetype` | type, template, pattern |
| `policy` | config, settings, parameters |

When in doubt about a term: ask. Do not substitute.

---

## III. Determinism Enforcement

AI must guarantee:
- No global random usage
- No order-dependent set or dict iteration without explicit sorting
- No implicit floating-point epsilon decisions
- No hidden repair heuristics

Seed discipline is mandatory. Ordering must be explicit. Repairs must be visible.

---

## IV. Assumption Declaration

AI must never act on invisible knowledge.

When a module is generated or modified, AI appends an explicit block:

```
# ASSUMED — not verified against current codebase:
# - [assumption 1]
# - [assumption 2]
```

This block is removed only after the assumptions are confirmed by the user.

Plausible inference is not verification. A consistent-looking assumption
can be architecturally wrong. Making assumptions visible is not a weakness —
it is the mechanism that prevents silent architectural drift.

---

## V. Stop Conditions (Mandatory Ask)

AI must stop and request clarification if:
- A public function signature is unclear
- A dataclass schema may have changed
- A contract assumption is not visible
- A module boundary is ambiguous
- A change implies cross-layer architectural impact

When uncertain — stop. Continuing under incomplete context is a rule violation.

---

## VI. Stop Protocol

**STOP — 10 seconds for 10 minutes**

When context is missing, AI stops immediately and delivers a structured request.

Format:

> **STOP — 10 seconds for 10 minutes**
> I need the following before I can continue:
> - `[filename]` — reason
> - `[signature of function X]` — reason
> - `[decision: was Y ever defined?]` — reason

Two stop types exist:

**File stop** — a specific file or signature is needed.
Response: provide the file or excerpt. Task resumes immediately.

**Decision stop** — an architectural question has no visible answer.
Response: a discussion may be needed before the task continues.

Rules:
- AI never continues under incomplete context
- AI never assumes what a missing file contains
- AI never infers a signature it cannot see
- The stop is a delivery — not a failure. It is the correct output
  when context is missing.

---

## VII. Change Template (Mandatory Structure)

Every structural change must be delivered in this format:

```
1. Goal            — one sentence
2. Affected files  — explicit list
3. Change          — exact description of what changes and why
4. Invariant       — architectural invariant that holds after the change
5. Determinism     — impact on seed behavior and reproducibility
6. Verification    — minimal test or manual check that confirms correctness
```

No free-form patches. No implicit changes buried in larger diffs.

---

### Output Format — Code Delivery

AI never delivers isolated code snippets for insertion into existing files.

Reasons:
- Python indentation errors are silent and destructive
- Insertion point is often ambiguous
- Partial output cannot be verified in isolation

Rules:

**Single function changed** — deliver the complete function, from `def` to
the last line of the body. Nothing less.

**Multiple functions in one file changed** — deliver the complete file,
ready for copy/paste replacement.

**New file** — deliver the complete file.

The delivered code must be immediately usable without mental assembly.
If the user has to decide where something goes or how to merge it,
the delivery is incomplete.

---

## VIII. Test Discipline

Tests must be written against contract postconditions — not against
AI's own implementation.

A test that verifies "does the function return what I implemented it
to return" is a tautology. It proves nothing about correctness.

AI derives test cases from docstring postconditions as defined in
ENG_CODING_GUIDE.md §9. If postconditions are missing from the docstring,
AI adds them before writing the test — and flags the addition for review.

---

## IX. Red Flag Checklist (AI Self-Review)

Before finalizing any contribution, AI verifies:

- Did I modify any signature?
- Did I remove or rewrite any comment?
- Did I introduce a fallback?
- Did I add silent repair logic?
- Did I assume ordering?
- Did I introduce random without a seed?
- Did I create duplicate logic?
- Did I guess any schema?
- Did I fix anything outside the task scope?
- Did I use a synonym for a defined project term?
- Did I act on an assumption I did not declare?
- Did I add constructs to a HOT PATH function that its directive forbids?
- Did I preserve all directive comments and obey their constraints?
- Did I leave non-obvious decisions uncommented — reasoning a future
  contributor would have to reconstruct from scratch?
- Did I deliver a code snippet instead of a complete function or file?
- Is the HANDOFF current enough that a new AI instance could
  continue without asking questions already answered here?

If any answer is "yes" — stop and revise before delivering.

---

## X. Session Continuity

Chat sessions are ephemeral. AI context does not persist.
When a session ends — by choice or by necessity — all working knowledge
that was not externalized is lost.

This is not an edge case. It is the normal operating condition.
The system must be designed for it.

---

### Session Start Protocol

Every new chat session begins with regrounding — not with the task.

1. User loads the current HANDOFF document into the new chat.
2. AI reads it and confirms in one short paragraph:
   - What is being built
   - What the last known state is
   - What the next concrete step is
3. User confirms or corrects.
4. Work begins.

AI must not begin working before regrounding is confirmed.
Starting a task under an unverified model is a rule violation.

---

### HANDOFF Document

The HANDOFF document is a living document maintained during the session.
It is not a summary written at the end — it is updated continuously
as decisions are made and work progresses.

Canonical format:

```markdown
# HANDOFF — [date] / [session topic]

## Task
[One sentence: what is being built right now]

## Status
- DONE: [what is complete and stable]
- IN PROGRESS: [what is open, with last known state]
- BLOCKED: [what is waiting and why]

## Active decisions
- [Decision X]: [why, what was rejected and why]
- [Decision Y]: [why, what was rejected and why]

## Hot zone
[Which files and functions are currently in active work
and may be in an inconsistent state]

## Assumptions declared
[Any assumptions AI flagged during this session that have
not yet been confirmed by the user]

## Next step
[First concrete action in the next session — specific enough
that a new AI instance can execute it without asking]
```

---

### AI Obligations

**During a session:**
- AI updates the HANDOFF on request at any point.
- AI updates the HANDOFF proactively when:
  - A significant decision is made
  - A task is completed
  - A blocker is identified
  - The session is approaching natural complexity limits
- AI never summarizes reasoning only in chat prose
  if that reasoning is architecturally relevant.
  Relevant reasoning goes into code comments (Rule I.1a)
  or the HANDOFF — not only into the chat.

**At session end:**
- If the user signals an upcoming chat switch, AI delivers
  a final HANDOFF update before the session closes.
- The HANDOFF must be complete enough that a new AI instance
  can continue without asking questions already answered
  in the current session.

**At session start:**
- AI does not assume continuity.
- AI does not reconstruct context from memory.
- AI reads the HANDOFF, confirms the model, and waits.

---

### What the HANDOFF Is Not

The HANDOFF is not a changelog. It records current state, not history.
Completed items are removed or archived when they are no longer
relevant to active work.

The HANDOFF is not a specification. It is a snapshot.
Architectural decisions belong in the permanent documentation —
SYS_PRINCIPLES.md, ARCH_POLICIES.md, and the codebase itself.
The HANDOFF carries only what is needed to resume work.

---



Integrity over speed.

In BVILLAGE, architecture is primary.
Runtime stability is secondary.
Convenience is irrelevant.

A non-runnable codebase with correct architecture is recoverable.
A running codebase with corrupted architecture is not.

---

## Enforcement Note

Violation of these rules risks:
- Hidden nondeterminism
- Contract drift
- Architectural corruption
- Exponential future rewrite cost

AI contributions must preserve long-term structural coherence.
The cost of a violation is always paid later — and always with interest.
