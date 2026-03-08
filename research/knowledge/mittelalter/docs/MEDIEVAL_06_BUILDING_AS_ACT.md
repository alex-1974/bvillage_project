# Achse 6 — Bauen als gesellschaftlicher Akt
## Das mittelalterliche Gebäude im Systemkontext

```
Dokument-Typ:  Research Foundation
Achse:         6 von 7
Scope:         BVILLAGE — alle Domains, alle Haustypen
               Zeitraum: 500–1750 (Kern: 950–1500)
               Raum: Westeuropa und Byzanz
Status:        v2.1
Referenziert von:
  MEDIEVAL_WORLD_OVERVIEW.md
  ARCH_POLICIES.md (StylePolicy, CulturePolicy, ConstraintsPolicy)
Referenziert:
  MEDIEVAL_07_EPOCHS_AND_BREAKS.md
  MEDIEVAL_05_KNOWLEDGE_CRAFT.md
```

---

## Inhaltsverzeichnis

- [Vorbemerkung: Die Synthese-Achse](#vorbemerkung-die-synthese-achse)
- [1. Das Gebäude als mehrdimensionales Objekt](#1-das-gebäude-als-mehrdimensionales-objekt)
- [2. Der Bauprozess als sozialer Akt](#2-der-bauprozess-als-sozialer-akt)
- [3. Warum Häuser so aussehen wie sie aussehen](#3-warum-häuser-so-aussehen-wie-sie-aussehen)
- [4. Regionale Repräsentationslogiken: Gesamteuropa](#4-regionale-repräsentationslogiken-gesamteuropa)
  - [4.1 HRR: Außenrepräsentation und vertikaler Wettbewerb](#41-hrr-außenrepräsentation-und-vertikaler-wettbewerb)
  - [4.2 England: Great Hall als horizontaler Statusraum](#42-england-great-hall-als-horizontaler-statusraum)
  - [4.3 Al-Andalus: Innenrepräsentation und Innenhoflogik](#43-al-andalus-innenrepräsentation-und-innenhoflogik)
  - [4.4 Skandinavien: Qualitätsmaterial als Statusanzeige](#44-skandinavien-qualitätsmaterial-als-statusanzeige)
  - [4.5 Byzanz: Kaiserliche Monumentalität vs. Provinz](#45-byzanz-kaiserliche-monumentalität-vs-provinz)
- [5. Gebäudetypen als soziale Kategorien](#5-gebäudetypen-als-soziale-kategorien)
- [6. Was sich nicht ändern darf — und was sich muss](#6-was-sich-nicht-ändern-darf--und-was-sich-muss)
- [7. BVILLAGE-Syntheseregeln](#7-bvillage-syntheseregeln)
- [8. Offene Fragen für BVILLAGE](#8-offene-fragen-für-bvillage)
- [9. Quellen](#9-quellen)

---

## Vorbemerkung: Die Synthese-Achse

Achse 6 ist die letzte der sieben — und die schwierigste zu formalisieren.
Sie beschreibt nicht eine isolierbare Dimension des mittelalterlichen Systems.
Sie beschreibt, wie alle anderen Dimensionen in einem konkreten Gebäude
zusammenlaufen.

Ein Haus ist das Dokument, in dem Klima, Recht, Kapital, Wissen und soziale
Ambition einen Gleichgewichtspunkt finden. Wer dieses Dokument lesen kann,
liest alle anderen Achsen gleichzeitig.

Für BVILLAGE ist das die operative Begründung, warum Achse 6 zuletzt kommt:
Sie kann nur formuliert werden, wenn die anderen sechs bekannt sind.
Und sie ist zugleich der Test, ob das System als Ganzes kohärent ist.

**Scope-Erweiterung in v2.0**: Abschnitt 4 erschließt systematisch die
regionalen Repräsentationslogiken außerhalb des HRR. Zentraler Befund:
Statusanzeige durch das Gebäude ist universell — aber die Sprache, in der
der Status codiert ist, variiert fundamental. HRR codiert Status nach außen
durch Höhe, Vorkragung, Ornamentdichte. Al-Andalus codiert Status nach innen
durch Innenhofqualität, Wasseranlage, Ornamentgrammatik. Das sind zwei
entgegengesetzte Gebäudelogiken.

> [!IMPORTANT]
> Die `StylePolicy`-Mapping-Funktion `wealth → morphology` ist
> **regional verschieden** und muss als solche implementiert werden.
> Ein universelles Mapping ist historisch falsch.

---

## 1. Das Gebäude als mehrdimensionales Objekt

Ein mittelalterliches Gebäude ist niemals nur technische Konstruktion.
Es ist gleichzeitig fünf Dinge — und alle fünf sind untrennbar verwoben.

### 1.1 Eigentumsbeweis

Im mittelalterlichen Rechtsverständnis konstituiert das Gebäude Eigentum
am Grund, nicht umgekehrt. Wer ein Haus baut und es nutzt, demonstriert
Besitzrecht. Das ist nicht Metapher — es hat rechtliche Konsequenz.[^schulze1985]

Das erklärt, warum auch arme Haushalte investierten, was sie nicht hatten:
ein Haus, das verfiel, gefährdete den Rechtsanspruch. Unterhalt war keine
ästhetische Entscheidung. Er war Rechtsausübung.

> [!NOTE]
> **BVILLAGE-Implikation**: Gebäudezustand ist kein reiner `wealth`-Parameter.
> Er hat eine rechtliche Dimension, die für Siedlungstyp und Eigentumsstruktur
> relevant ist. Ein verfallenes Haus in einem gut dokumentierten Siedlungskontext
> signalisiert gesellschaftliche Disruption, nicht nur Armut.

### 1.2 Statusanzeige

Das Gebäude kommuniziert. An Nachbarn, Stadtrat, Handelspartner, Reisende.
Die Botschaft ist codiert in: Geschosszahl, Vorkragungstiefe, Holzqualität,
Ornamentreichtum, Infill-Material, Fassadenbehandlung.[^grossmann2009-status]

Großmann (2009) belegt, dass die Vorkragung primär Repräsentationsmerkmal
war, nicht Schutzfunktion. Je tiefer die Auskragung, desto teurer und
aufwändiger — und desto deutlicher die Botschaft.[^grossmann2009-vorkragung]

> [!NOTE]
> **BVILLAGE-Implikation**: Der `wealth`-Parameter steuert nicht nur
> Materialqualität und Querschnittsgröße. Er steuert die Kodierungsintensität
> der Statusbotschaft: Ornamentdichte, Vorkragungstiefe, Geschosszahl,
> Infill-Materialwahl. Diese Variablen sind nicht unabhängig — sie sind
> kohärente Signale desselben sozialen Anspruchs.

### 1.3 Rechtsdokument

Das Gebäude ist Träger von Rechtsverhältnissen, die über den Eigentümer
hinausgehen. Vorkragungsrechte waren stadtrechtlich geregelt — das Recht,
in den öffentlichen Straßenraum auszukragen, war eine stadtrechtliche
Konzession, keine selbstverständliche Baufreiheit.[^stiewe2007-recht]

Grenzen, Nutzungsrechte, Dienstbarkeiten wurden am physischen Gebäude
abgelesen, nicht an Katasterdokumenten.

> [!IMPORTANT]
> **BVILLAGE-Implikation**: Die `ConstraintsPolicy` muss stadtrechtliche
> Regelungen als lokale Hard-Constraints abbilden — insbesondere für
> Vorkragung, Traufhöhe und Parzellenausnutzung. Diese Constraints sind
> nicht physikalisch, sondern juristisch. Sie variieren zwischen Städten
> und über die Zeit. Jeder Constraint-Parameter braucht eine dokumentierte
> Herkunft (physikalisch / rechtlich / sozial / ökonomisch).

### 1.4 Kollektives Werk

Der Abbund erforderte den Zimmermann als Fachmann. Das Aufrichten dagegen
konnte von vielen ungelernten Helfern durchgeführt werden, die zum Richtfest
mit Naturalien entlohnt wurden.[^bedal1993-kollektiv]

Diese Arbeitsteilung verankerte das Gebäude in sozialen Verpflichtungen:
Wer beim Richtfest half, hatte Ansprüche auf Gegenseitigkeit. Das Haus
entstand im sozialen Schuldengeflecht.

> [!NOTE]
> **BVILLAGE-Implikation**: `settlement_type` beeinflusst, wie dieser
> kollektive Aspekt gewichtet ist. Städtische Handwerkergesellschaft
> (Zunft organisiert Arbeit, Geld zahlt Lohn) vs. ländliche Dorfgemeinschaft
> (Gegenseitigkeitspflicht, Naturalentlohnung) — beides erzeugt dasselbe
> Ergebnis, aber aus anderen sozialen Dynamiken.

### 1.5 Wirtschaftliche Anlage

Das Haus ist Kapital. Es kann vermietet, verpfändet, vererbt, verkauft
werden. Städtische Oberstockwerke wurden an Mieter vergeben. Keller an
Händler. Ladenfronten an Gewerbetreibende.[^spufford2002-kapital]

> [!NOTE]
> **BVILLAGE-Implikation**: Der `InteriorPlanner` muss diese Nutzungsvielfalt
> kennen. Erdgeschoss-Kommerz, Mittelgeschoss-Wohnen, Obergeschoss-Lager
> ist kein Sonderfall — es ist der städtische Normalfall für wohlhabende
> Handwerker und Kaufleute.

---

## 2. Der Bauprozess als sozialer Akt

### 2.1 Entscheidung: Wer baut?

Die Entscheidung zu bauen ist keine rein ökonomische. Sie ist eingebettet
in soziale Anlässe: Heirat, Erbschaft, Zunftzulassung, Stadtbürgerrecht.
Wer neu in die Zunft eintritt, braucht ein standesgemäßes Haus.[^boockmann1987-entscheidung]

Das erklärt die demographisch nachweisbaren Bauphasen: Pestwiederaufbau
(1360–1400), Zunftblüte (15. Jh.), Nachkriegswiederaufbau (nach 1648).
Bauen folgt sozialen Opportunitätsfenstern, nicht nur Kapitalverfügbarkeit.

### 2.2 Beauftragung: Wer plant?

Für Profanbauten des Mittelstands gilt: Der Zimmermann plant und baut.
Es gibt keinen Architekten im modernen Sinne. Der Bauherr kommuniziert
Typus, Größe und Ausstattungsgrad. Der Zimmermann übersetzt in Konstruktion.[^binding1993-planung]

Für gehobene Stadtbauten und öffentliche Gebäude: Der Werkmeister als
spezialisierter Planungsverantwortlicher. Für Kirchenbauten: Die Bauhütte.

> [!NOTE]
> **BVILLAGE-Implikation**: `knowledge_infrastructure_tier` aus Achse 5
> bestimmt nicht nur die Konstruktionskompetenz, sondern auch die
> Planungsstruktur. Ein Dorfzimmermann plant anders als ein Stadtmeister —
> nicht nur technisch, sondern prozessual.

### 2.3 Vorfertigung: Der Zimmerplatz

Vollständige Vorfertigung auf dem Zimmerplatz ist durch Abbundzeichen
physisch belegt.[^eissing2023-zimmerplatz]

Der Grundriss wird in Originalgröße auf dem Boden aufgerissen. Jedes
Bauteil wird markiert. Das Gebäude existiert virtuell vollständig, bevor
der erste Ständer auf der Baustelle steht.

Das ist nicht Modernität — das ist die Lösung für das Problem der
Baustellenlogistik ohne Lagerkapazität und mit sozialer Termindisziplin
(Richtfest als angekündigtes Gemeinschaftsereignis).

### 2.4 Aufrichtung: Das Richtfest

Das Richtfest ist mittelalterliche Tradition, historisch belegbar.[^bedal1993-richtfest]

Es ist gleichzeitig: logistisches Ereignis (viele Helfer für kurze Zeit),
soziales Ereignis (Verpflichtungsnetz wird aktiviert), religiöses Ereignis
(Segnung, Richtkranz, Gebete) und Demonstration des sozialen Netzwerks
des Bauherrn.

### 2.5 Einzug und Nutzung

Der Einzug in ein neues Haus hatte rituelle Dimension: Schwellenkult
(die Schwelle als Übergang, Schutzzeichen), erste Feuerung im Herd als
Inbesitznahme.[^schwellenkult]

---

## 3. Warum Häuser so aussehen wie sie aussehen

### 3.1 Die Logik des Mehraufwands

Viele Entscheidungen im mittelalterlichen Hausbau erscheinen technisch
irrational: teurer als nötig, aufwändiger als funktional erforderlich.
Die Erklärung liegt nicht in der Technik, sondern in der sozialen Logik.

Eichenholz wo Tanne reicht: Eiche signalisiert Dauerhaftigkeit und Reichtum.
Geschnitzte Knaggen wo glatte ausreichen: Komplexe Schnitzereien erforderten
erfahrene Meister — der Beweis, dass man sich den Besten leisten konnte.
Mehrfache Vorkragung wo einfache genügte: Jede zusätzliche Auskragung
erfordert komplexere Verbindungen und ist von der Straße aus lesbar.[^grossmann2009-mehraufwand]

### 3.2 Die Logik der regionalen Konformität

Ein Haus, das konstruktiv "falsch" wirkt nach lokalen Normen, signalisiert
Fremdheit — auch wenn es technisch überlegen ist. Zunftordnungen schützten
lokale Standards explizit gegen auswärtige Meister.[^epstein1998-konformitaet]

Das erklärt, warum Innovationen sich langsam ausbreiten: nicht wegen
technischer Trägheit, sondern wegen sozialer Kosten der Abweichung.
Ein Zimmermann, der anders baut als seine Zunftbrüder, riskiert Ruf
und Auftragslage.

> [!IMPORTANT]
> **BVILLAGE-Implikation**: Historische Plausibilität ist soziale Kohärenz,
> nicht nur physikalische Korrektheit. Regionale Konformität ist ein
> Qualitätsmerkmal — nicht Konservativismus. Der `StylePolicy`-Parameter
> `regional_conformity` sollte explizit modelliert werden.

### 3.3 Die Logik der Einschränkungen

Stadtrechtliche Einschränkungen: Was nach oben begrenzt, ermutigt zur
Ausschöpfung des Maximalrahmens: wenn 0,8 m Vorkragung erlaubt sind,
baut der Ehrgeizige 0,8 m — nicht 0,4 m.[^stiewe2007-constraints]

Soziale Einschränkungen: Wer unter dem Zunftmindestniveau baut, verliert
Ansehen. Wer über dem Standesniveau baut, macht sich verdächtig. Der
Spielraum ist nach oben und unten begrenzt.[^wesoly1985]

---

## 4. Regionale Repräsentationslogiken: Gesamteuropa

<a name="representation-logic-table"></a>

### 4.1 HRR: Außenrepräsentation und vertikaler Wettbewerb

Im HRR (besonders in Reichsstädten) codiert das Gebäude Status primär
**nach außen**: zur Straße, zum Nachbarn, zum öffentlichen Raum.

Die Achse des Wettbewerbs ist **vertikal**: Höhe (Geschosszahl) ist
das primäre Statusmedium, weil Höhe aus der Distanz lesbar ist. Auf
einer engen Stadtparzelle ist Vorkragung das zweite Statusmedium —
sie vergrößert die Nutzfläche und demonstriert Handwerkskompetenz.

Die **Fassade** ist die Statusfläche: Ornamentik konzentriert sich auf
die straßenzugewandte Seite. Rückseiten sind unbehandelt.

Patrizierhäuser in Reichsstädten erreichten 7–8 Stockwerke — nicht weil
das funktional nötig wäre, sondern weil Höhe lesbar war.[^hrr-hoehe]

### 4.2 England: Great Hall als horizontaler Statusraum

In England codiert das Gebäude Status primär **nach innen**: durch die
Qualität des empfangenen Raums, nicht durch die Außenfassade.

Die **Great Hall** ist das Statusmedium: ihre Größe, ihre Firsthöhe,
ihre Dekoration (hammer beam roofs als konstruktives Luxussignal) zeigen
den Rang des Hausherrn — aber für Gäste, nicht für Straßenpassanten.[^brunskill2000-hall]

Der Wettbewerb ist **horizontal**: nicht Höhe, sondern Breite und Tiefe
der Hall. In England ist ein einzelgeschossiges Gebäude keine Armutsgeste —
es kann ein großer Landsitz sein.

Das erklärt, warum englische Fachwerkarchitektur breiter und geduckter
wirkt als HRR-Architektur: Das ist keine technische Rückständigkeit,
sondern eine andere Statuslogik.[^dyer1989-hall]

> [!IMPORTANT]
> **BVILLAGE-Implikation**: `wealth` kann in England nicht direkt auf
> `floor_count` gemappt werden. Die Mapping-Funktion `wealth → floor_count`
> ist regional verschieden. Für England: `wealth → hall_size + hall_quality`.

### 4.3 Al-Andalus: Innenrepräsentation und Innenhoflogik

Al-Andalus codiert Status **nach innen** — aber anders als England.
Während England die Halle als Repräsentationsraum für Gäste öffnet,
verbirgt das islamische Stadthaus seinen Reichtum hinter einer
geschlossenen Straßenfassade. Status ist für Gäste sichtbar, die
eingeladen wurden — nicht für Passanten.

Die **Innenhofqualität** ist das primäre Statusmedium:
- Brunnen oder Wasserbecken: Wasser ist kostbar in trockenem Klima
- Zahl und Qualität der umlaufenden Arkaden
- Qualität des Gipsstucks (Muqarnas, geometrische Muster)
- Qualität der geometrischen Bodenkeramik[^alhambra-bestand]

Eine geschlossene, schlichte Straßenfassade bedeutet im HRR Armut.
In Al-Andalus kann dieselbe Fassade einen reichen Kaufmann verbergen.

> [!IMPORTANT]
> **BVILLAGE-Implikation**: Wenn BVILLAGE auf Al-Andalus erweitert wird,
> muss die `StylePolicy` für islamische Häuser den `wealth`-Parameter
> auf Innenhofparameter mappen, nicht auf Fassadenparameter. Das ist eine
> **fundamentale Richtungsumkehr** der Kodierungslogik — eine neue
> `RepresentationPolicy`-Komponente ist erforderlich:
>
> ```
> representation_direction: outward   # HRR
> representation_direction: inward    # Al-Andalus
> representation_direction: interior_horizontal  # England (Hall)
> representation_direction: material_quality     # Skandinavien
> ```

### 4.4 Skandinavien: Qualitätsmaterial als Statusanzeige

In Skandinavien — wo Holz abundant ist — codiert Status nicht durch
Materialknappheit, sondern durch **handwerkliche Qualität** des reichlich
vorhandenen Materials.

Statusanzeiger im skandinavischen Kontext:
- Holzqualität (kern-dichtes, astfreies Holz aus alten Bäumen)
- Komplexität der Verbindungen (direkter Qualifikationsnachweis ohne
  Zunftstruktur)
- Größe und Anzahl der Ensemblegebäude (*huseby* aus mehreren Bauten)[^anker1997-status]

Das Stabkirchen-Prinzip: Die Stabkirchen sind nicht aus individuellem
Repräsentationswillen entstanden. Sie entstehen aus gemeinschaftlichem
Investitionswillen der *Bonde*-Gemeinschaft — das Gebäude als kollektiver
Statusakt der freien Gemeinde, nicht des individuellen Reichen.[^sawyer1993-bonde]

> [!NOTE]
> **BVILLAGE-Implikation**: `wealth` in Skandinavien mappt stärker auf
> `joint_complexity_level` und `ensemble_size` als auf `floor_count`
> oder `ornament_density`.

### 4.5 Byzanz: Kaiserliche Monumentalität vs. Provinz

Byzanz entwickelt die extremste Statusdifferenzierung aller betrachteten Regionen:

**Kaiserliche Monumentalität**: Hagia Sophia, Hippodrom, Kaiserpalast —
kaiserlicher Selbstausdruck ohne Vergleich in der HRR-Welt. Die Dimensionen
sind theologisch kodiert: das Kaisergebäude spiegelt die göttliche Ordnung,
nicht den menschlichen Wettbewerb.[^mango1976-monumentalitaet]

**Provinziale Normalität**: Außerhalb Konstantinopels gibt es kein
vergleichbares monumentales Bauprogramm. Der Abstand zwischen Kaiserpalast
und städtischem Handwerkerhaus ist größer als im HRR.

> [!NOTE]
> **BVILLAGE-Implikation**: Für byzantinische Kontexte braucht die
> `wealth`-Skala eine andere Kalibrierung — mit größerem Abstand zwischen
> Klasse 5 (Aristokratie) und Klasse 1–3 (städtische Bevölkerung).

---

**Zusammenfassung Repräsentationslogiken:**

| Region | `representation_direction` | Primäres Statusmedium | `wealth` mappt auf |
|---|---|---|---|
| HRR | `outward` | Fassade, Geschosszahl | `floor_count`, `ornament_density` |
| England | `interior_horizontal` | Great Hall Größe/Qualität | `hall_size`, `hall_quality` |
| Al-Andalus | `inward` | Innenhofqualität, Wasser | `courtyard_quality`, `stucco_grade` |
| Skandinavien | `material_quality` | Holzqualität, Ensemble | `joint_complexity`, `ensemble_size` |
| Byzanz (Hauptstadt) | `imperial_theological` | Dimension, Material | Separate Skala |

---

## 5. Gebäudetypen als soziale Kategorien

Die morphologischen Typen des BVILLAGE-Systems sind nicht nur technische
Kategorien. Sie sind soziale Positionen im Siedlungsgefüge.

**Das Bauernhaus (ländlich, HRR)**: Einhaus-Logik. Produktionsfunktion
dominiert. Repräsentation ist sekundär — aber nicht abwesend: Toreinfahrt,
Firsthöhe, Tordekoration sind sichtbare Statusmarker.[^bedal1993-bauernhaus]

**Das Handwerkerhaus (städtisch, HRR)**: Erdgeschoss für Werkstatt und
Laden, Obergeschoss für Wohnen, Dachgeschoss für Lager. Zunftmitglied
mit definierten Rechten und Pflichten.[^boockmann1987-handwerker]

**Das Kaufmannshaus (städtisch, wohlhabend, HRR)**: Repräsentation als
primäre Funktion der Fassade. Kanonische Parzelle: 6–10 m Breite,
12–20 m Tiefe. Stockwerkszahl als Wohlstandsindex.[^stiewe2007-kaufmann]

**Das Ackerbürgerhaus (Kleinstadt)**: Hybrid aus Stadt und Land.
Schauseite zur Straße, Rückseite mit Stall und Garten.

**Das Manor House (England)**: Gentry-Typus. Great Hall als Kern.
Nicht prachtvoll wie ein Patrizierstadthaus, aber stabil und dauerhaft.[^brunskill2000-manor]

**Das Innenhofhaus (Al-Andalus)**: Geschlossene Straßenfassade,
Patio als Repräsentationszentrum. Klimatisch und sozial zugleich
motiviert.[^alhambra-innenhof]

**Das Langhausensemble (Skandinavien)**: Mehrere Bauten als Ensemble
(*huseby*), nicht ein Gebäude. Investition sichtbar in Qualität,
nicht Quantität.[^thue2012-huseby]

> [!IMPORTANT]
> **BVILLAGE-Implikation**: `settlement_type` × `wealth` × `primary_function`
> × `region` ergibt die soziale Kategorie, die dann die morphologischen
> Parameter steuert. Diese vier Parameter sind nicht unabhängig — sie
> konstituieren zusammen den sozialen Kontext, aus dem das Gebäude wächst.

---

## 6. Was sich nicht ändern darf — und was sich muss

### 6.1 Invarianten

Über alle Epochen, Regionen und Wohlstandsstufen hinweg:

- **Grünholzverbau**: Frisch geschlagenes Holz ist Standard.
  Trockenes Holz ist Ausnahme.[^gruenholz]
- **Modulares Maßsystem**: Abmessungen sind Vielfache eines Grundmaßes.
  Kein metrisches System.[^massystem]
- **Zapfen-Schlitz als Universalverbindung**: Die Variante wechselt,
  das Prinzip bleibt.[^zapfen-schlitz]
- **Soziale Einbettung des Bauprozesses**: Kein Gebäude entsteht ohne
  soziales Netzwerk.

**Regional unterschiedliche Invarianten**:
- Islamischer Kontext: Innenhof als strukturelles Raumzentrum ist Invariante
  für alle `wealth`-Klassen.
- Skandinavischer Kontext: Holz als primäres Material ist Invariante
  (Stein tritt erst nach Hansekontakt und Christianisierung auf).
- Byzantinischer Kontext: Stein als primäres Material ist Invariante
  (Holz nur für Innenausbau und Dachkonstruktion).

### 6.2 Wandelnde Parameter

Was sich ändert — epochal, regional, sozial:

- Konstruktionssystem (Ständerbau → Stockwerksbau): epochal, regional geshiftet
- Ornamentdichte: epochal + `wealth`
- Infill-Material: regional + epochal (Holzmangel → Ziegel)
- Vorkragungstiefe: epochal + `wealth` + städtisches Stadtrecht
- Querschnittsdimensionen: epochal (Holzmangel erzwingt Schlankung nach ~1650)
- Fassadenbehandlung (sichtbar vs. verputzt): epochal (ab ~1700 Statuswandel)
- **`representation_direction`**: regional (nicht epochal — Grundlogik ändert
  sich nicht innerhalb einer Kultur, sondern zwischen Kulturen)

---

## 7. BVILLAGE-Syntheseregeln

### Regel 1: Technische und soziale Plausibilität sind gleich obligatorisch

Ein Gebäude, das physikalisch korrekt, aber sozial inkohärent ist,
ist historisch falsch. Ein Patrizierhaus mit Flechtwerk-Infill. Ein
Bauernhaus mit 6 Stockwerken. Ein städtisches Handwerkerhaus ohne
Werkstattfläche.

> [!IMPORTANT]
> Der `PhysicalPlausibilityValidator` prüft Physik.
> Die `CulturePolicy` prüft soziale Kohärenz.
> **Beide Validierungen sind harte Grenzen.**

### Regel 2: wealth ist ein Bündel, kein Skalar

`wealth` steuert gleichzeitig: Materialqualität, Ornamentdichte,
Querschnittsgröße, Vorkragungstiefe, Geschosszahl, Infill-Material,
Fassadenbehandlung. Diese Dimensionen korrelieren, weil sie dasselbe
soziale Signal senden.

> [!IMPORTANT]
> Eine `WealthPolicy` muss ein konsistentes Bündel liefern, nicht
> unabhängige Einzelparameter. Das Bündel ist regional verschieden
> (vgl. [Repräsentationslogiken](#representation-logic-table)).

### Regel 3: settlement_type und region modulieren den wealth-Effekt

Derselbe `wealth`-Wert erzeugt in Stadt und Dorf verschiedene Häuser.
Derselbe `wealth`-Wert erzeugt in HRR und Al-Andalus fundamental
verschiedene Häuser (außen vs. innen orientiert).

> [!IMPORTANT]
> Die Mapping-Funktion `wealth → morphology` ist regional verschieden
> und muss als solche implementiert werden. Ein universelles Mapping
> ist historisch falsch.

### Regel 4: Constraints haben Herkunft

> [!IMPORTANT]
> Jeder `ConstraintsPolicy`-Parameter hat eine Herkunft:
> - physikalisch (Statik)
> - rechtlich (Stadtrecht)
> - sozial (Zunftnorm)
> - ökonomisch (Materialverfügbarkeit)
>
> Diese Herkunft muss im Code dokumentiert sein.
> Ein Constraint ohne Herkunft ist eine willkürliche Grenze —
> und damit historisch nicht verteidigbar.

### Regel 5: Bauen ist ein Prozess, nicht ein Zustand

Das Gebäude entsteht in einer Sequenz: Entscheidung, Beauftragung,
Abbund, Aufrichtung, Ausbau, Nutzung, Umbau, Verfall. BVILLAGE
generiert einen Zustand — aber dieser Zustand ist Momentaufnahme
eines Prozesses.

### Regel 6: Die Repräsentationsrichtung ist regional verschieden

> [!IMPORTANT]
> `representation_direction` muss aus `region` und `religion_context`
> abgeleitet werden — **nicht** aus `wealth` oder `archetype`.
>
> | Region | `representation_direction` |
> |---|---|
> | HRR | `outward` |
> | England | `interior_horizontal` |
> | Al-Andalus | `inward` |
> | Skandinavien | `material_quality` |
> | Byzanz Hauptstadt | `imperial_theological` |

---

## 8. Offene Fragen für BVILLAGE

> [!WARNING]
> **Frage 1 — Wie wird Bauherrschaft modelliert?**
> BVILLAGE braucht ein `BuildingContext`-Objekt, das Kapital, sozialen
> Status, Zunftzugehörigkeit und Absicht des Bauherrn trägt — über die
> abstrakten Parameter `wealth` und `settlement_type` hinaus.

> [!WARNING]
> **Frage 2 — Wie werden Rechtsconstraints spezifiziert?**
> Vorkragungsrechte, Traufhöhen, Parzellenausnutzung variieren zwischen
> Städten. Für historisch genaue Generierung städtischer Bauten braucht
> die `ConstraintsPolicy` stadtspezifische Regelprofile. Das ist
> Forschungsaufwand, der noch aussteht.

> [!WARNING]
> **Frage 3 — Wie wird Gebäudealter modelliert?**
> Ein Haus von 1280, das 1380 noch steht, sieht anders aus als ein
> Neubau von 1380. Reparaturen, Ergänzungen, Umbauten akkumulieren sich.
> BVILLAGE generiert heute Neubauten.

> [!WARNING]
> **Frage 4 — Wie wird kollektive Arbeit im Generator abgebildet?**
> Was war überhaupt machbar ohne professionelle Vollzeitbauarbeiter?
> Das limitiert Komplexität und Präzision für ländliche Kontexte.

> [!WARNING]
> **Frage 5 — RepresentationPolicy als neue Komponente?**
> Für Al-Andalus-Erweiterung: Wie invertiert man die Mapping-Logik
> von `wealth → facade_parameters` zu `wealth → courtyard_parameters`?
> Das erfordert möglicherweise eine eigenständige
> `RepresentationPolicy`-Komponente, die `StylePolicy` vorgelagert ist.

---

## 9. Quellen

**Anker, Leif:** The Norwegian Stave Churches. Oslo: Arfo, 1997. [HART]

**Bedal, Konrad:** Historische Hausforschung. Münster: Coppenrath, 1993. [MITTEL]

**Binding, Günther:** Baubetrieb im Mittelalter. Darmstadt: WBG, 1993. [MITTEL/HART]

**Boockmann, Hartmut:** Die Stadt im späten Mittelalter. München: Beck, 1987. [MITTEL]

**Brunskill, R. W.:** Illustrated Handbook of Vernacular Architecture.
London: Faber, 2000. [MITTEL/HART]

**Dodds, Jerrilynn D.:** Architecture and Ideology in Early Medieval Spain.
University Park: Penn State UP, 1990. [MITTEL]

**Dyer, Christopher:** Standards of Living in the Later Middle Ages.
Cambridge: CUP, 1989. [MITTEL/HART]

**Eißing, Thomas et al.:** Vorindustrieller Holzbau. Heidelberg: Propylaeum, 2023.
DOI: https://doi.org/10.11588/sbhbf.2023.1.99050 [HART]

**Epstein, Stephan R.:** Craft Guilds, Apprenticeship, and Technological Change.
Journal of Economic History 58 (1998), 684–713. [MITTEL]

**Großmann, G. Ulrich:** Der Fachwerkbau in Deutschland. Petersberg: Imhof, 2009. [MITTEL]

**Harvey, P. D. A.:** Manorial Records. London: British Records Association, 1984. [MITTEL/HART]

**Kaspar, Fred:** Fachwerkbauten des 14. bis 16. Jahrhunderts in Westfalen.
Münster: Coppenrath, 1986. [MITTEL/HART]

**Klein, Ulrich:** Zum aktuellen Forschungsstand des Holzbaus in Deutschland.
DGAMN-Mitteilungen Bd. 24. Paderborn 2012.
DOI: https://doi.org/10.11588/dgamn.2012.1.17131 [MITTEL]

**Long, Pamela O.:** Openness, Secrecy, Authorship. Baltimore: Johns Hopkins UP, 2001.

**Mango, Cyril:** Byzantine Architecture. London: Faber, 1976. [MITTEL]

**Recht, Roland:** Les Bâtisseurs des cathédrales gothiques. Straßburg: Éd. des Musées, 1989.

**Sawyer, Peter; Sawyer, Birgit:** Medieval Scandinavia. Minneapolis: Univ. of Minnesota Press, 1993. [MITTEL]

**Schulze, Hans K.:** Grundstrukturen der Verfassung im Mittelalter.
Stuttgart: Kohlhammer, 1985–2011. [MITTEL]

**Spufford, Peter:** Power and Profit. London: Thames & Hudson, 2002. [MITTEL/HART]

**Stiewe, Heinrich:** Fachwerkhäuser in Deutschland. Darmstadt: WBG, 2007. [MITTEL]

**Thue, Lars:** Norsk Bygningsleksikon. Oslo: Gyldendal, 2012. [HART]

**Wesoly, Kurt:** Lehrlinge und Handwerksgesellen am Mittelrhein.
Frankfurt: Waldemar Kramer, 1985. [MITTEL]

---

<!-- FOOTNOTES -->

[^schulze1985]: Schulze: Grundstrukturen der Verfassung im Mittelalter, 1985–2011. Boockmann: Die Stadt im späten Mittelalter, 1987. [MITTEL]

[^grossmann2009-status]: Großmann: Der Fachwerkbau in Deutschland, 2009. Stiewe: Fachwerkhäuser in Deutschland, 2007. [MITTEL]

[^grossmann2009-vorkragung]: Großmann: Der Fachwerkbau in Deutschland, 2009. [MITTEL]

[^stiewe2007-recht]: Stiewe: Fachwerkhäuser in Deutschland, 2007. Boockmann: Die Stadt im späten Mittelalter, 1987. [MITTEL]

[^bedal1993-kollektiv]: Bedal: Historische Hausforschung, 1993. Binding: Baubetrieb im Mittelalter, 1993. [MITTEL]

[^spufford2002-kapital]: Spufford: Power and Profit, 2002. Boockmann 1987. [MITTEL/HART]

[^boockmann1987-entscheidung]: Boockmann: Die Stadt im späten Mittelalter, 1987. Epstein: Journal of Economic History 58 (1998). [MITTEL]

[^binding1993-planung]: Binding: Baubetrieb im Mittelalter, 1993. Long: Openness, Secrecy, Authorship, 2001. [MITTEL]

[^eissing2023-zimmerplatz]: Eißing et al.: Vorindustrieller Holzbau, 2023. Klein: DGAMN-Mitteilungen, 2012. [HART]

[^bedal1993-richtfest]: Bedal: Historische Hausforschung, 1993. [MITTEL]

[^schwellenkult]: Bedal: Historische Hausforschung, 1993. Ethnologische Analogieschlüsse. [SCHWACH]

[^grossmann2009-mehraufwand]: Großmann: Der Fachwerkbau in Deutschland, 2009. Kaspar: Fachwerkbauten in Westfalen, 1986. [MITTEL]

[^epstein1998-konformitaet]: Epstein: Journal of Economic History 58 (1998). Wesoly: Lehrlinge und Handwerksgesellen, 1985. [MITTEL]

[^stiewe2007-constraints]: Stiewe: Fachwerkhäuser in Deutschland, 2007. Boockmann 1987. [MITTEL]

[^wesoly1985]: Wesoly: Lehrlinge und Handwerksgesellen, 1985. Boockmann 1987. [MITTEL]

[^hrr-hoehe]: Stiewe: Fachwerkhäuser in Deutschland, 2007. Großmann 2009. [MITTEL]

[^brunskill2000-hall]: Brunskill: Illustrated Handbook of Vernacular Architecture, 2000. [MITTEL/HART]

[^dyer1989-hall]: Dyer: Standards of Living in the Later Middle Ages, 1989. [MITTEL/HART]

[^alhambra-bestand]: Erhaltene Gebäude in Granada, Córdoba, Sevilla. Dodds 1990. [HART für Bestand; MITTEL für Interpretation]

[^anker1997-status]: Anker: The Norwegian Stave Churches, 1997. [HART]

[^sawyer1993-bonde]: Sawyer/Sawyer: Medieval Scandinavia, 1993. [MITTEL]

[^mango1976-monumentalitaet]: Mango: Byzantine Architecture, 1976. [MITTEL]

[^bedal1993-bauernhaus]: Bedal: Historische Hausforschung, 1993. Stiewe 2007. [MITTEL]

[^boockmann1987-handwerker]: Boockmann: Die Stadt im späten Mittelalter, 1987. [MITTEL]

[^stiewe2007-kaufmann]: Spufford: Power and Profit, 2002. Stiewe: Fachwerkhäuser in Deutschland, 2007. [MITTEL]

[^brunskill2000-manor]: Brunskill: Illustrated Handbook, 2000. Harvey: Manorial Records, 1984. [MITTEL/HART]

[^alhambra-innenhof]: Erhaltene Gebäude in Granada, Córdoba, Sevilla. Dodds 1990. [HART]

[^thue2012-huseby]: Thue: Norsk Bygningsleksikon, 2012. Anker 1997. [HART]

[^gruenholz]: Eißing et al.: Vorindustrieller Holzbau, 2023. [HART]

[^massystem]: Binding: Baubetrieb im Mittelalter, 1993. [MITTEL]

[^zapfen-schlitz]: Eißing et al.: Vorindustrieller Holzbau, 2023. Klein: DGAMN-Mitteilungen, 2012. [HART]

---

*BVILLAGE Research Foundation — Achse 6 — v2.1*
