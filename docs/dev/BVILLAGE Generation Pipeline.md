# BVILLAGE — Generation Pipeline & Stabilization Plan (v0.4.0)

## Purpose

Dieses Dokument fasst den **aktuellen Architekturstand von BVILLAGE** sowie die **konkreten nächsten Schritte nach dem Architecture Audit** zusammen.

Es dient als **Handout für neue Chats**, damit Projektkontext nicht verloren geht.

Ziel der aktuellen Phase ist:

> **BVILLAGE v0.4.0 Stabilization**

Das bedeutet:

- stabile Systemarchitektur
- saubere Plugin-Grenzen
- deterministische Hausgenerierung
- klar definierte Daten-Contracts
- keine stillen Fallbacks

---

# 1. Architekturprinzipien

Die BVILLAGE-Architektur basiert auf drei strikt getrennten Ebenen.

## Core

Core enthält ausschließlich **generische Infrastruktur**.

Core kennt **keine Bauweise, keine Archetypen und keine Construction Grammars**.

Core enthält:

- Context / BuildingOrder
- PolicyStack
- Registry
- Foreman / Dispatch
- Validation Framework
- Data Contracts

Core darf **niemals importieren**:

```text
bvillage.domains.*
bvillage.types.*
bvillage.blender.*
```

## Domains

Domains definieren **Konstruktion / structural grammar**.

Beispiele:

```text
timber_frame
log_construction
masonry_loadbearing
```

Domains enthalten:

- Frame Producer
- Roof Producer
- domain validation
- domain translation layer for Inspector
- domain renderer

Domains kennen **keine konkreten Archetypen**.

## Types

Types definieren **Topologie / Gebäudeorganisation**.

Beispiele:

```text
fw_longhouse
fw_townhouse
fw_crosshall
```

Types enthalten:

- spatial layout
- zone logic
- opening demands
- archetype constraints

Types erzeugen **keine Struktur**.

---

# 2. Kanonische Pipeline-Rollen

Die Dokumentation definiert die Pipeline über **Rollen**, nicht über historisch gewachsene Modulnamen.

## 2.1 Commissioner

Startet den Bauauftrag.

Aufgaben:

- entscheidet, **welches Gebäude wo** platziert wird
- sammelt Rohkontext
- löst den vollständigen PolicyStack zu `ResolvedPolicy`
- erzeugt `BuildingOrder`

Er trifft **keine konstruktiven Entscheidungen**.

## 2.2 Foreman

Koordiniert die Pipeline.

Aufgaben:

- fragt die Registry nach den passenden Plugins
- dispatcht die Spezialisten in der richtigen Reihenfolge
- koordiniert Konflikte zwischen Spezialisten
- kennt nur **Interfaces**, keine konkreten Implementierungen

## 2.3 Topology Planner

Plant die **räumliche Organisation**.

Aufgaben:

- erzeugt `SemanticPlan`
- definiert Zonen, Wanddefinitionen, Achslogik, Öffnungsbedarfe
- erzeugt **keine Members**

## 2.4 Frame Producer

Erzeugt den **Rohbau**.

Aufgaben:

- übersetzt `SemanticPlan` + `ResolvedPolicy` in `FramePlan`
- erzeugt explizite Members
- implementiert die jeweilige Construction Grammar

## 2.5 Roof Producer

Erzeugt den **RoofPlan**.

Aufgaben:

- liest `FramePlan`
- setzt `RoofPolicy` innerhalb der domain-spezifischen Möglichkeiten um
- verändert `FramePlan` nicht

## 2.6 Joiner

Plant den **Innenraum**.

Aufgaben:

- erzeugt `InteriorPlan`
- plant Raumunterteilungen, Zirkulation, hearth / furnace, Innenöffnungen
- verändert `FramePlan` oder `RoofPlan` nicht

## 2.7 Inspector

Prüft **universelle Physik**.

Aufgaben:

- erhält abstrahierte Strukturdaten
- erzeugt `Issue`-Objekte
- verändert nichts

## 2.8 Appraiser

Bewertet Kandidaten.

Aufgaben:

- wertet Varianten gegen `ConstraintsPolicy` aus
- wählt den besten Kandidaten
- verändert keine Geometrie

## 2.9 Renderer

Erzeugt **Geometrie**.

Aufgaben:

- liest `FramePlan` und `RoofPlan`
- baut exakt das, was in den Plänen steht
- macht **keine strukturellen Entscheidungen**

---

# 3. Angepasste BVILLAGE-Generation-Pipeline

Die Generierung eines Gebäudes erfolgt deterministisch in dieser Reihenfolge:

```text
Commissioner
   ↓
BuildingOrder + ResolvedPolicy
   ↓
Foreman
   ↓
Topology Planner
   ↓
SemanticPlan
   ↓
Frame Producer
   ↓
FramePlan
   ↓
Roof Producer
   ↓
RoofPlan
   ↓
Joiner
   ↓
InteriorPlan
   ↓
Inspector
   ↓
Issue[]
   ↓
Appraiser
   ↓
selected candidate
   ↓
Renderer
   ↓
Blender Geometry
```

Wichtig:

- `FramePlan` ist die **einzige strukturelle Wahrheit**.
- Der Renderer baut **Members**, nicht Achsen.
- `Joiner` kommuniziert über Plan-Grenzen, nicht über direkte Mutation.

---

# 4. Pipeline-Komponenten im Projekt

## 4.1 Commissioner

Implementierungsebene:

```text
SettlementBuilder / caller code
```

Nicht als eigener File-Role-Name festgelegt.

## 4.2 Foreman

Ort:

```text
bvillage/foreman/
```

Dateinamen folgen der Naming Policy, z. B.:

```text
plan_context.py
plan_dispatch.py
plan_conflict.py
```

## 4.3 Topology Planner

Ort:

```text
bvillage/types/<family>/plan_topology.py
```

Beispiel:

```text
bvillage/types/fw_longhouse/plan_topology.py
```

Erzeugt ausschließlich:

```text
SemanticPlan
```

Typischer Inhalt:

```text
zone graph
axis grid
wall definitions
opening demands
geometric intent
```

## 4.4 Frame Producer

Ort:

```text
bvillage/domains/<domain>/core/derive_frameplan_<grammar>.py
```

Beispiele:

```text
derive_frameplan_boxframe.py
derive_frameplan_storeyframe.py
derive_frameplan_cruck.py
```

Input:

```text
SemanticPlan
ResolvedPolicy
```

Output:

```text
FramePlan
```

Erzeugt explizite Members, z. B.:

```text
posts
beams
rails
braces
infills
```

## 4.5 Roof Producer

Ort:

```text
bvillage/domains/<domain>/core/derive_roofplan.py
```

Input:

```text
FramePlan
RoofPolicy
```

Output:

```text
RoofPlan
```

## 4.6 Joiner

Ort:

```text
bvillage/domains/<domain>/core/plan_interior.py
```

Output:

```text
InteriorPlan
```

## 4.7 Inspector

Ort:

```text
bvillage/core/validate_physics.py
```

Output:

```text
tuple[Issue, ...]
```

## 4.8 Appraiser

Ort:

```text
bvillage/core/audit_candidates.py
```

Output:

```text
AuditReport / candidate selection
```

## 4.9 Renderer

Ort:

```text
bvillage/domains/<domain>/blender/build_*.py
```

Beispiel:

```text
build_frameplan.py
```

Renderer baut **nur Geometrie**.

Nicht erlaubt:

```text
axes → structure
fallback structure
implicit repair
```

---

# 5. Dateinamen vs. Rollen

Die Dokumentation unterscheidet zwischen **Pipeline-Rollen** und **Dateirollen**.

Pipeline-Rollen sind:

- Commissioner
- Foreman
- Topology Planner
- Frame Producer
- Roof Producer
- Joiner
- Inspector
- Appraiser
- Renderer

Dateirollen folgen dagegen strikt dem Schema:

```text
<role>_<aspect>.py
```

Erlaubte Dateirollen sind:

```text
plan_
derive_
build_
validate_
audit_
report_
policy_
schema_
mesh_
```

Beispiel-Mapping:

| Pipeline role | File role | Beispiel |
|---|---|---|
| Foreman | `plan_` | `foreman/plan_dispatch.py` |
| Topology Planner | `plan_` | `types/fw_longhouse/plan_topology.py` |
| Frame Producer | `derive_` | `domains/fachwerk/core/derive_frameplan_boxframe.py` |
| Roof Producer | `derive_` | `domains/fachwerk/core/derive_roofplan.py` |
| Joiner | `plan_` | `domains/fachwerk/core/plan_interior.py` |
| Inspector | `validate_` | `core/validate_physics.py` |
| Appraiser | `audit_` | `core/audit_candidates.py` |
| Renderer | `build_` | `domains/fachwerk/blender/build_frameplan.py` |

---

# 6. System-Contracts

Die Pipeline basiert mindestens auf diesen stabilen Datenstrukturen.

## 6.1 BuildingOrder

Definiert den Bauauftrag.

Typischer Inhalt:

```text
archetype_id
seed
resolved policies
plot constraints
```

## 6.2 SemanticPlan

Definiert die topologische Gebäudeorganisation.

Beispiele:

```text
zone graph
axis grid
wall definitions
opening demands
```

Keine Strukturinformationen.

## 6.3 FramePlan

Definiert die Struktur.

```text
members:
    posts
    beams
    rails
    braces
    infills
```

`FramePlan` ist die **einzige Quelle der Struktur**.

## 6.4 RoofPlan

Definiert die Dachstruktur.

```text
rafters
ridge
purlins
roof members
```

## 6.5 InteriorPlan

Definiert Innenraumlogik.

```text
partitions
circulation
room functions
hearth / furnace placement
```

## 6.6 Issue

Wird von Validatoren erzeugt.

```text
HARD
SOFT
SUGGEST
```

---

# 7. Ergebnis des Architecture Audit

Der Audit ergab:

```text
24 HARD violations
38 MEDIUM violations
104 LOW violations
```

LOW = Hygiene  
MEDIUM = Designprobleme  
HARD = Architekturbruch

Die HARD-Probleme lassen sich auf wenige Kernursachen reduzieren.

---

# 8. Hauptprobleme

## 8.1 Type erzeugt Struktur

Datei:

```text
types/fachwerkhaus/hallenhaus/architect.py
```

Dort werden aktuell erzeugt:

```text
posts
rails
braces
```

Das verletzt die Layerregel:

```text
Types → Topologie
Domains → Struktur
```

## 8.2 Core enthält Domainwissen

Beispiele:

```text
fachwerk
hallenhaus
binder
```

in

```text
core/policy_stack.py
core/materials/policies/
core/model.py
```

Core darf **keine Domain- oder Type-Semantik** kennen.

## 8.3 Domain kennt Types

Beispiel:

```text
validate_frameplan_fachwerk.py
```

importiert Type-Schema.

Domain darf **keine Archetypen kennen**.

## 8.4 Renderer enthält Fallback-Logik

Renderer enthält:

```text
fallback
legacy fallback
```

Das verletzt den Members-only-Contract.

## 8.5 Pipeline-Reihenfolge im Handout war zu grob

Die frühere Kurzpipeline

```text
TypePlanner → DomainFrameProducer → OpeningProducer → Renderer
```

war für v0.4.0 als Arbeitsmodell brauchbar,
aber **nicht mehr deckungsgleich mit der kanonischen Dokumentation**.

Fehlende Rollen waren:

- Commissioner
- Foreman
- Roof Producer
- Joiner
- Inspector
- Appraiser

---

# 9. Konkrete nächste Schritte

Die Stabilization erfolgt in dieser Reihenfolge.

## Schritt 1 — Type-Architect auflösen

Datei:

```text
types/.../architect.py
```

wird funktional ersetzt durch:

```text
plan_topology.py
plan_openings.py   (nur falls typologisch nötig)
```

Alle strukturellen Operationen wandern in Domain-Core.

## Schritt 2 — Frame Producer implementieren / herauslösen

Neue oder bereinigte Dateien:

```text
domains/fachwerk/core/derive_frameplan_boxframe.py
domains/fachwerk/core/derive_frameplan_storeyframe.py
```

Diese erzeugen:

```text
posts
beams
rails
braces
infills
```

Input:

```text
SemanticPlan
ResolvedPolicy
```

## Schritt 3 — Roof Producer explizit machen

Datei:

```text
domains/fachwerk/core/derive_roofplan.py
```

muss als eigener Pipeline-Schritt sichtbar werden.

## Schritt 4 — Joiner sauber abgrenzen

Datei:

```text
domains/fachwerk/core/plan_interior.py
```

muss `InteriorPlan` erzeugen, ohne `FramePlan` oder `RoofPlan` zu mutieren.

## Schritt 5 — Core entfachwerken

Entfernen aus Core:

```text
fachwerk
hallenhaus
binder
```

Diese Logik gehört nach:

```text
domains/
types/
policies/
```

## Schritt 6 — Domain-Type-Kopplung entfernen

Datei:

```text
validate_frameplan_fachwerk.py
```

darf **keine Type-Schemas importieren**.

Domain validiert nur:

```text
structural grammar
member constraints
domain topology rules
```

## Schritt 7 — Renderer deterministisch machen

Entfernen:

```text
fallback
legacy fallback
```

Renderer darf nur:

```text
FramePlan
RoofPlan
```

verwenden.

## Schritt 8 — Foreman-Dispatch explizit machen

Die reale Pipeline soll über Foreman laufen, nicht über einen monolithischen `architect.py`.

## Schritt 9 — PolicyStack isolieren

Zugriffe auf:

```text
ctx.region
ctx.epoch_band
ctx.wealth
```

nur innerhalb von Policy-Resolution.

Andere Module bekommen:

```text
ResolvedPolicy
```

---

# 10. Ziel von v0.4.0

Am Ende von v0.4.0 gilt:

```text
Commissioner → Auftrag
Foreman → Orchestrierung
Type → Topologie
Domain → Struktur + Dach + Innenraumableitung
Inspector/Appraiser → Prüfung/Bewertung
Renderer → Geometrie
Core → Infrastruktur
```

Und die Pipeline ist vollständig deterministisch.

---

# 11. Erwartetes Ergebnis

Am Ende der Stabilization soll folgendes funktionieren:

```text
seed = X
build order = Y
generate_house()
```

liefert **immer dieselbe Struktur und dieselbe Geometrie**.

---

# 12. Leitprinzip

Das Projekt darf unvollständig sein.

Es darf nicht inkonsistent sein.
