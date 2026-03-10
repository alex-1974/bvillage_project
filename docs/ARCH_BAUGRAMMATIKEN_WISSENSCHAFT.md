# Baugrammatiken und Archetypen der europäischen Fachwerkarchitektur
## Definition, Abgrenzung, Klassifikationsachsen und Systemempfehlung

---

```yaml
tier: 2
authority: REFERENCE
status: Freigegeben
version: 2.2
datum: 2026-03-07
references: ARCH_TAXONOMY.md, SYS_PRINCIPLES.md §3–4, ARCH_POLICIES.md §2
```

---

## 0. Methodik und Evidenzgrade

Für jede inhaltliche Behauptung wird der Evidenzgrad angegeben:

- **[HART]** — durch mehrere unabhängige akademische Quellen gesichert
- **[MITTEL]** — durch eine Primärquelle oder übereinstimmende Sekundärquellen gestützt
- **[SCHWACH]** — plausibel, aber noch nicht durch Primärliteratur verifiziert

Quellenkürzel in Fußnoten am Ende des Dokuments. Code-Bezeichner
(Klassen, Members, Variablen, Funktionssignaturen) sind durchgehend Englisch.

---

## 1. Definition: Was ist Fachwerk?

### 1.1 Kerndefinition

Fachwerk bezeichnet eine **Skelettbauweise aus Holz**, bei der ein tragendes
Gerüst aus Ständern, Riegeln und Streben die Lasten ableitet und die
Zwischenräume (Gefache) mit nichttragendem Material gefüllt sind.
**[HART]**[^wiki-fachwerk][^rdklabor]

Die drei Definitionsmerkmale sind konstruktiv untrennbar:

1. **Tragendes Holzgerüst** — Ständer, Riegel, Streben übernehmen alle
   statischen Funktionen. Weder die Füllung noch die Außenwand trägt.
2. **Nichttragede Gefache** — die Felder zwischen den Hölzern sind
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
Dieser Befund markiert zugleich den Übergang von der älteren
Pfostenbauweise zur Ständerbauweise um die Mitte des 13. Jahrhunderts.

### 1.2 Einbettung in die Baukonstruktionslehre

Die Baukonstruktionslehre unterscheidet vier Grundprinzipien des
Tragwerks: Massenbau, Massivbau (Flächenbau), Skelettbau und räumliches
Tragwerk. **[HART]**[^lernhelfer-skelett]

Fachwerk gehört zum **Skelettbau** (auch: Gerippebau, Gliederbau):
Tragwerk und Raumabschluss sind voneinander entkoppelt; die Wand
übernimmt nur noch raumabschließende, keine statische Funktion.
**[HART]**[^wiki-skelettbau] Diese Entkopplung ist das konstruktive
Prinzip, das Fachwerk von Massivbau und Blockbau unterscheidet —
und die Grundlage jeder Baugrammatik, die BVILLAGE kennt.

### 1.3 Vorläufer: Pfostenbau

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
Damit gilt:

> **Pfostenbau ≠ Fachwerk.** Fachwerk beginnt mit dem Schwellbalken.
> BVILLAGE generiert keine Pfostenbauten.

---

## 2. Abgrenzung zu verwandten Bauweisen

Fachwerk ist eine spezifische Form des Holzgerüstbaus. Die Abgrenzung
zu anderen Holz- und Massivbauweisen ist sowohl historisch als auch für
die `construction_grammar`-Klassifikation in BVILLAGE relevant.

### 2.1 Abgrenzungsmatrix

| Bauweise | Tragendes Element | Gefache / Füllung | Fachwerk? |
|---|---|---|---|
| Fachwerkbau | Holzgerüst (Ständer, Riegel, Streben) | Nichttragend (Lehm, Ziegel, Flechtwerk) | **Ja** |
| Pfostenbau | Im Erdreich eingegrabene Pfosten | Flechtwerk, Bohlen | **Nein** — kein Schwellbalken |
| Blockbau | Horizontal geschichtete Stämme (die Wand trägt) | keine — Wand ist Tragwerk | **Nein** — Massivbauweise |
| Ständerbohlenbau | Holzgerüst (wie Fachwerk) | Holzbohlen in Nuten | **Grenzfall** — Gefache aus Holz |
| Stabholzbau | Senkrechte Stäbe | keine | **Nein** — eigene Tradition |
| Massivbau / Steinbau | Mauerwerk | keine — Wand ist Tragwerk | **Nein** |
| Steinwerk | Massives Mauerwerk (städtisch) | keine | **Nein** |
| Bundwerk (Alpenraum) | Wie Stockwerkbau, mit Bundbalken | Holz oder Lehm | **Verwandt**, Spätform |
| Holzrahmenbau (modern) | Vorgefertigte Rahmenelemente | Isolierplatten | **Moderner Nachfolger** |

### 2.2 Fachwerk und Blockbau

Blockbau ist das konstruktive Gegenstück zum Fachwerk: Wand und
Tragwerk sind beim Blockbau ein identisches Bauteil — horizontal
geschichtete Stämme, deren Eigengewicht und gegenseitige Verknotung
die Stabilität erzeugen. **[HART]**[^wiki-massivbau]

Die Grenze ist in der historischen Baupraxis nicht immer scharf. Das
**Umgebindehaus** der Oberlausitz kombiniert einen Blockbaukern
(Stube) mit einem umgebenden Fachwerk-Außengefüge — ein historisch
dokumentierter Hybridtyp. **[HART]**[^wiki-fachwerk-haus] In BVILLAGE
erhält dieser Typ den Archetyp `FW-UMG` mit einer eigenen
`hybrid_strategy` (noch offen, siehe §7).

Für alle anderen Archetypen gilt: Blockbau und Fachwerk schließen
sich als `construction_grammar` gegenseitig aus.

### 2.3 Fachwerk und Ständerbohlenbau

Der **Ständerbohlenbau** verwendet dasselbe Holzgerüst wie der
Fachwerkbau — der konstruktive Unterschied liegt allein im
Füllmaterial: Statt Lehm oder Ziegel werden Holzbohlen in
eingefräste Nuten eingeschoben. **[HART]**[^rdklabor]

Das RDK Labor dokumentiert beide Bauweisen oft am selben Gebäude,
besonders in der Schweiz, im Bodenseegebiet und in Oberschwaben.
**[HART]**[^rdklabor] Konstruktiv ist Ständerbohlenbau ein
Fachwerk mit Holzgefache — die Gerüstlogik ist identisch.

Für BVILLAGE gilt: Ständerbohlenbau teilt die `construction_grammar`
mit Fachwerk; die Unterscheidung zwischen Lehm- und Holzgefache ist
ein `infill_material`-Parameter, kein Grammatikwechsel.

### 2.4 Fachwerk und Massivbau / Steinbau

Beim Massivbau übernehmen raumabschließende Wände und Decken zugleich
die statisch tragende Funktion — Tragwerk und Raumabschluss sind
nicht getrennt. **[HART]**[^wiki-massivbau] Historisch konkurrierten
Steinbau und Fachwerkbau in Städten direkt: In Freiburg im Breisgau
wurde im 12. Jahrhundert der straßenseitige Holzbau oft durch einen
steinernen Hofbau ergänzt; Mischformen (Holzhaus mit Steinkeller,
Steinhaus mit Fachwerkgeschoss) sind dokumentiert. **[MITTEL]**[^loebbecke]

Für BVILLAGE: Massivbau und Steinwerk liegen außerhalb des
Generierungsscope. Mischformen (Erdgeschoss Stein, Obergeschoss
Fachwerk) können als `ground_floor_material`-Parameter abgebildet
werden, ändern aber die `construction_grammar` nicht.

### 2.5 Geographische und zeitliche Grenzen

Fachwerk im engeren Sinn — auf Schwellbalken aufgestelltes,
zimmermannsmäßig verbundenes Holzgerüst mit nichttragendem Gefache —
war vom frühen Mittelalter bis ins 19. Jahrhundert die dominierende
Hochbautechnik nördlich der Alpen in Deutschland, Teilen Frankreichs,
England und Skandinavien. **[HART]**[^wiki-fachwerk][^de-academic]

Fachwerkkonstruktionen sind auch aus dem ehemaligen osmanischen Reich
(Bulgarien bis Syrien) bekannt — dort aber als regionale Tradition
ohne direkten Zusammenhang zur mitteleuropäischen Entwicklung.
**[MITTEL]**[^de-academic] BVILLAGE beschränkt sich auf den
mitteleuropäisch-englischen Kernraum.

---

## 3. Zeitliche Entwicklung

Die konstruktive Entwicklung verlief nicht linear, sondern in
unterscheidbaren Epochen mit regional unterschiedlicher Geschwindigkeit:

- **Pfostenbau** bis ca. 1250 — Vorläufer, kein Fachwerk im engeren Sinn.
- **Ständerbau** ab ca. 1250 als erste vollständige Fachwerkform:
  Ständer durchgehend von Schwelle bis Dachgebälk. **[HART]**[^hessenpark]
- **Übergang zum Stockwerkbau** in Mittel- und Oberdeutschland
  ca. 1470–1580. **[HART]**[^hessenpark] Auslöser: vermutlich
  Holzmangel im Umfeld wachsender Städte sowie der Wunsch nach
  kürzeren, leichter transportierbaren Hölzern. **[MITTEL]**[^wiki-fachwerk]
  Das älteste bekannte Stockwerkbaubeispiel: Bäckerhaus Eppingen, 1412.
  **[HART]**[^wiki-fachwerk]
- **Regionale Persistenz des Ständerbaus** bis ins 19. Jahrhundert,
  etwa im fränkischen Fachwerk. **[HART]**[^wiki-ständerbauweise]
- **Ende des Fachwerkbaus** mit der Industrialisierung: Mineralische
  und metallische Baustoffe verdrängten Holz; Massivbau galt als
  werthaltiger. **[HART]**[^wiki-fachwerk-haus]

Diese Epochen funktionieren in BVILLAGE als harte Diskontinuitäten
in den `epoch_band`-Policy-Parametern, nicht als Gradienten.
Innerhalb jeder Epoche bleibt die **Baugrammatik** stabil —
der Übergang zwischen Ständerbau und Stockwerkbau ist kein Gradient,
sondern ein Grammatikbruch.

---

## 4. Die fünf Baugrammatiken

### 4.1 `BOX_FRAME`

**Primärstruktur:** `binder_sequence` — durchgehende Ständer, gebäudehoch.

Beim Ständerbau laufen die Wandständer von der Schwelle bis zum
Traufrähm durch. Deckenbalken sind in die Ständer eingezapft oder
überblattet. Die Dachlast wird über diese Ständer direkt zur Schwelle
und zum Fundament geleitet. **[HART]**[^rdklabor] Das Haus entsteht
als Sequenz tragender Querrahmen (`frame`). **[HART]**[^rdklabor]

Varianten (Zwei-, Drei-, Vierständer) unterscheiden sich durch die
Anzahl innerer Stützenreihen und die Spannweiten — diese sind
`policy_parameters`, keine separaten Baugrammatiken.
**[MITTEL]**[^wiki-timber-framing]

Aisled Frames (englische Hallenhäuser mit inneren Stützenreihen)
werden in der englischen Fachliteratur als strukturell verwandt
mit dem norddeutschen Ständerhaus behandelt.[^wiki-timber-framing]
**[MITTEL]** Die strukturelle Eigenständigkeit des Aisled-Typs
(Arkadenreihe als Primäreinheit) rechtfertigt dennoch einen
eigenen `IFrameProducer` — siehe §4.4.

> **`frame_producer_class`:** `BoxFrameProducer`
> **`construction_grammar`:** `BOX_FRAME`
> **`entry_point`:** `derive_binder_sequence(frame_plan: FramePlan) -> BoundFrame`

---

### 4.2 `STOREY_FRAME`

**Primärstruktur:** `storey_frames` — gestapelte, autonome Geschosseinheiten.

Beim Stockwerkbau bildet jedes Geschoss eine in sich geschlossene
Einheit aus Schwelle, Ständern und Rähm. Diese Einheiten werden
gestapelt; jedes Geschoss wird separat abgebunden und aufgerichtet.
**[HART]**[^rdklabor][^hessenpark] Vorkragungen (`jettying`) entstehen
durch vorstehende Deckenbalken — eine typische Konsequenz dieser
Baugrammatik. **[HART]**[^stockwerkbau]

Der Begriff *Rähmbau* ist veraltet. Korrekt: **Stockwerkbau** oder
**Stockwerkbauweise**. Das *Bildwörterbuch der Architektur*
(Koepf/Binding 2005) und Wikipedia/Rähm führen dies explizit aus.
**[HART]**[^raehm] Der interne Klassenname `StoreyFrameProducer`
folgt dem korrekten englischen Fachbegriff.

> **`frame_producer_class`:** `StoreyFrameProducer`
> **`construction_grammar`:** `STOREY_FRAME`
> **`entry_point`:** `derive_storey_frames(frame_plan: FramePlan) -> BoundStoreyStack`

---

### 4.3 `CRUCK_FRAME`

**Primärstruktur:** `cruck_pairs` — Dachtragwerk als Primärrahmen.

Zwei gebogene oder gerade Hölzer (`cruck_blades`) bilden einen
A-Rahmen, der von nahe Bodenniveau bis zum Dachfirst reicht.
Dach- und Wandtragwerk sind in einem einzigen Member vereint.
Die Außenwände sind strukturell sekundär. **[HART]**[^cruck-northhouse]

Der Lastpfad ist invertiert gegenüber allen anderen Baugrammatiken:
Dach → Boden, nicht Wand → Boden. Dies macht `CRUCK_FRAME` zu einer
konstruktiv eigenständigen Baugrammatik, nicht zu einer Variante von
`BOX_FRAME`. **[HART]**[^cruck-northhouse]

Historische Varianten (Full Cruck, Jointed Cruck, Raised Cruck)
unterscheiden sich in der Ansatzhöhe der `blades`, nicht in der
grundlegenden Logik. **[HART]** Raised Crucks beginnen oberhalb
des Wandfußes und kommen fast ausschließlich in Steinwandgebäuden
vor. **[MITTEL]**[^bard-glossary]

Geographische Eingrenzung: England und Wales (gesichert). Westfrankreich
peripher. Ein Befund nennt Deutschland und die Niederlande (1. Jh.),
ist aber in der Primärliteratur nicht gestützt. **[SCHWACH]**
Kanonisches Standardwerk: N. W. Alcock, *Cruck Construction*,
CBA 1981. **[HART]**[^timber-framers-guild]

> **`frame_producer_class`:** `CruckFrameProducer`
> **`construction_grammar`:** `CRUCK_FRAME`
> **`entry_point`:** `derive_cruck_pairs(frame_plan: FramePlan) -> BoundCruckFrame`

---

### 4.4 `AISLED_FRAME`

**Primärstruktur:** `arcade_rows` — innere Stützenreihen als struktureller Kern.

Aisled-Konstruktionen schaffen große Hallenräume, indem innere
Stützenreihen (`arcade_posts`) die Dachspannweite unterteilen. Das
Mittelschiff (`nave`) bestimmt die Primärspannweite; die Seitenschiffe
(`aisles`) werden davon abgeleitet. **[HART]**[^wiki-timber-framing]

Die VAG Aisled Buildings Database dokumentiert 391 aisled halls und
2.127 aisled barns in England und Wales. Das älteste bekannte
Beispiel (Cressing Temple barn) datiert auf 1205–1235.
**[HART]**[^vag-aisled]

Die Arkadenreihe, nicht der einzelne Binder, ist die Primäreinheit
der Generierung — das ist der konstruktive Unterschied zu
`BOX_FRAME`. Die englische Fachliteratur bestätigt diese
Eigenständigkeit. **[HART]**[^vag-aisled]

Hybridfall: Kombinierte Cruck-Aisled-Konstruktionen sind belegt
(Plas Uchaf, Wales, 1435). Dies ist ein `hybrid_archetype`,
kein Widerspruch zur Baugrammatiktrennung. **[HART]**[^hall-house-wiki]

> **`frame_producer_class`:** `AisledFrameProducer`
> **`construction_grammar`:** `AISLED_FRAME`
> **`entry_point`:** `derive_arcade_rows(frame_plan: FramePlan) -> BoundAisledFrame`

---

### 4.5 `WALL_GRID_FRAME` *(Phase 2)*

**Primärstruktur:** `frame_grid` — selbstausgesteiftes Wandraster.

Das Wandrastersystem strukturiert den Bau durch ein gleichmäßiges
Fassadenraster aus Pfosten (*poteaux*), Horizontalen (*sablières*)
und Diagonalen (*décharges*). Jede Ebene (Erdgeschoss, Obergeschoss,
Dachzone) ist eine autonome, selbstausgesteifte Einheit — in der
elsässischen Forschung beschrieben als Superposition von Einheiten,
die sich jeweils selbst aussteifen. **[HART]**[^pufr-alsace]

Abgrenzung zu `STOREY_FRAME`: Beide Baugrammatiken denken in Schichten.
`primary_unit` beim Stockwerkbau ist der Geschossrahmen; beim
Wandrastersystem ist es die Wandfläche. Die Eigenständigkeit dieser
Logik ist durch die elsässische Forschung wissenschaftlich
dokumentiert. **[HART]**[^pufr-alsace]

Terminologie: *pan de bois* bezeichnet das Konstruktionssystem;
*colombage* ist heute ein Sammelbegriff. Für BVILLAGE:
`WALL_GRID_FRAME` als `construction_grammar`-Bezeichner,
`pan de bois` als regionale Ausprägung. **[MITTEL]**[^wiki-colombages]

> **`frame_producer_class`:** `WallGridFrameProducer` *(Phase 2)*
> **`construction_grammar`:** `WALL_GRID_FRAME`
> **`entry_point`:** `derive_frame_grid(frame_plan: FramePlan) -> BoundWallGrid`

---

## 5. Zuordnung Baugrammatik → Frame Producer

```
BoxFrameProducer        construction_grammar = BOX_FRAME
                        archetypes: FW-LH-ND, FW-LH-2S/3S/4S,
                                    FW-GULF, FW-HAUB, FW-MITT,
                                    FW-WLD, FW-OHALL, FW-LH-EN

StoreyFrameProducer     construction_grammar = STOREY_FRAME
                        archetypes: FW-ER-MD, FW-HARZ,
                                    FW-STG-GIE, FW-STG-TRF,
                                    FW-ACK, FW-SPC, FW-MER, FW-HOF

CruckFrameProducer      construction_grammar = CRUCK_FRAME
                        archetypes: FW-CRK, FW-CRJ, FW-CRR

AisledFrameProducer     construction_grammar = AISLED_FRAME
                        archetypes: FW-AIS

WallGridFrameProducer   construction_grammar = WALL_GRID_FRAME  [Phase 2]
                        archetypes: FW-PDC, FW-COL
```

Begründung der Trennung `BoxFrameProducer` ≠ `AisledFrameProducer`:
Obwohl beide Stützenreihen verwenden, ist die `primary_unit`
verschieden. Beim Box Frame ist `frame` (Binder) die
Planungseinheit — die Baugrammatik denkt in Querrahmen. Beim
Aisled-System ist `arcade_row` primär und definiert die
Mittelschiffspannweite — die Baugrammatik denkt in Längsachsen.
VAG-Forschung bestätigt die strukturelle Eigenständigkeit.
**[HART]**[^vag-aisled]

`CruckFrameProducer` ist unvermeidlich eigenständig: Invertierter
Lastpfad (Dach → Boden) ist mit keiner anderen Baugrammatik
kompatibel. **[HART]**[^cruck-northhouse]

---

## 6. Archetypen-Inventar

**Begriffsklärung:** Ein *Archetyp* ist ein kategorial stabiles Raummuster,
das Varianten zulässt, ohne seine Identität zu verlieren. Der Begriff
stammt aus der Architekturtheorie (Rossi 1966) und der Hausforschung
(Schepers, Bedal), die beide dasselbe meinen: das invariante Grundgefüge
eines Gebäudetyps — Zonanordnung, Raumhierarchie, Zirkulationslogik —
unabhängig von Material, Region und Epoche. In BVILLAGE ist `archetype`
*ausschließlich* topologisch definiert. Er ist das Gegenstück zur
Baugrammatik: die Baugrammatik sagt, wie Member erzeugt werden;
der Archetyp sagt, in welcher räumlichen Ordnung sie angeordnet sind.

### 6.1 Korrektur: Wealden House

Das Wealden House ist ein Hallenhaus-Archetyp, kein Stockwerkbau.
Es besitzt eine zentrale, zur Dachzone offene Halle (`open_hall`)
flankiert von zweigeschossigen Endfeldern unter einem durchgehenden Dach.
**[HART]**[^vag-wealden][^oxford-wealden][^wiki-wealden]

Charakteristisch ist die `flying_wall_plate`: Da die Außenwand der
Mittelhalle nicht vorgekragt ist, läuft die Wandplatte über den
zurückgesetzten Hallenteil. Das ist strukturell unvereinbar mit
Stockwerklogik (gestapelte, autonome Geschossrahmen). **[HART]**[^vag-wealden]

**Korrektur:** `FW-WLD` — `construction_grammar = BOX_FRAME`
(nicht `STOREY_FRAME`). Zu ändern in `ARCH_TAXONOMY.md`.

### 6.2 Inventar

| `archetype_id` | Name | Region | Periode | `construction_grammar` | Evidenz |
|---|---|---|---|---|---|
| `FW-LH-ND` | Niederdeutsches Hallenhaus | Norddeutschland | 13–19. Jh. | `BOX_FRAME` | HART |
| `FW-LH-2S` | Hallenhaus Zweiständer | Norddeutschland | 15–18. Jh. | `BOX_FRAME` | HART |
| `FW-LH-3S` | Hallenhaus Dreiständer | Norddeutschland | 16–18. Jh. | `BOX_FRAME` | HART |
| `FW-LH-4S` | Hallenhaus Vierständer | Norddeutschland | 16–19. Jh. | `BOX_FRAME` | HART |
| `FW-GULF` | Gulfhaus | Nordseeküste | 16–19. Jh. | `BOX_FRAME` | MITTEL |
| `FW-HAUB` | Haubarg | Nordfriesland | 17–19. Jh. | `BOX_FRAME` | MITTEL |
| `FW-MITT` | Mittertennhaus | Alpenraum | 15–19. Jh. | `BOX_FRAME` | MITTEL |
| `FW-ER-MD` | Mitteldeutsches Ernhaus | Mittel-/Süddeutschland | 14–18. Jh. | `STOREY_FRAME` | MITTEL |
| `FW-HARZ` | Harzer Haus | Harzregion | 16–19. Jh. | `STOREY_FRAME` | MITTEL |
| `FW-STG-GIE` | Giebelständiges Stadthaus | Städte (D) | 14–18. Jh. | `STOREY_FRAME` | HART |
| `FW-STG-TRF` | Traufenständiges Stadthaus | Städte (D) | 15–18. Jh. | `STOREY_FRAME` | HART |
| `FW-ACK` | Ackerbürgerhaus | Kleinstädte (D) | 15–19. Jh. | `STOREY_FRAME` | MITTEL |
| `FW-SPC` | Speicherhaus | Städte | 15–18. Jh. | `STOREY_FRAME` | MITTEL |
| `FW-WLD` *(korr.)* | Wealden House | Südostengland | 14–16. Jh. | `BOX_FRAME` | HART |
| `FW-MER` | Merchant House | England, Niederlande | 14–17. Jh. | `STOREY_FRAME` | MITTEL |
| `FW-AIS` | Aisled Hall House | England, Niederlande | 12–16. Jh. | `AISLED_FRAME` | HART |
| `FW-OHALL` | Open Hall House | England | 13–16. Jh. | `BOX_FRAME` | HART |
| `FW-CRK` | Cruck House (Full Cruck) | England, Wales | 12–17. Jh. | `CRUCK_FRAME` | HART |
| `FW-CRJ` | Jointed Cruck House | Westengland | 13–16. Jh. | `CRUCK_FRAME` | MITTEL |
| `FW-CRR` | Raised Cruck House | England | 14–17. Jh. | `CRUCK_FRAME` | MITTEL |
| `FW-PDC` | Maison à pans de bois | Frankreich, Elsass | 14–18. Jh. | `WALL_GRID_FRAME` | HART |
| `FW-COL` | Colombage House | Normandie, Lothringen | 14–18. Jh. | `WALL_GRID_FRAME` | HART |
| `FW-UMG` | Umgebindehaus | Oberlausitz | 15–19. Jh. | `HYBRID` | MITTEL |
| `FW-HOF` | Fachwerk-Hofanlage | Mittel-/Süddeutschland | 16–19. Jh. | `STOREY_FRAME` | MITTEL |
| `FW-LH-EN` *(prov.)* | English Longhouse | England, Wales | 12–16. Jh. | `BOX_FRAME` | MITTEL |
| `FW-STV` *(prov.)* | Stavkirke-Grundtypus | Skandinavien | 11–14. Jh. | `BOX_FRAME` (tentativ) | SCHWACH |

---

## 7. Offene Fragen

| Typ | Problem | Status |
|-----|---------|--------|
| `FW-GULF` / `FW-HAUB` | `policy_variant` oder eigenständiger `archetype`? Spannweiten und Stützenlogik weichen erheblich ab. | Offen — Primärquellen nötig |
| `FW-UMG` | `hybrid_strategy` für Blockbau-Kern + Fachwerk-Umgebinde nicht definiert | Konzeptionell offen |
| `FW-STV` | Konstruktionslogik (Kernpfosten) weicht von `BOX_FRAME` ab; `SCHWACH`-Evidenz | Primärliteratur fehlt |
| `FW-LH-EN` | Abgrenzung zu `FW-OHALL` nicht vollständig belegt | Mercer 1975 als Ausgangspunkt |
| Niederlande/Flandern | Keine Primärquellen zu Dutch timber townhouse, Flemish guild house | Forschungslücke |
| Pan de bois intern | Zwei Subtypen (*poteaux de fond* vs. *étages superposés*) — in Phase 1 vereinfacht | Für Phase 2 zu differenzieren |
| `AISLED_FRAME` / Zweiständerhaus | Konzeptionelle Grenze zwischen deutschen Varianten und englischen Aisled Halls | Entscheidung ausstehend |

---

## 8. Wissenschaftliche Klassifikationssystematik

### 8.1 Keine einheitliche Metataxonomie

Die Hausforschung kennt keine universelle Klassifikationshierarchie.
Stattdessen arbeitet sie mit einem Kanon **orthogonaler Klassifikationsachsen**,
die je nach Fragestellung kombiniert werden. Denkmalpflege-Datenbanken
(z. B. Landesamt Baden-Württemberg) erfassen jedes Gebäude nach
**Form, Funktion und Konstruktion** als Mindestmenge.[^bw-db]
Englische Vernacular-Forschung (Brunskill, Mercer) ergänzt um Material
und sozialen Kontext.[^brunskill-function]

### 8.2 Die fünf Klassifikationsachsen

**Achse 1 — Baugrammatik**
Wie wird gebaut? Skelettbau vs. Massivbau vs. Blockbau; innerhalb
Skelettbau: `BOX_FRAME`, `STOREY_FRAME`, `CRUCK_FRAME`, `AISLED_FRAME`,
`WALL_GRID_FRAME`. In der Bautypologie-Literatur klar getrennt von der
Nutzungsklassifikation: Bauweise ist die Konstruktion im Hinblick
auf Materialien und Technologien, Bautypologie die Zuordnung nach
Architektur, Funktion oder Nutzung.[^wiki-bautypologie]

**Achse 2 — Archetyp**
Wie ist das Gebäude innen organisiert? Einschiffig, zweischiffig,
Halle + Kammern, Quergang, Diele, Kreuzgrundriss. Georg Landau
erkannte bereits um 1860, dass der Grundriss das konstanteste
Klassifikationsmerkmal ist, da er im Vergleich zu Material und
Zierformen über längere Perioden stabil bleibt.[^landau-grundriss]
Baugrammatik und Archetyp korrelieren, sind aber nicht identisch:
Derselbe Archetyp kann in `BOX_FRAME` oder `STOREY_FRAME`
ausgeführt werden.

**Achse 3 — Nutzungstyp / Sozialtyp**
Was und für wen ist das Gebäude? Bauernhaus, Bürgerhaus,
Ackerbürgerhaus, Herrenhaus, Speicherhaus, Sakralbau. Forschung
zeigt, dass gleiche Gefügeformen nicht zwangsläufig gleiche
Nutzungsstrukturen implizieren — ein dreischiffiges Hallenhaus kann
Bauernhof, Scheune oder Adelssitz sein.[^maschmeyer-nutzung]
Brunskill nennt Funktion explizit als den dominierenden Faktor
im vernacular building.[^brunskill-function]

**Achse 4 — Gebäudeform / Morphologie**
Wie sieht das Gebäude aus? Giebelständig vs. traufständig, Dachform,
Geschosszahl, Vorkragungen, Fassadengliederung. Relevante
Unterscheidungsmerkmale in wissenschaftlichen Katastern: Dachform,
Giebelwand, Raumabfolge, Erscheinungsbild, Dachkonstruktion.[^irb-merkmale]

**Achse 5 — Verbreitung / Kulturraum**
Wo und wann? Regionale Hauslandschaften, Kulturräume, dendrochronologische
Datierung. Hausforschung geht über Gefügekonstruktionen hinaus:
vergleichende Analysen regionaler Bauweisen, örtliche Besonderheiten
und zeittypische Formen gehören alle dazu.[^igbauernhaus-methoden]

### 8.3 Das veraltete „Drei-Stämme-Modell"

Bis ins frühe 20. Jahrhundert klassifizierte die deutsche Hausforschung
nach ethnisch-stammesmäßigen Kategorien (sächsisch, fränkisch,
alemannisch). Dieses Modell ist wissenschaftlich aufgegeben.[^grossmann-voelkisch]
Für BVILLAGE gilt: Regional-Bezeichnungen wie `FW-LH-ND`
(Niederdeutsches Hallenhaus) sind geographisch-konstruktiv, nicht
ethnisch — das ist korrekt und bleibt haltbar.

### 8.4 Einordnung von BVILLAGE

Der aktuelle BVILLAGE-`archetype` ist eine Synthese aus **Baugrammatik
(Achse 1) + Archetyp (Achse 2, implizit) + Kulturraum (Achse 5)**.
Das entspricht dem wissenschaftlichen Hauptstrom der Gefügeforschung
(Bedal, Schepers, VAG).

| Achse | Bezeichnung | BVILLAGE-Parameter | Status |
|---|---|---|---|
| 1 | Baugrammatik | `construction_grammar` | Explizit, vollständig |
| 2 | Archetyp | Implizit im `archetype_id` (Hallenhaus = Einraumhalle + Diele) | Kein formaler `floor_plan_type`-Parameter |
| 3 | Nutzungstyp | Nicht als eigenständige Dimension | `FW-LH-ND` und Scheune nicht trennbar |
| 4 | Morphologie | Teilweise in `StylePolicy` | Keine eigenständige Klassifikationsachse |
| 5 | Kulturraum | `region` + `epoch_band` | Explizit |

Die **kritische Lücke** ist Achse 3 (Nutzungstyp). In der
Hausforschung sind ein Bauernhallenhaus und ein adliges Herrenhaushallenhaus
konstruktiv identisch — sozial aber kategorial verschieden. BVILLAGE
bildet das derzeit nicht ab. Das ist keine Fehlerklasse, sondern eine
dokumentierte Designgrenze.

**BVILLAGE-Konsequenz:** Achse 3 ist direkt mit bestehenden Parametern
verknüpfbar: `settlement_type`, `wealth` und `ConstructionCulturePolicy`
tragen bereits die nötigen Informationen. Ein formaler `building_use`-Parameter
(Werte: `residential`, `agricultural`, `storage`, `civic`, `religious`)
würde Achse 3 explizit machen und die Archetypen-Auflösung deutlich
präzisieren — insbesondere für `FW-LH-ND`, `FW-AIS` und `FW-SPC`,
die sich konstruktiv überschneiden, aber nutzungsseitig disjunkt sind.

---

## 9. Klassifikationsachsen — normative Festlegung

> **Dieser Abschnitt ist normativ.** Er setzt Regeln fest, keine Empfehlungen.
> Bestehende Dokumente, die diesen Regeln widersprechen, sind anzupassen.
> Neue Komponenten, die diese Regeln verletzen, sind abzulehnen.

### 9.1 Die fünf bindenden Achsen

Ein Gebäude in BVILLAGE wird vollständig durch fünf orthogonale Achsen
beschrieben. Jede Achse beantwortet eine eigene, klar abgegrenzte Frage.
Keine Achse darf Wissen der anderen tragen.

---

**Achse 1 — Baugrammatik** (`construction_grammar`)
*Wie steht das Gebäude?*

Strukturgrammatik und Lastpfad. Diese Achse definiert, welche Member
erzeugt werden, wie Lasten fließen, welche Verbindungstypen möglich sind.
Wechsel dieser Achse ist kein Stilwechsel — er ist ein Strukturbruch.

Zuständige Systemkomponenten: `DomainConstructor`, `PhysicalPlausibilityValidator`,
`ConstructionCulturePolicy`.

> **Regel:** Strukturelle Unterschiede werden nie als `StylePolicy`-Varianten
> codiert. Wenn eine regionale Variation andere Member, andere Lastpfade oder
> andere Validierungslogik erfordert, ist das eine neue `construction_grammar`
> oder ein neuer `CulturePolicy`-Branch.

---

**Achse 2 — Archetyp** (`archetype`)
*Wie ist das Gebäude organisiert?*

Reine Topologie: Zonanordnung, Zirkulationslogik, Öffnungsprogramm,
Raumhierarchie. Der Archetyp definiert ausschließlich räumliche Logik —
keine Nutzung, keine Materialien, keine Regionalität. Ein Hallenhaus in
Westfalen und eines in Mecklenburg teilen denselben `archetype_id`.

Zuständige Systemkomponenten: `TypePlanner`, `InteriorPlanner`.

> **Regel:** Nutzung ist kein Bestandteil des Archetyps. Wenn zwei
> Gebäude dieselbe Zonanordnung und dieselbe Zirkulationslogik haben,
> aber unterschiedliche Nutzung, ist das **nicht** ein Grund für
> unterschiedliche `archetype_id`. Nutzungsunterschiede gehören
> ausschließlich in Achse 3.

> **Konsequenz für bestehende Einträge:** Archetypen, die implizit
> Nutzungsinformation tragen (z. B. `FW-LH-ND` mit eingebetteter
> Annahme „landwirtschaftlich"), sind nicht falsch — aber ihre
> Nutzungskomponente ist explizit nach Achse 3 auszulagern.

---

**Achse 3 — Nutzungstyp** (`FunctionPolicy`)
*Wozu dient das Gebäude?*

Nutzungstyp und wirtschaftliche Funktion. Diese Achse ist bisher nicht
first-class im Policy-Stack. Das ist ein Systemfehler. Sie wird hiermit
als **Secondary Axis** etabliert, positioniert zwischen `OpeningsPolicy`
und `StylePolicy`.

`FunctionPolicy` steuert: Zonenprogramm, Öffnungsanforderungen
(Scheunentor vs. Wohneingang), Repräsentationsrichtung, Integration
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
Bestehende Archetypen und Domains werden durch diesen Default nicht
berührt.

> **Regel:** `FunctionPolicy` ist ein Pflichtparameter für jeden
> `HouseRequest`. Default-Werte sind zulässig. Fehlende `FunctionPolicy`
> im Stack ist ein Fehler.

> **Konsequenz:** `FW-LH-ND` und eine Scheune gleichen Typs sind
> ab sofort über `FunctionPolicy.building_use` trennbar, ohne
> unterschiedliche `archetype_id` zu benötigen.

---

**Achse 4 — Morphologie** (`RoofPolicy`, `VerticalPolicy`, `TopologyModifier`)
*Wie sieht das Gebäude aus?*

Gebäudeform, Dachtyp, Geschosszahl, Vorkragungen, Orientierung.
Diese Achse ist bereits vollständig im System vorhanden als
Secondary Axes: `RoofPolicy`, `VerticalPolicy`, `TopologyModifier`,
`OpeningsPolicy`. Kein Handlungsbedarf.

> **Regel:** Morphologische Unterschiede zwischen regional verwandten
> Gebäudetypen werden nie als separate `archetype_id` codiert. Sie
> sind `RoofPolicy`- oder `VerticalPolicy`-Varianten.

---

**Achse 5 — Kulturraum** (`StylePolicy`, `epoch_band`, `region`)
*Wann und wo steht das Gebäude?*

Kulturraum, Epoche, Wohlstand, Siedlungstyp. Diese Achse ist bereits
vollständig vorhanden. `StylePolicy` trägt das Kreuzprodukt
region × epoch × wealth × settlement_type. Kein Handlungsbedarf.

> **Regel:** Epochale Diskontinuitäten (Pest 1347, Holzmangel ca.
> 1400–1520, Dreißigjähriger Krieg 1618–1648) sind harte Sprünge
> in `epoch_band`-Policy-Parametern, keine Gradienten.

---

### 9.2 Orthogonalitätsprinzip

Die fünf Achsen sind orthogonal. Wissen einer Achse darf nicht in
einer anderen codiert werden. Verletzungen dieser Regel sind die
Hauptquelle technischer Schulden im System.

Entscheidungsregeln bei Klassifikationszweifeln:

| Frage | Antwort | Achse |
|---|---|---|
| Andere Lastpfade oder Member? | Neue Baugrammatik (`construction_grammar`) | 1 |
| Andere Zonanordnung oder Raumhierarchie? | Neuer Archetyp oder `TopologyModifier` | 2 |
| Andere Nutzung bei gleicher Topologie? | `FunctionPolicy`-Variante | 3 |
| Anderer Dachtyp, Geschosszahl, Orientierung? | `RoofPolicy` / `VerticalPolicy` | 4 |
| Andere Region, Epoche, Wohlstand? | `StylePolicy`-Variante | 5 |

### 9.3 Betroffene Dokumente

Die Einführung von Achse 3 als first-class `FunctionPolicy` erfordert
Anpassungen in folgenden Dokumenten:

| Dokument | Anpassungsbedarf |
|---|---|
| `ARCH_POLICIES.md` | `FunctionPolicy` als Secondary Axis in §3 einfügen; §5 aktualisieren |
| `SYS_CONCEPTS.md` | Policy-Stack in §2 um `FunctionPolicy` erweitern |
| `ARCH_TAXONOMY.md` | Archetyp-Beschreibungen: implizite Nutzungsannahmen dokumentieren oder entfernen |
| `SYS_CONTRACT.md` | `HouseRequest`-Schema: `FunctionPolicy` als Pflichtfeld ergänzen |

---

## 10. Primärliteratur

Empfohlen, noch nicht vollständig ausgewertet:

- **N. W. Alcock**: *Cruck Construction: An Introduction and Catalog.*
  CBA, 1981. → Pflichtlektüre für `CruckFrameProducer`.
- **E. Mercer**: *English Vernacular Houses.* RCHME, 1975.
- **R. W. Brunskill**: *Illustrated Handbook of Vernacular Architecture.*
  Faber, 1978.
- **C. A. Hewett**: *English Historic Carpentry.* Phillimore, 1980.
- **Heinrich Stiewe**: *Fachwerkhäuser in Deutschland.* Darmstadt, 2007.
- **Manfred Gerner**: *Fachwerk, Entwicklung, Gefüge, Instandsetzung.*
  DVA, 2007.
- **Hans Koepf / Günther Binding**: *Bildwörterbuch der Architektur.*
  Kröner, 2005. → Terminologiereferenz.
- **R. T. Mason**: *Framed Buildings of the Weald.* Coach Publishing, 1969.
- **W. H. Zimmermann**: Pfosten, Ständer und Schwelle und der Übergang
  vom Pfosten- zum Ständerbau. *Probleme der Küstenforschung* 25, 1998.
  → Primärquelle für §1.3.

---

## 11. Quellen

[^wiki-fachwerk]: Fachwerkhaus. Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Fachwerkhaus

[^rdklabor]: Fachwerk, Fachwerkbau. Reallexikon zur Deutschen
  Kunstgeschichte (RDK Labor), März 2026.
  https://www.rdklabor.de/wiki/Fachwerk,_Fachwerkbau

[^wiki-skelettbau]: Skelettbau. Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Skelettbau

[^wiki-massivbau]: Massivbau. Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Massivbau

[^lernhelfer-skelett]: Skelettbau (Gliederbau). Duden Lernhelfer,
  März 2026.
  https://www.lernhelfer.de/schuelerlexikon/kunst/artikel/konstruktionsprinzipien-skelettbau-gliederbau

[^wiki-pfostenhaus]: Pfostenhaus. Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Pfostenhaus

[^wiki-ständerbauweise]: Ständerbauweise. Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Ständerbauweise

[^regionalgeschichte]: Fachwerk. Regionalgeschichte.net, März 2026.
  https://www.regionalgeschichte.net/bibliothek/glossar/begriffe/eintrag/fachwerk.html

[^de-academic]: Fachwerkhaus. De-Academic, März 2026.
  https://de-academic.com/dic.nsf/dewiki/425843

[^hessenpark]: Freilichtmuseum Hessenpark / Kompetenzzentrum Fachwerk:
  Historische Konstruktionsweisen, März 2026.
  https://kompetenzzentrum-fachwerk.de/themenschwerpunkte/historische-konstruktionsweisen/

[^stockwerkbau]: Rähmbauweise. Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Rähmbauweise

[^raehm]: Rähm. Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Rähm

[^wiki-fachwerk-haus]: Fachwerkhaus (Industrialisierung, Umgebindehaus).
  Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Fachwerkhaus

[^loebbecke]: Frank Löbbecke: Hochmittelalterliche Holz-Stein-Bauten in
  Südwestdeutschland. Archaia Brno, PDF.
  https://www.archaiabrno.org/media/doc/02_fuma_ii_loebbecke_de.pdf

[^cruck-northhouse]: North House Folk School: Cruck Framing, 2020.
  https://northhouse.org/course-session/cruck-framing-8-5-2020

[^timber-framers-guild]: Timber Framers Guild: Review of N. W. Alcock,
  *Cruck Construction: An Introduction and Catalog*, CBA 1981.
  https://www.tfguild.org/downloads/TF-136-book-review.pdf

[^bard-glossary]: BARD Illustrated Glossary (Tree-Ring Services, 2024).
  http://www.buildingarchaeology.com/wp-content/uploads/2024/03/BARD-Illustrated-Glossary.pdf

[^wiki-timber-framing]: Timber framing. Wikipedia (English), März 2026.
  https://en.wikipedia.org/wiki/Timber_framing

[^vag-aisled]: N. W. Alcock / VAG: A Database of Aisled Buildings in
  England and Wales. *Vernacular Architecture*, 2024.
  https://www.tandfonline.com/doi/full/10.1080/03055477.2024.2321373

[^hall-house-wiki]: Hall house. Wikipedia (English), März 2026.
  https://en.wikipedia.org/wiki/Hall_house

[^vag-wealden]: VAG Wealden Houses Database. Archaeology Data Service,
  August 2025.
  https://archaeologydataservice.ac.uk/archives/view/vag_wealden/

[^oxford-wealden]: Oxford Reference: *A Dictionary of Architecture and
  Landscape Architecture* — Wealden house. OUP, 2023.
  https://www.oxfordreference.com/display/10.1093/oi/authority.20110803121434465

[^wiki-wealden]: Wealden hall house. Wikipedia (English), März 2026.
  https://en.wikipedia.org/wiki/Wealden_hall_house

[^pufr-alsace]: La construction en pan de bois. Presses universitaires
  François-Rabelais, 2018.
  https://books.openedition.org/pufr/7902

[^wiki-colombages]: Maison à colombages. Wikipedia (français), März 2026.
  https://fr.wikipedia.org/wiki/Maison_à_colombages

[^bw-db]: Denkmalpflege Baden-Württemberg: Bauforschung-Restaurierung,
  Datenbank, 2004. Form, Funktion, Konstruktion als Pflichtfelder.
  https://www.denkmalpflege-bw.de/denkmale/datenbanken/bauforschung-restaurierung

[^wiki-bautypologie]: Bautypologie. Wikipedia (deutsch), März 2026.
  https://de.wikipedia.org/wiki/Bautypologie

[^landau-grundriss]: Georg Landau (1860), zitiert nach: Bäuerliches Wohnen
  im 19. Jahrhundert in Oberdeutschland. Hausarbeiten.de.
  https://www.hausarbeiten.de/document/3419

[^maschmeyer-nutzung]: Dietrich Maschmeyer (IGB): Gefügeformen und
  Nutzungsstrukturen. Tagungsbericht Hausforschung, Wolfenbüttel 2003.
  http://www.hausforscher.de/2003/03/2003-grenzen-in-der-hausforschung.html

[^brunskill-function]: R. W. Brunskill: *Illustrated Handbook of Vernacular
  Architecture.* Faber, 1971/2000. Funktion als dominanter Faktor,
  zitiert bei: Vernacular Architecture — Wikipedia (English).
  https://en.wikipedia.org/wiki/Vernacular_architecture

[^irb-merkmale]: Fraunhofer IRB: Schlagwortliste Hausforschung-Publikationen.
  Unterscheidungsmerkmale: Haustyp, Bauweise, Dachform, Giebelwand,
  Grundriss, Raumabfolge, Erscheinungsbild, Dachkonstruktion.
  https://www.irb.fraunhofer.de/bauforschung/baufolit.jsp?s=Hausforschung

[^igbauernhaus-methoden]: IGB Interessengemeinschaft Bauernhaus:
  Arbeitstechniken der Hausforschung.
  https://www.igbauernhaus.de/de/2-unsere-themen/bautechnik/Arbeitstechniken-der-Hausforschung/

[^grossmann-voelkisch]: G. Ulrich Großmann: Völkisch und national —
  Der „Beitrag" der Hausforschung. In: Puschner/Großmann (Hg.),
  Darmstadt 2009. Heidelberg Archiv.
  https://archiv.ub.uni-heidelberg.de/artdok/2688/1/Grossmann_VoelkischundNational_2009.pdf

---

*Status: Freigegeben als REFERENCE-Dokument. Version 2.1.*
*Provisional-Einträge (`prov.`) sind noch nicht Teil von `ARCH_TAXONOMY.md`.*

*© 2026 Alexander Bernardi — CC-BY-SA 4.0*
