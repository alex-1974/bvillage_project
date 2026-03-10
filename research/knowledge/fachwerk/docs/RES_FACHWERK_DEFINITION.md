# RES_FACHWERK_DEFINITION
## Definition, Abgrenzung und Klassifikationsachsen

---

```yaml
tier: 2
authority: REFERENCE
status: Freigegeben
version: 1.0
datum: 2026-03-07
bereich: FACHWERK/SYSTEMATIK
references: ARCH_BAUGRAMMATIKEN_WISSENSCHAFT.md, SYS_PRINCIPLES.md §3–4, ARCH_POLICIES.md §2
```

---

## Methodik und Evidenzgrade

Für jede inhaltliche Behauptung wird der Evidenzgrad angegeben:

- **[HART]** — durch mehrere unabhängige akademische Quellen gesichert
- **[MITTEL]** — durch eine Primärquelle oder übereinstimmende Sekundärquellen gestützt
- **[SCHWACH]** — plausibel, aber noch nicht durch Primärliteratur verifiziert

Quellenkürzel in Fußnoten am Ende des Dokuments. Code-Bezeichner
(Klassen, Members, Variablen, Funktionssignaturen) sind durchgehend Englisch.

---

## 1. Kerndefinition

Fachwerk bezeichnet eine **Skelettbauweise aus Holz**, bei der ein tragendes
Gerüst aus Ständern, Riegeln und Streben die Lasten ableitet und die
Zwischenräume (Gefache) mit nichttragendem Material gefüllt sind.
**[HART]**[^wiki-fachwerk][^rdklabor]

Die drei Definitionsmerkmale sind konstruktiv untrennbar:

1. **Tragendes Holzgerüst** — Ständer, Riegel, Streben übernehmen alle
   statischen Funktionen. Weder die Füllung noch die Außenwand trägt.
2. **Nichtragende Gefache** — die Felder zwischen den Hölzern sind
   strukturell entlastet. Füllmaterial (Lehm, Flechtwerk, Ziegel) ist
   austauschbar, ohne die Tragwerklogik zu berühren.
3. **Zimmermannsmäßige Verbindungen** — die Hölzer werden durch Zapfen,
   Blätter und Überblattungen verbunden, unter weitgehendem Verzicht auf
   metallische Verbindungsmittel. **[HART]**[^wiki-fachwerk]

Der Begriff *Fachwerk* ist seit dem 17. Jahrhundert belegt. *Fach* und
*Gefach* bezeichnen die durch die tragenden Balken gebildeten
Zwischenräume; *-werk* ist das zugehörige Kollektivum. **[HART]**[^wiki-fachwerk]

Das älteste dendrochronologisch datierte Fachwerkhaus in Deutschland
steht in Esslingen am Neckar (Heugasse 3, 1262/63). **[HART]**[^wiki-fachwerk]
Dieser Befund markiert den Übergang von der älteren Pfostenbauweise zur
Ständerbauweise um die Mitte des 13. Jahrhunderts.

---

## 2. Einbettung in die Baukonstruktionslehre

Die Baukonstruktionslehre unterscheidet vier Grundprinzipien des Tragwerks:
Massenbau, Massivbau (Flächenbau), Skelettbau und räumliches Tragwerk.
**[HART]**[^lernhelfer-skelett]

Fachwerk gehört zum **Skelettbau** (auch: Gerippebau, Gliederbau):
Tragwerk und Raumabschluss sind voneinander entkoppelt; die Wand übernimmt
nur noch raumabschließende, keine statische Funktion. **[HART]**[^wiki-skelettbau]
Diese Entkopplung ist das konstruktive Prinzip, das Fachwerk von Massivbau
und Blockbau unterscheidet — und die Grundlage jeder Baugrammatik, die
BVILLAGE kennt.

---

## 3. Vorläufer: Pfostenbau

Die direkte Vorstufe des Fachwerkbaus ist der **Pfostenbau**. Die
Unterscheidung ist für BVILLAGE relevant, weil sie die untere zeitliche
Grenze des Systems definiert.

Beim Pfostenbau werden die stehenden Konstruktionselemente bis zu einem
Meter tief in den Erdboden eingegraben. **[HART]**[^wiki-pfostenhaus]
Das gibt der Konstruktion Halt ohne Schwellbalken — aber der direkte
Erdkontakt führt zur Fäulnis; Pfostenhäuser hielten 30 bis maximal
50 Jahre. **[HART]**[^wiki-pfostenhaus]

Ab etwa 1250 wurden Wandpfosten stattdessen auf Schwellbalken aufgelegt.
**[HART]**[^regionalgeschichte] Dieser Wechsel — Pfosten werden zu
Ständern, Schwellbalken ersetzen den Erdbodenkontakt — markiert den
Übergang zum Fachwerk im engeren Sinn. **[HART]**[^wiki-ständerbauweise]

> **Pfostenbau ≠ Fachwerk.** Fachwerk beginnt mit dem Schwellbalken.
> BVILLAGE generiert keine Pfostenbauten.

---

## 4. Abgrenzung zu verwandten Bauweisen

### 4.1 Abgrenzungsmatrix

| Bauweise | Tragendes Element | Gefache / Füllung | Fachwerk? |
|---|---|---|---|
| Fachwerkbau | Holzgerüst (Ständer, Riegel, Streben) | Nichttragend (Lehm, Ziegel, Flechtwerk) | **Ja** |
| Pfostenbau | Im Erdreich eingegrabene Pfosten | Flechtwerk, Bohlen | **Nein** — kein Schwellbalken |
| Blockbau | Horizontal geschichtete Stämme | keine — Wand ist Tragwerk | **Nein** — Massivbauweise |
| Ständerbohlenbau | Holzgerüst (wie Fachwerk) | Holzbohlen in Nuten | **Grenzfall** — Gefache aus Holz |
| Stabholzbau | Senkrechte Stäbe | keine | **Nein** — eigene Tradition |
| Massivbau / Steinbau | Mauerwerk | keine — Wand ist Tragwerk | **Nein** |
| Bundwerk (Alpenraum) | Wie Stockwerkbau, mit Bundbalken | Holz oder Lehm | **Verwandt**, Spätform |
| Holzrahmenbau (modern) | Vorgefertigte Rahmenelemente | Isolierplatten | **Moderner Nachfolger** |

### 4.2 Fachwerk und Blockbau

Blockbau ist das konstruktive Gegenstück zum Fachwerk: Wand und Tragwerk
sind beim Blockbau ein identisches Bauteil — horizontal geschichtete
Stämme, deren Eigengewicht und gegenseitige Verknotung die Stabilität
erzeugen. **[HART]**[^wiki-massivbau]

Die Grenze ist in der historischen Baupraxis nicht immer scharf. Das
**Umgebindehaus** der Oberlausitz kombiniert einen Blockbaukern (Stube)
mit einem umgebenden Fachwerk-Außengefüge — ein historisch dokumentierter
Hybridtyp. **[HART]**[^wiki-fachwerk-haus] In BVILLAGE erhält dieser Typ
den Archetyp `FW-UMG` mit einer eigenen `hybrid_strategy`.

> **[AUSSTEHEND]** `hybrid_strategy` für `FW-UMG` ist konzeptionell noch
> nicht definiert. Primärquellen zur Oberlausitz-Bautradition fehlen.
> Siehe `RES_ARCHETYPE_SONDERFAELLE.md`.

Für alle anderen Archetypen gilt: Blockbau und Fachwerk schließen sich
als `construction_grammar` gegenseitig aus.

### 4.3 Fachwerk und Ständerbohlenbau

Der **Ständerbohlenbau** verwendet dasselbe Holzgerüst wie der Fachwerkbau —
der konstruktive Unterschied liegt allein im Füllmaterial: Statt Lehm oder
Ziegel werden Holzbohlen in eingefräste Nuten eingeschoben.
**[HART]**[^rdklabor]

Das RDK Labor dokumentiert beide Bauweisen oft am selben Gebäude, besonders
in der Schweiz, im Bodenseegebiet und in Oberschwaben. **[HART]**[^rdklabor]

Für BVILLAGE gilt: Ständerbohlenbau teilt die `construction_grammar` mit
Fachwerk; die Unterscheidung zwischen Lehm- und Holzgefache ist ein
`infill_material`-Parameter, kein Grammatikwechsel.

### 4.4 Fachwerk und Massivbau

Beim Massivbau übernehmen raumabschließende Wände zugleich die statisch
tragende Funktion — Tragwerk und Raumabschluss sind nicht getrennt.
**[HART]**[^wiki-massivbau]

Historisch konkurrierten Steinbau und Fachwerkbau in Städten direkt.
Mischformen (Holzhaus mit Steinkeller, Steinhaus mit Fachwerkgeschoss)
sind dokumentiert. **[MITTEL]**[^loebbecke]

Für BVILLAGE: Massivbau und Steinwerk liegen außerhalb des Generierungsscope.
Mischformen können als `ground_floor_material`-Parameter abgebildet werden,
ändern aber die `construction_grammar` nicht.

### 4.5 Geographische und zeitliche Grenzen

Fachwerk im engeren Sinn war vom frühen Mittelalter bis ins 19. Jahrhundert
die dominierende Hochbautechnik nördlich der Alpen in Deutschland, Teilen
Frankreichs, England und Skandinavien. **[HART]**[^wiki-fachwerk][^de-academic]

Fachwerkkonstruktionen sind auch aus dem ehemaligen osmanischen Reich
bekannt — dort aber als regionale Tradition ohne direkten Zusammenhang zur
mitteleuropäischen Entwicklung. **[MITTEL]**[^de-academic]

> **[AUSSTEHEND]** Osmanisches Fachwerk ist als zukünftiger
> `CulturePolicy`-Branch `ottoman_timber_frame` vorgesehen.
> Bis dahin: BVILLAGE beschränkt sich auf den mitteleuropäisch-englischen
> Kernraum. Siehe `RES_FACHWERK_OSMANISCH.md` (zukünftig).

---

## 5. Klassifikationsachsen

### 5.1 Keine einheitliche Metataxonomie

Die Hausforschung kennt keine universelle Klassifikationshierarchie.
Stattdessen arbeitet sie mit einem Kanon **orthogonaler Klassifikationsachsen**,
die je nach Fragestellung kombiniert werden. Denkmalpflege-Datenbanken
(z. B. Landesamt Baden-Württemberg) erfassen jedes Gebäude nach Form,
Funktion und Konstruktion als Mindestmenge. **[HART]**[^bw-db]

Das veraltete **Drei-Stämme-Modell** (sächsisch, fränkisch, alemannisch)
ist wissenschaftlich aufgegeben. **[HART]**[^grossmann-voelkisch] Für
BVILLAGE gilt: Regional-Bezeichnungen wie `FW-LH-ND` (Niederdeutsches
Hallenhaus) sind geographisch-konstruktiv, nicht ethnisch.

### 5.2 Die fünf Klassifikationsachsen

Ein Gebäude in BVILLAGE wird durch fünf orthogonale Achsen beschrieben.
Jede Achse beantwortet eine eigene, klar abgegrenzte Frage. Keine Achse
darf Wissen der anderen tragen.

---

**Achse 1 — Baugrammatik** (`construction_grammar`)
*Wie steht das Gebäude?*

Strukturgrammatik und Lastpfad. Diese Achse definiert, welche Member
erzeugt werden, wie Lasten fließen, welche Verbindungstypen möglich sind.
Wechsel dieser Achse ist kein Stilwechsel — er ist ein Strukturbruch.

Zuständige Systemkomponenten: `DomainConstructor`, `PhysicalPlausibilityValidator`,
`ConstructionCulturePolicy`.

> **Regel:** Strukturelle Unterschiede werden nie als `StylePolicy`-Varianten
> codiert. Wenn eine regionale Variation andere Member, andere Lastpfade
> oder andere Validierungslogik erfordert, ist das eine neue
> `construction_grammar` oder ein neuer `CulturePolicy`-Branch.

---

**Achse 2 — Archetyp** (`archetype`)
*Wie ist das Gebäude organisiert?*

Reine Topologie: Zonanordnung, Zirkulationslogik, Öffnungsprogramm,
Raumhierarchie. Ein Hallenhaus in Westfalen und eines in Mecklenburg
teilen denselben `archetype_id`.

Zuständige Systemkomponenten: `TypePlanner`, `InteriorPlanner`.

> **Regel:** Nutzung ist kein Bestandteil des Archetyps. Wenn zwei
> Gebäude dieselbe Zonanordnung haben, aber unterschiedliche Nutzung,
> ist das kein Grund für unterschiedliche `archetype_id`.
> Nutzungsunterschiede gehören ausschließlich in Achse 3.

---

**Achse 3 — Nutzungstyp** (`FunctionPolicy`)
*Wozu dient das Gebäude?*

Nutzungstyp und wirtschaftliche Funktion. `FunctionPolicy` steuert:
Zonenprogramm, Öffnungsanforderungen, Repräsentationsrichtung, Integration
von Tiernutzung, Lageranteil, kommerzielle Straßenfront.

```python
@dataclass(slots=True)
class FunctionPolicy:
    building_use: BuildingUse
    # Werte: RESIDENTIAL | AGRICULTURAL | STORAGE | CIVIC | RELIGIOUS | MIXED

    representation_direction: RepresentationDirection | None
    # Werte: STREET_FACING | COURTYARD_FACING | NONE

    livestock_integration: bool
    # True: Mensch-Tier-Integration unter einem Dach (Hallenhaus-Logik)

    storage_ratio: float
    # 0.0–1.0: Anteil Lagerraum am Gesamtvolumen

    commercial_frontage: bool
    # True: straßenseitige Handelsnutzung (Bürgerhaus, Ackerbürgerhaus)
```

Default: `building_use=RESIDENTIAL`, alle anderen Felder neutral.

> **Regel:** `FunctionPolicy` ist ein Pflichtparameter für jeden
> `HouseRequest`. Default-Werte sind zulässig. Fehlende `FunctionPolicy`
> im Stack ist ein Fehler.

---

**Achse 4 — Morphologie** (`RoofPolicy`, `VerticalPolicy`, `TopologyModifier`)
*Wie sieht das Gebäude aus?*

Gebäudeform, Dachtyp, Geschosszahl, Vorkragungen, Orientierung.
Diese Achse ist bereits vollständig im System vorhanden.

> **Regel:** Morphologische Unterschiede zwischen regional verwandten
> Gebäudetypen werden nie als separate `archetype_id` codiert. Sie sind
> `RoofPolicy`- oder `VerticalPolicy`-Varianten.

---

**Achse 5 — Kulturraum** (`StylePolicy`, `epoch_band`, `region`)
*Wann und wo steht das Gebäude?*

Kulturraum, Epoche, Wohlstand, Siedlungstyp. `StylePolicy` trägt das
Kreuzprodukt region × epoch × wealth × settlement_type.

> **Regel:** Epochale Diskontinuitäten (Pest 1347, Holzmangel ca.
> 1400–1520, Dreißigjähriger Krieg 1618–1648) sind harte Sprünge in
> `epoch_band`-Policy-Parametern, keine Gradienten.

---

### 5.3 Orthogonalitätsprinzip

Die fünf Achsen sind orthogonal. Wissen einer Achse darf nicht in einer
anderen codiert werden. Verletzungen sind die Hauptquelle technischer
Schulden im System.

Entscheidungsregeln bei Klassifikationszweifeln:

| Frage | Antwort | Achse |
|---|---|---|
| Andere Lastpfade oder Member? | Neue `construction_grammar` | 1 |
| Andere Zonanordnung oder Raumhierarchie? | Neuer Archetyp oder `TopologyModifier` | 2 |
| Andere Nutzung bei gleicher Topologie? | `FunctionPolicy`-Variante | 3 |
| Anderer Dachtyp, Geschosszahl, Orientierung? | `RoofPolicy` / `VerticalPolicy` | 4 |
| Andere Region, Epoche, Wohlstand? | `StylePolicy`-Variante | 5 |

### 5.4 Dokumentierte Systemlücke: Achse 3

Die **kritische Lücke** ist Achse 3 (Nutzungstyp). In der Hausforschung
sind ein Bauernhallenhaus und ein adliges Herrenhaushallenhaus konstruktiv
identisch — sozial aber kategorial verschieden. BVILLAGE bildet das
derzeit nicht vollständig ab.

`settlement_type`, `wealth` und `ConstructionCulturePolicy` tragen bereits
verwandte Informationen. Ein formaler `building_use`-Parameter würde Achse 3
explizit machen — insbesondere für `FW-LH-ND`, `FW-AIS` und `FW-SPC`, die
sich konstruktiv überschneiden, aber nutzungsseitig disjunkt sind.

Folgende Dokumente sind bei Einführung von `FunctionPolicy` anzupassen:

| Dokument | Anpassungsbedarf |
|---|---|
| `ARCH_POLICIES.md` | `FunctionPolicy` als Secondary Axis in §3 einfügen |
| `SYS_CONCEPTS.md` | Policy-Stack in §2 um `FunctionPolicy` erweitern |
| `ARCH_TAXONOMY.md` | Implizite Nutzungsannahmen in Archetyp-Beschreibungen dokumentieren |
| `SYS_CONTRACT.md` | `HouseRequest`-Schema: `FunctionPolicy` als Pflichtfeld |

---

## 6. Offene Forschungsfelder

| ID | Thema | Status | Zieldokument |
|---|---|---|---|
| DEF-001 | `hybrid_strategy` für Umgebindehaus (Blockbau-Kern + Fachwerk) | Konzeptionell offen | `RES_ARCHETYPE_SONDERFAELLE.md` |
| DEF-002 | Osmanisches / osteuropäisches Fachwerk als eigener Branch | Zurückgestellt | `RES_FACHWERK_OSMANISCH.md` (zukünftig) |
| DEF-003 | Formaler `FunctionPolicy`-Parameter im Policy-Stack | Systemarchitektur offen | `ARCH_POLICIES.md`, `SYS_CONTRACT.md` |

---

## 7. Quellen

[^wiki-fachwerk]: Fachwerkhaus. Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Fachwerkhaus

[^rdklabor]: Fachwerk, Fachwerkbau. Reallexikon zur Deutschen
  Kunstgeschichte (RDK Labor), März 2026.
  https://www.rdklabor.de/wiki/Fachwerk,_Fachwerkbau

[^wiki-skelettbau]: Skelettbau. Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Skelettbau

[^wiki-massivbau]: Massivbau. Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Massivbau

[^lernhelfer-skelett]: Skelettbau (Gliederbau). Duden Lernhelfer, März 2026.
  https://www.lernhelfer.de/schuelerlexikon/kunst/artikel/konstruktionsprinzipien-skelettbau-gliederbau

[^wiki-pfostenhaus]: Pfostenhaus. Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Pfostenhaus

[^wiki-ständerbauweise]: Ständerbauweise. Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Ständerbauweise

[^regionalgeschichte]: Fachwerk. Regionalgeschichte.net, März 2026.
  https://www.regionalgeschichte.net/bibliothek/glossar/begriffe/eintrag/fachwerk.html

[^de-academic]: Fachwerkhaus. De-Academic, März 2026.
  https://de-academic.com/dic.nsf/dewiki/425843

[^wiki-fachwerk-haus]: Fachwerkhaus (Umgebindehaus). Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Fachwerkhaus

[^loebbecke]: Frank Löbbecke: Hochmittelalterliche Holz-Stein-Bauten in
  Südwestdeutschland. Archaia Brno, PDF.
  https://www.archaiabrno.org/media/doc/02_fuma_ii_loebbecke_de.pdf

[^bw-db]: Denkmalpflege Baden-Württemberg: Bauforschung-Restaurierung,
  Datenbank, 2004.
  https://www.denkmalpflege-bw.de/denkmale/datenbanken/bauforschung-restaurierung

[^grossmann-voelkisch]: G. Ulrich Großmann: Völkisch und national —
  Der „Beitrag" der Hausforschung. In: Puschner/Großmann (Hg.),
  Darmstadt 2009.
  https://archiv.ub.uni-heidelberg.de/artdok/2688/1/Grossmann_VoelkischundNational_2009.pdf

---

*Status: Freigegeben als REFERENCE-Dokument. Version 1.0.*
*© 2026 Alexander Bernardi — CC-BY-SA 4.0*
