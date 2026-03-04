# BVILLAGE -- Structural Grammar Architecture

## Version 0.2.0

**Status:** Conceptual Foundation\
**Project Phase:** Structural Intelligence (v0.4.x)\
**Domain Scope:** Timber Construction (Europe 800--1600)\
**Paradigm:** Multi-Architect Structural Model\
**Last Updated:** YYYY-MM-DD

------------------------------------------------------------------------

# 1. Introduction

BVILLAGE models historically grounded architectural systems.\
To achieve structural plausibility, it must operate on the level of
**construction grammar**, not merely stylistic variation.

Timber buildings in Europe between roughly **800 and 1600** do not
represent a single construction logic with superficial regional
variation.\
Instead they embody a limited number of **structural design paradigms**,
each with distinct internal rules.

These paradigms determine:

-   how loads flow through the building\
-   how buildings grow over time\
-   how walls, floors, and roofs interact\
-   which structural operations are possible

This document introduces **Structural Grammar Architecture (SGA)** for
BVILLAGE.

SGA formalizes the idea that historically plausible buildings must
emerge from **coherent structural grammars** rather than from arbitrary
parameter combinations.

------------------------------------------------------------------------

# 2. Core Thesis

A universal architect capable of combining all construction principles
freely leads to:

-   internal contradictions\
-   exploding rule sets\
-   historically implausible hybrids\
-   increasing system fragility over time

Historical building practice did not operate through universal
abstraction.

It relied on **localized structural competence**.

Therefore BVILLAGE adopts the following principle:

> Each architect represents a coherent structural grammar.\
> Grammars may not be freely mixed.\
> Hybrids arise only through controlled composition.

------------------------------------------------------------------------

# 3. What Is a Structural Grammar?

A **structural grammar** defines the fundamental ordering principles of
a building system.

These include:

-   primary load center
-   dominant structural axis
-   building growth mechanism
-   relationship between roof, wall, and floor
-   permissible structural operations

A grammar is **not**:

-   a style
-   a region
-   a roof type
-   a material
-   an ornament system

A grammar describes **deep structural organization**.

------------------------------------------------------------------------

# 4. Candidate Grammar Families (Europe 800--1600)

Based on architectural literature and preliminary case studies, several
candidate grammar families can be identified.

These families represent **working hypotheses**, not final categories.

------------------------------------------------------------------------

## 4.1 Modular / Box Grammar

**Core Logic:** Additive cell structure.

Characteristics:

-   stackable storeys\
-   independent structural frames per level\
-   overhang (jetty) as natural operation\
-   erker or bay windows as sub-modules

**Growth Mechanism**

    module + module + module

**Primary Load Logic**

    roof
    ↓
    wall frames
    ↓
    ground

Typical examples:

-   urban timber houses\
-   English box-frame buildings\
-   modular town houses

------------------------------------------------------------------------

## 4.2 Hall / Aisled Grammar

**Core Logic:** Span-oriented interior support system.

Characteristics:

-   interior support rows\
-   roof-dominant structural logic\
-   large unified interior volumes\
-   clear axial organization

**Growth Mechanism**

    bay extension along longitudinal axis

**Primary Load Logic**

    roof
    ↓
    tie beams / purlins
    ↓
    interior supports
    ↓
    ground

Typical examples:

-   Hallenhäuser\
-   tithe barns\
-   medieval halls

------------------------------------------------------------------------

## 4.3 Surface / Continuous Wall Grammar

**Core Logic:** Structural continuity of wall planes.

Characteristics:

-   dense bracing systems\
-   walls functioning as structural surfaces\
-   integrated diagonal stabilization

**Growth Mechanism**

    expansion of structural wall planes

This grammar remains under investigation.

It may represent a distinct structural family or a constrained variant
of modular systems.

------------------------------------------------------------------------

## 4.4 Core-Centered Grammar

**Core Logic:** Dominant structural nucleus.

Characteristics:

-   central vertical core\
-   height-prioritized composition\
-   radial or tiered load distribution

**Growth Mechanism**

    vertical stacking around core

Typical examples:

-   stave churches\
-   central timber towers\
-   vertically organized sacred structures

------------------------------------------------------------------------

# 5. Structural Member Ontology

Structural grammars operate at the level of **organizational
principles**.

To translate these principles into a computable system, BVILLAGE
requires a **stable vocabulary of structural elements**.

BVILLAGE therefore introduces a **Structural Member Ontology**.

Each structural element receives a stable **Term Identifier (TID)**.

Examples:

    post.primary
    post.corner
    post.jamb

    beam.tie
    beam.wallplate
    beam.bressumer
    beam.jetty

    brace.diagonal
    brace.knee

    infill.panel

These identifiers represent structural concepts independent of:

-   archetype
-   region
-   epoch
-   material

The ontology acts as the **semantic contract between topology and
geometry generation**.

------------------------------------------------------------------------

# 6. Architectural Roles in BVILLAGE

BVILLAGE separates architectural responsibility across specialized
roles.

## Architect

Responsible for structural logic.

Tasks:

-   select grammar
-   define topology
-   produce FramePlan skeleton

## Roof

Resolves roof structure within grammar constraints.

Tasks:

-   select roof system
-   resolve span and load distribution

## Interior

Responsible for spatial organization.

Tasks:

-   insert floors
-   partition space
-   introduce secondary loads

## Facade

Responsible for structural articulation.

Tasks:

-   opening rhythm
-   visual modulation
-   facade composition

## Structural Validation

Responsible for plausibility.

Tasks:

-   define cross-sections
-   verify load capacity
-   suggest structural corrections

------------------------------------------------------------------------

# 7. Grammar Invariants

Each grammar defines **non-negotiable invariants**.

Examples:

Hall grammar:

-   interior support rows required
-   axial bay extension
-   roof-dominant load path

Modular grammar:

-   discrete structural units
-   vertical stacking possible

Surface grammar:

-   continuous wall integrity

Core grammar:

-   central structural dominance

------------------------------------------------------------------------

# 8. Grammar Compatibility

Not all grammars can coexist safely within one building.

BVILLAGE therefore introduces a **Grammar Compatibility Matrix**.

Compatibility depends on:

-   load path compatibility
-   structural axis compatibility
-   growth mechanism compatibility

Compatibility categories:

  Category     Meaning
  ------------ --------------------------
  Compatible   grammars may coexist
  Restricted   mediation required
  Forbidden    structural contradiction

------------------------------------------------------------------------

# 9. Research Methodology

Structural grammar classification must be validated empirically.

BVILLAGE will therefore construct a dataset of approximately:

**100--200 historically documented buildings.**

Each building will be coded using structural parameters including:

-   load center
-   wall continuity
-   support rows
-   roof influence
-   growth mechanism
-   storey logic

Cluster analysis may confirm or revise grammar definitions.

------------------------------------------------------------------------

# 10. Software Architecture Implications

Because grammar taxonomy remains under investigation:

-   grammars must remain modular
-   grammars must not be hard-coded enums
-   grammars should be implemented as rule systems
-   new grammars must be addable without system rewrite

------------------------------------------------------------------------

# 11. Long-Term Vision

Structural Grammar Architecture forms the conceptual backbone of
BVILLAGE.

Combined with the Structural Member Ontology it provides:

-   historically plausible building logic
-   scalable archetype expansion
-   clear separation of architectural responsibilities
-   deterministic structural interpretation

BVILLAGE therefore becomes not merely a building generator but a **model
of architectural intelligence**.

------------------------------------------------------------------------

License: CC-BY-SA 4.0\
© 2026 Alexander Bernardi
