# Achse 3 — Gesellschaft und Haushalt
## Soziale Struktur, Statusordnung und der mittelalterliche Haushalt als Baueinheit

```
Dokument-Typ:  Research Foundation
Achse:         3 von 7
Scope:         BVILLAGE — alle Domains, alle Haustypen
Status:        v1.0
Referenziert von:
  MEDIEVAL_WORLD_OVERVIEW.md
  ARCH_POLICIES.md (StylePolicy: wealth; InteriorPlanner)
  MEDIEVAL_04_ECONOMY_TRADE.md (Kaufkraft, Kapital)
  MEDIEVAL_06_BUILDING_AS_ACT.md (Repräsentation)
Evidenzgrade:
  [HART]   Direkt messbar, datierter Bestand, publizierte Messdaten
  [MITTEL] Wissenschaftlicher Konsens, erschlossen, nicht direkt messbar
  [SCHWACH] Analogieschluss, experimentelle Archäologie, Fachtradition
```

---

## Vorbemerkung

Gesellschaft und Haushalt sind die menschliche Seite des Bauens.
Achse 3 beantwortet die Frage: Für wen wird gebaut — und was braucht
dieser Mensch?

Das ist der direkte Fundus für den `wealth`-Parameter und den
`InteriorPlanner`. Ein Gebäude, das für einen Patrizier gebaut wird,
unterscheidet sich von einem Handwerkerhaus nicht willkürlich — es
folgt einer sozialen Logik, die aus Statusordnung, Haushaltsgröße
und Nutzungsanforderungen entsteht.

---

## 1. Die mittelalterliche Sozialstruktur

### 1.1 Das Drei-Stände-Modell und seine Unzulänglichkeit

Das klassische mittelalterliche Drei-Stände-Schema (Klerus, Adel,
Bauern/Dritter Stand) ist ein Denkmodell mittelalterlicher Theologen,
keine Beschreibung sozialer Realität. Die tatsächliche Sozialstruktur
ist wesentlich differenzierter — und für das Bauen ist diese
Differenzierung entscheidend.
[MITTEL — Duby 1978; Le Goff 2004]

### 1.2 Soziale Schichten mit Baurelevanz

**Hochadel / Reichsfürsten**
Könige, Herzöge, Bischöfe in weltlicher Funktion. Bauen auf höchstem
Niveau, aber primär Burgen, Paläste, Kathedralen — außerhalb des
BVILLAGE-Primärscopes.

**Niederadel / Ritter**
Ritter und niederer Adel. Auf dem Land: Turmhügel, befestigte
Häuser, kleine Güter. Ökonomisch oft schlechter gestellt als reiche
städtische Kaufleute. Das Ritterhaus ist oft kleiner und schlechter
gebaut als ein Patrizierstadthaus.
[MITTEL — Schulze 1985; Boockmann 1987]

**Stadtpatrizier / Fernhändler**
Die wirtschaftliche Elite der Städte. Kaufleute mit überregionalen
Handelskontakten. Oft reicher als niederer Adel. Bauen prachtvoll:
mehrgeschossige Patrizierhäuser mit Repräsentationsräumen, Gewölbe-
keller, Handelsräume im Erdgeschoss.
Typische Merkmale: 4–8 Stockwerke, Vorkragungen, reiches Ornament,
Eichenholz durchgehend, gemauerter Keller.
[MITTEL — Boockmann 1987; Schulz 2010]

**Zunftbürger / Handwerksmeister**
Meister in städtischen Zünften. Mittlere Wohlstandsklasse.
Eigenes Haus, häufig mit Werkstatt oder Ladenlokal im Erdgeschoss.
2–3 Stockwerke, solide Konstruktion, bescheidene Ornamentik.
[MITTEL — Wesoly 1985; Schulz 2010]

**Kleinstädtisches Bürgertum / Ackerbürger**
Kleinstädtische Haushalte mit gemischter Erwerbsbasis: Handwerk
und Landwirtschaft. Das Ackerbürgerhaus vereint Wohnbereich und
kleinere landwirtschaftliche Nutzfläche.
[MITTEL — Bedal 1993; Stiewe 2007]

**Bäuerliche Bevölkerung**
Die Mehrheit der mittelalterlichen Bevölkerung. Baut nach
agrarischer Funktion: Hallenhaus, Ernhaus, einfache Bauernhäuser.
Kein Luxus, lange Kontinuität der Formen, Material aus dem
Nahbereich.
[MITTEL — Bedal 1993; Stiewe 2007]

**Unterschichten / Tagelöhner**
Mieter, nicht Eigentümer. Wohnen in Hintergebäuden, Söllern,
gemieteten Kammern. Bauen für sich selbst nicht.
[SCHWACH — schlecht dokumentiert]

### 1.3 Die Mehrdimensionalität von Status

Status im Mittelalter ist nicht eindimensional. Geburt, Reichtum,
Zunftzugehörigkeit, politische Funktion, Religiosität und lokale
Reputation sind separate Dimensionen, die nicht immer korrelieren.

Ein reicher Fernhändler ohne Adelstitel kann in einer Reichsstadt
mehr politischen Einfluss haben als ein verarmter Ritter auf dem Land.
Ein Zunftmeister kann wohlhabender sein als ein Landedelmann.

**BVILLAGE-Implikation**: Der `wealth`-Parameter ist eine Vereinfachung.
Er sollte als Index verstanden werden, der mehrere Dimensionen
synthetisiert: materiellen Besitz, sozialen Status und institutionelle
Einbindung. Für Bau-Constraints ist die Kombination entscheidend,
nicht ein einzelner Wert.

---

## 2. Der mittelalterliche Haushalt

### 2.1 Haushaltsgröße

Der mittelalterliche Haushalt ist größer und heterogener als der
moderne. Er umfasst nicht nur die Kernfamilie, sondern oft:
- Eltern und Kinder (Kernfamilie: 4–6 Personen)
- Gesellen und Lehrlinge (Handwerksbetrieb)
- Dienstboten und Mägde (je nach Wohlstand 1–10 Personen)
- Kostgänger (gemietete Untermieter)
- Ältere Elternteile oder Verwandte

Typische Haushaltsgrößen:
- Armes städtisches Haushalt: 3–5 Personen
- Handwerksmeister-Haushalt: 6–12 Personen
- Patrizierfamilie: 10–20 Personen (incl. Gesinde)
- Großer Handelshof: 20–30+ Personen

[MITTEL — Herlihy/Klapisch-Zuber 1985 für Florenz; übertragbar auf
deutschsprachigen Raum mit Vorbehalt; Schulz 2010]

**BVILLAGE-Implikation**: `InteriorPlanner`-Raumanzahl und Raumgrößen
sind Funktionen der Haushaltsgröße, nicht des Grundrisssquadratmeters.
Ein Patrizierfamilien-Haushalt von 15 Personen braucht mehr separate
Schlafräume als eine 5-Personen-Familie — aber nicht fünfmal mehr,
weil gemeinschaftliches Schlafen der Normalfall ist.

### 2.2 Raumnutzung

Mittelalterliche Räume haben multiple Funktionen. Privatsphäre im
modernen Sinne existiert nicht für die meisten Schichten.

**Erdgeschoss**: Fast immer gewerblich oder landwirtschaftlich.
Laden, Werkstatt, Stall, Lager, Tenne. Kein Wohnraum für die Familie
(außer in ärmsten Verhältnissen).

**Erstes Obergeschoss (Piano Nobile)**: Die primäre Wohnebene der
Eigentümer. Großer Saal (Flett beim Hallenhaus, Diele beim Stadthaus),
evtl. separate Kammer für die Eltern.

**Zweites Obergeschoss aufwärts**: Schlafkammern, Vorratslagerung,
Gesindeschlafraum (oft ungeteilt, gemeinschaftlich). Bei reichen
Häusern: separate Gastzimmer, Schreibstube.

**Dachgeschoss**: Vorratslagern, Dörren, Gesinde.

[MITTEL — Bedal 1993; Binding 1993; Stiewe 2007]

### 2.3 Typische Nutzungsaufteilungen nach Schicht

**Bäuerlicher Haushalt (ländlich)**
```
Erdgeschoss: Tenne / Diele (zentral, offen bis First)
             Stallboxen links und rechts
             Flett (Küche/Wohnraum) am Ende der Diele
Dachraum:    Heueinlagerung über der gesamten Fläche
```
Raumanzahl: 2–4 Nutzungsbereiche, nicht Räume im modernen Sinne.
[HART für Hallenhaustyp — aus erhaltenen Bauten; Stiewe 2007]

**Handwerksmeister-Stadthaus**
```
Erdgeschoss:      Werkstatt oder Laden + Lager
1. Obergeschoss:  Wohnstube (beheizt, Mittelpunkt des Familienlebens)
                  Schlafkammer (Eltern, ev. Kleinkinder)
2. Obergeschoss:  Gesellen-/Lehrlingskammern, Vorrat
Keller:           Lebensmittellagerung
```
Raumanzahl: 5–8 Räume gesamt. Nutzfläche: 40–80 m².
[MITTEL — aus Hausforschung; Bedal 1993]

**Patrizierstadthaus**
```
Keller:            Gewölbter Weinkeller, Warenlager
Erdgeschoss:       Kontor, Handelsraum, Eingangsgewölbe
1. Obergeschoss:   Repräsentationssaal (Sommer- oder Prunkstube)
                   Herrenstube (beheizt, Alltagswohnen)
2. Obergeschoss:   Elternschlafkammer, Gästekammer
3.+ Obergeschoss:  Vorratsräume, Gesindekammern
Dachgeschoss:      Großlager (Getreide, Textilien)
```
Raumanzahl: 12–20 Räume. Nutzfläche: 150–400 m².
[MITTEL — aus erhaltenen Patrizierhäusern; Boockmann 1987; Stiewe 2007]

---

## 3. Raumgrößen: Historische Maßstäbe

### 3.1 Typische Raumgrößen

| Raum | Typische Größe | Schicht | Evidenz |
|---|---|---|---|
| Einfache Schlafkammer | 8–15 m² | alle | MITTEL |
| Wohnstube (Handwerker) | 15–25 m² | Handwerker | MITTEL |
| Repräsentationssaal | 30–60 m² | Patrizier | MITTEL |
| Werkstatt / Laden EG | 20–50 m² | Handwerker/Händler | MITTEL |
| Tenne / Diele (Hallenhaus) | 60–150 m² | ländlich | HART |
| Gesamtnutzfläche Kleinbürger | 30–60 m² | Kleinbürger | MITTEL |
| Gesamtnutzfläche Handwerker | 60–120 m² | Handwerker | MITTEL |
| Gesamtnutzfläche Patrizier | 150–400 m² | Patrizier | MITTEL |

[Evidenz: Herlihy/Klapisch-Zuber 1985; Binding 1993; Bedal 1993;
Stiewe 2007; aus erhaltenen Gebäuden]

### 3.2 Parzellen und Gebäudegrundrisse

Städtische Parzellen sind durch mittelalterliches Stadtrecht geregelt
und historisch stabil. Ihre Maße prägen den Grundriss direkt.

Typische Parzellbreiten in deutschen Mittelstädten (14.–16. Jh.):
- Sehr eng (Kleinstadthandwerker): 4–6 m
- Normal (Handwerker/Händler): 6–10 m
- Breit (Patrizier): 10–15 m, manchmal mehrere Parzellen zusammen

Parzelltiefe: 15–30 m (städtisch), bis 50 m (Ackerbürger mit
Scheune im hinteren Bereich).
[MITTEL — aus Stadtgrundrissforschung; Stoob 1985; Boockmann 1987]

**BVILLAGE-Implikation**: `lot.width` ist kein freier Parameter.
Er ist statistisch an `settlement_type` und `social_class` gebunden.
Ein Patrizier in einer Reichsstadt hat im Schnitt eine breitere
Parzelle als ein Handwerker — nicht immer, aber als Wahrscheinlichkeit.

---

## 4. Der wealth-Parameter: Operationalisierung

### 4.1 Was wealth kodiert

`wealth` in BVILLAGE ist ein synthetischer Index. Er fasst zusammen:
- Verfügbares Kapital für den Bau
- Sozialer Status (Repräsentationsanforderungen)
- Haushaltsgröße (Raumanforderungen)
- Institutionelle Einbindung (Zunft, Gilde, Ratsmitglied)

Diese vier Dimensionen korrelieren in der Regel, divergieren aber
in charakteristischen Fällen:

| Profil | Kapital | Status | Haushalt | Institutionen | Bautendenz |
|---|---|---|---|---|---|
| Armer Ritter | gering | hoch | mittel | hoch (Adel) | bescheiden, aber standesgemäß |
| Reicher Händler | hoch | mittel | groß | mittel (Zunft) | prachtvoll, funktional |
| Klosterpropst | mittel | sehr hoch | groß | sehr hoch | repräsentativ, asketisch |
| Ackerbürger | gering | gering | mittel | gering | pragmatisch, gemischt |

[MITTEL — Synthese aus Boockmann 1987; Schulz 2010; Duby 1978]

### 4.2 Baumerkmale nach wealth-Klassen

Die folgende Tabelle verbindet `wealth`-Klassen mit konkreten
Bauparametern. Die Grenzen sind Wahrscheinlichkeiten, keine
deterministische Zuordnung.

| Klasse | Bezeichnung | Geschosse | Ornament | Infill | Keller | Besondere Merkmale |
|---|---|---|---|---|---|---|
| 0 | Subsistenz | 1 | 0 | Lehm/Flechtwerk | nein | Pfostenbau möglich; Erdgeschoss-Wohnen |
| 1 | Kleinstbürger | 1–2 | 0 | Lehm | nein | Gemischte Nutzung, enge Parzelle |
| 2 | Handwerker | 2 | 1 | Lehm/Ziegel | ggf. einfach | Werkstatt EG, Wohnstube OG |
| 3 | Wohlhabender Handwerker | 2–3 | 1–2 | Ziegel | einfach | Repräsentationsstube |
| 4 | Großbürger / Händler | 3–5 | 2–3 | Ziegel | gewölbt | Kontor, Handelslager |
| 5 | Patrizier | 5–8 | 3–4 | Ziegel | gewölbt, mehrjochig | Saal, Gastzimmer, Prunkfassade |

[MITTEL — Synthese aus Stiewe 2007; Großmann 2009; Boockmann 1987;
Binding 1993]

---

## 5. Haustypen und ihre soziale Trägerschicht

Nicht jeder Haustyp ist für jede Sozialschicht gebaut. Die
Zuordnung ist statistisch stabil, aber nicht absolut.

| Haustyp | Primäre Schicht | Sekundär | Soziale Logik |
|---|---|---|---|
| Niederdeutsches Hallenhaus | Bäuerliche Familie (groß) | — | Agrarfunktion dominiert |
| Gulfhaus | Wohlhabende Bauern | — | Agrarkapital, Nordseewirtschaft |
| Ernhaus | Mittelbäuerliche Familie | Kleinstädtisch | Gemischte Funktion |
| Giebelständiges Stadthaus | Handwerker, Händler | Kleinstbürger | Stadtparzelle, Gewerbenutzung |
| Ackerbürgerhaus | Kleinstädtisch gemischt | — | Übergang Stadt/Land |
| Patrizierhaus | Fernhändler, Ratsherren | — | Repräsentation + Handel |

[MITTEL — Großmann 2009; Stiewe 2007; Bedal 1993]

---

## 6. Geschlecht und Haushalt

Frauen sind als Bauherrschaft und Haushaltsmitglieder in der
Forschung lange unterschätzt worden. Für BVILLAGE relevant:

**Witwen als Bauherrschaft**: Verwitwete Frauen hatten in
Reichsstädten häufig volle Eigentumsrechte. Zahlreiche dokumentierte
Fälle von Frauen als alleinige Bauauftraggeber.
[MITTEL — Wiesner-Hanks 2008]

**Frauenarbeit im Haushalt**: Die räumliche Organisation des Hauses
folgt der Arbeitsteilung im Haushalt. Küche, Vorratraum und
Waschbereich haben spezifische Positionierungen, die von der
weiblichen Nutzung abhängen. [MITTEL — Bedal 1993]

**BVILLAGE-Implikation**: Der `InteriorPlanner` sollte Haushaltsfunktion
als primären Planungsparameter verwenden — nicht Anzahl von Räumen.
Welche Tätigkeiten finden statt? Dann folgen die Räume.

---

## 7. Offene Forschungsfragen

**Frage 1 — Quantitative Haushaltsgrößen für deutschsprachigen Raum**
Herlihy/Klapisch-Zuber (1985) liefern exzellente Daten für Florenz 1427
(Steuerregister). Vergleichbare systematische Quellen für das HRR
existieren, sind aber weniger ausgewertet. Für präzise
`InteriorPlanner`-Parameter wären regionale Haushaltsstudien nötig.

**Frage 2 — Parzellmaße für spezifische Städte**
Stadtgrundrissforschung hat für viele Städte historische Parzellenmaße
rekonstruiert. Eine systematische Zusammenstellung für BVILLAGE-relevante
Städte fehlt noch.

**Frage 3 — Raumnutzungsarchäologie**
Welche Tätigkeiten fanden konkret in welchen Räumen statt?
Archäobotanische und archäozoologische Befunde beginnen das zu beantworten,
aber die Forschungslage ist für Profanbau dünn.

---

## 8. Quellen und wissenschaftliche Grundlage

### 8.1 Zitierte Werke

**Bedal, Konrad:** Historische Hausforschung. Eine Einführung in
Arbeitsweise, Begriffe und Literatur. Münster: Coppenrath, 1993.
*Raumnutzung, Haushaltsgröße, ländliche Baukultur.*

**Binding, Günther:** Baubetrieb im Mittelalter. Darmstadt: WBG, 1993.
*Raumorganisation, Nutzungsaufteilungen.*

**Boockmann, Hartmut:** Die Stadt im späten Mittelalter.
München: Beck, 1987.
*Stadtgesellschaft, Patriziertum, Zunftbürger, Sozialstruktur.*

**Duby, Georges:** Les trois ordres ou l'imaginaire du féodalisme.
Paris: Gallimard, 1978. Deutsche Ausgabe: Die drei Ordnungen.
Das Weltbild des Feudalismus. Frankfurt: Suhrkamp, 1981.
*Das Drei-Stände-Modell und seine Grenzen. Sozialstruktur des
mittelalterlichen Europa.*
[MITTEL]

**Herlihy, David; Klapisch-Zuber, Christiane:** Tuscans and their
Families. A Study of the Florentine Catasto of 1427.
New Haven: Yale University Press, 1985.
*Quantitative Sozialgeschichte auf Basis eines Steuerregisters.
Haushaltsgrößen, Besitzverhältnisse. Für Florenz — als methodisches
Vorbild für deutschsprachige Forschung.*
[HART für Florenz; MITTEL als Analogie]

**Le Goff, Jacques:** Die Geburt Europas im Mittelalter.
München: Beck, 2004.
*Gesellschaftsstruktur, Ständeordnung, sozialer Wandel.*

**Schulz, Knut:** Handwerk, Zünfte und Gewerbe.
Darmstadt: WBG, 2010. ISBN 978-3-534-15827-1.
*Soziale Lage der Handwerker, Zunfthierarchie, Meisterrecht.*
[MITTEL]

**Schulze, Hans K.:** Grundstrukturen der Verfassung im Mittelalter.
4 Bde. Stuttgart: Kohlhammer, 1985–2011.
*Adelsrecht, Stadtrecht, Standesordnungen.*

**Stiewe, Heinrich:** Fachwerkhäuser in Deutschland.
Darmstadt: WBG, 2007. ISBN 978-3-534-18714-1.
*Haustypen und ihre soziale Trägerschicht. Nutzungsaufteilungen.*
[MITTEL]

**Stoob, Heinz (Hrsg.):** Die Stadt. Gestalt und Wandel bis zum
industriellen Zeitalter. Köln/Wien: Böhlau, 1985. 2. Aufl.
*Parzellmaße, Stadtgrundrisse, Bevölkerungsdaten.*

**Wesoly, Kurt:** Lehrlinge und Handwerksgesellen am Mittelrhein.
Frankfurt: Waldemar Kramer, 1985.
*Soziale Lage von Gesellen und Lehrlingen. Haushaltszugehörigkeit
im Handwerksbetrieb.*
[MITTEL]

**Wiesner-Hanks, Merry E.:** Women and Gender in Early Modern Europe.
Cambridge: Cambridge University Press, 2008. 3. Aufl.
*Frauen als Eigentumssubjekte, Bauherrschaft, Haushaltsfunktionen.*
[MITTEL]

---

### 8.2 Weiterführende Literatur

**Dyer, Christopher:** Standards of Living in the Later Middle Ages.
Social Change in England c. 1200–1520.
Cambridge: Cambridge University Press, 1989.
*Lebensstandard, materielle Kultur, Haushaltsausstattung nach
Sozialschicht. Für England, aber methodisch vorbildhaft.*

**Saalman, Howard:** Medieval Cities.
New York: Braziller, 1968.
*Städtischer Raum, Parzellenstruktur, soziale Organisation des
Stadtgrundriss. Klassisch, gut zugänglich.*

---

*BVILLAGE Research Foundation — Achse 3 — v1.0*
