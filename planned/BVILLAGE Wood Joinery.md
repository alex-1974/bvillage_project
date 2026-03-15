# BVILLAGE Wood Joinery System

---
tier: 2
authority: ARCHITECTURAL
referenced-by: BVILLAGE_PIPELINE_ROLES.md, SYS_CONTRACT.md
references: SYS_PRINCIPLES.md, SYS_CONTRACT.md, ARCH_MATERIALS.md
---

---

# 1. Zweck

`wood_joinery` ist ein **Core-Service** — keine Pipeline-Rolle, kein eigener Plan, kein Artefakt.

Er stellt eine offene, erweiterbare Bibliothek von Holzverbindungstypen bereit, die jeder Produzent im System nach Bedarf aufruft: Frame Producer, Roof Producer, Furniture Producer, und jede zukünftige Baugrammatik mit Holzverbindungen.

Der Service erfüllt zwei Aufgaben:

1. **Registrierung** von Verbindungstypen — Core liefert das Fundament, Baugrammatiken registrieren Spezialisierungen.
2. **Auflösung** sichtbarer Oberflächenmerkmale für eine gegebene Verbindungssituation.

`wood_joinery` generiert keine Geometrie, schreibt keine Pläne, kennt keinen Renderer.

---

# 2. Architekturprinzip

```
Frame Producer / Roof Producer / Furniture Producer
    ↓
wood_joinery.resolve_visible_marks(joint_type, member_a, member_b, context)
    ↓
VisibleMarks
    ↓
in FramePlan / RoofPlan / FurniturePlan geschrieben
    ↓
Renderer liest Plan → emittiert Geometrie
```

Der Renderer ist dumm. Er befolgt den Plan — nicht mehr, nicht weniger.

Welche Verbindung an welchem Member sitzt und welche sichtbaren Merkmale sie hinterlässt, entscheidet ausschließlich der jeweilige Produzent. Er fragt `wood_joinery`, schreibt das Ergebnis in seinen Plan, und übergibt den Plan an den Renderer.

`wood_joinery` hat keinen Zustand zwischen Aufrufen. Es gibt keine Pipeline-Position, keinen eigenen Planschritt, keine Abhängigkeit vom Renderer.

---

# 3. Strikter Geltungsbereich

**`wood_joinery` tut ausschließlich:**

- Verbindungstypen registrieren und verwalten
- Sichtbare Merkmale einer Verbindungssituation auflösen

**`wood_joinery` tut niemals:**

- FramePlan, RoofPlan oder andere Pläne schreiben oder lesen
- Geometrie erzeugen
- Blender aufrufen oder davon abhängen
- Strukturelle Validierung durchführen (Aufgabe des Inspector)
- Policy-Stacks auflösen

---

# 4. Offene Verbindungsbibliothek

Das System beschränkt sich nicht auf vordefinierte Verbindungsfamilien.

Core liefert eine Basisbibliothek gebräuchlicher Verbindungen:

```
Blattstoß
Zapfen / Zapfenloch
Schwalbenschwanz
Hakenblatt
Gerberstoß
Überblattung
Holznagel-Verbindung
```

Jede Baugrammatik kann eigene Typen registrieren, wenn sie spezifische Verbindungen benötigt, die Core nicht abdeckt — z.B. japanische Zimmerverbindungen, Möbelverbindungen, Blockbauverbindungen.

Ein Verbindungstyp ist gültig, wenn er den Joinery-Contract implementiert.

---

# 5. Registrierung

```python
wood_joinery.register(spec: JoinerySpec) -> None
```

Jeder Verbindungstyp definiert:

- `joinery_id` — stabiler, eindeutiger Bezeichner
- `parameter_schema` — erlaubte Parameter und ihre Typen
- `visible_marks_fn` — Funktion, die `VisibleMarks` auflöst
- `metadata` — optional: Region, Epoche, Herkunft, historische Belege

Optionale Metadaten dienen der historischen Filterung durch die aufrufende Baugrammatik. Sie sind kein Pflichtfeld und beeinflussen die Auflösung nicht direkt.

---

# 6. Auflösung

```python
marks = wood_joinery.resolve_visible_marks(
    joinery_id: str,
    member_a: MemberRef,
    member_b: MemberRef,
    face_mask: FaceMask,
    context: JoineryContext,
    parameters: dict,
) -> list[VisibleMark]
```

Die Auflösung ist deterministisch. Gleiche Eingaben → gleiche Ausgabe, immer.

`face_mask` gibt an, welche Faces des Members sichtbar sind. Marks für nicht-sichtbare Faces werden nicht aufgelöst — das hält den Hot Path klein.

`context` trägt kulturellen Kontext (Region, Epoche, Handwerkstradition), der für die Auflösung relevant sein kann. Er wird einmal pro Gebäude durch den Produzenten aufgebaut, nicht durch `wood_joinery`.

---

# 7. Sichtbare Merkmale

Verbindungen hinterlassen beobachtbare Spuren auf den Oberflächen der Members. Diese werden als **neutrale Oberflächenmerkmale** dargestellt — keine Render-Instruktionen, keine Geometrie.

Kern-Merkmalstypen:

```
peg           — Holznagel
seam_line     — Stoßfuge
notch_line    — Kerbkante
scarf_line    — Schrägstoß
wedge_mark    — Keilabdruck
surface_patch — Flächenveränderung
```

Jedes Merkmal referenziert einen Member und einen Face.

Geometrie wird in **lokalen Member-Koordinaten** ausgedrückt (normiert: u/v auf der Fläche, Abmessungen in Metern).

---

# 8. Lokale Geometriedarstellung

Beispiel Holznagel:

```
kind: peg
member_id: post_04
face: front
geometry_local:
    u: 0.48
    v: 0.55
    diameter_m: 0.022
    recess_m: 0.003
```

Beispiel Stoßfuge:

```
kind: seam_line
member_id: beam_12
face: front
geometry_local:
    path_uv:
        - [0.2, 0.3]
        - [0.8, 0.3]
    width_m: 0.002
    depth_m: 0.001
```

Keine Weltkoordinaten. Keine Renderer-Begriffe.

---

# 9. Performance

Fachwerk-Gebäude enthalten typisch 200–600 Verbindungen. Durch konsequente Anwendung zweier Prinzipien bleibt der Aufwand gering:

**1. Nur sichtbare Verbindungen aufgelöst**
Verbindungen an nicht-sichtbaren Faces oder unterhalb des Detail-Levels werden übersprungen. Effektive Auflösungen pro Gebäude: 20–80.

**2. Caching identischer Verbindungssituationen**
Dutzende gleicher Verbindungstypen (z.B. identische Kopfband-Zapfen) produzieren nur einen Cache-Miss. Cache-Key:

```
joinery_id + member_section_class + face_mask + detail_level
```

Ergebnis: `wood_joinery` ist kein Performance-Engpass.

---

# 10. Abgrenzung zu anderen Subsystemen

| Aufgabe | Zuständig |
|---|---|
| Strukturelle Plausibilität prüfen | Inspector |
| Verbindungstyp für einen Member wählen | Frame Producer / Roof Producer |
| Verbindungsmerkmale auflösen | `wood_joinery` |
| Merkmale in den Plan schreiben | Produzent |
| Merkmale als Geometrie emittieren | Renderer |
| Mechanische Tragfähigkeit simulieren | außerhalb des Scope |

Mechanische Profile (Scherkraft, Rotationssteifigkeit, Duktilität) sind nicht Teil dieses Systems. BVILLAGE ist kein Statik-Simulator. Die Baugrammatik kodiert implizit strukturell plausible Verbindungssituationen. Feinkörnige Verbindungsmechanik wäre Overhead ohne Mehrwert für die Ausgabe.

---

# 11. Konzeptübersicht

```
Core-Bibliothek + Baugrammatik-Erweiterungen
        ↓
wood_joinery.register(spec)
        ↓
Produzent (Frame Producer / Roof Producer / ...)
        ↓
wood_joinery.resolve_visible_marks(...)
        ↓
VisibleMarks (in lokalem Member-Koordinatensystem)
        ↓
Produzent schreibt Marks in seinen Plan
        ↓
Renderer emittiert Geometrie aus Plan
```
