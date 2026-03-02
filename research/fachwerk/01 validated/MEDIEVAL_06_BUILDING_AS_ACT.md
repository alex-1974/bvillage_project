# Achse 6 — Bauen als gesellschaftlicher Akt
## Das mittelalterliche Gebäude im Systemkontext

```
Dokument-Typ:  Research Foundation
Achse:         6 von 7
Scope:         BVILLAGE — alle Domains, alle Haustypen
Status:        v1.0
Referenziert von:
  MEDIEVAL_WORLD_OVERVIEW.md
  ARCH_POLICIES.md (StylePolicy, CulturePolicy, ConstraintsPolicy)
Referenziert:
  mittelalterliche_baupraxis_v2.md
  RESEARCH_FACHWERK_HISTORISCH.md
  RESEARCH_FACHWERKBAU.md
  MEDIEVAL_07_EPOCHS_AND_BREAKS.md
  MEDIEVAL_05_KNOWLEDGE_CRAFT.md
Evidenzgrade:
  [HART]   Direkt messbar, datierter Bestand, publizierte Messdaten
  [MITTEL] Wissenschaftlicher Konsens, erschlossen, nicht direkt messbar
  [SCHWACH] Analogieschluss, experimentelle Archäologie, Fachtradition
```

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

---

## 1. Das Gebäude als mehrdimensionales Objekt

Ein mittelalterliches Gebäude ist niemals nur technische Konstruktion.
Es ist gleichzeitig fünf Dinge — und alle fünf sind untrennbar verwoben.

### 1.1 Eigentumsbeweis

Im mittelalterlichen Rechtsverständnis konstituiert das Gebäude Eigentum
am Grund, nicht umgekehrt. Wer ein Haus baut und es nutzt, demonstriert
Besitzrecht. Das ist nicht Metapher — es hat rechtliche Konsequenz.
[MITTEL — Schulze 1985; Boockmann 1987]

Das erklärt, warum auch arme Haushalte investierten, was sie nicht hatten:
ein Haus, das verfiel, gefährdete den Rechtsanspruch. Unterhalt war keine
ästhetische Entscheidung. Er war Rechtsausübung.

**BVILLAGE-Implikation**: Gebäudezustand ist kein reiner `wealth`-Parameter.
Er hat eine rechtliche Dimension, die für Siedlungstyp und Eigentumsstruktur
relevant ist. Ein verfallenes Haus in einem gut dokumentierten Siedlungs-
kontext signalisiert gesellschaftliche Disruption, nicht nur Armut.

### 1.2 Statusanzeige

Das Gebäude kommuniziert. An Nachbarn, Stadtrat, Handelspartner, Reisende.
Die Botschaft ist codiert in: Geschosszahl, Vorkragungstiefe, Holzqualität,
Ornamentreichtum, Infill-Material, Fassadenbehandlung.
[MITTEL — Großmann 2009; Stiewe 2007]

Großmann (2009) belegt, dass die Vorkragung primär Repräsentations-
merkmal war, nicht Schutzfunktion. Je tiefer die Auskragung, desto teurer
und aufwändiger — und desto deutlicher die Botschaft.
[MITTEL — Großmann 2009]

Patrizierhäuser in Reichsstädten erreichten 7–8 Stockwerke. Nicht weil
7 Stockwerke funktional nötig gewesen wären — sondern weil Höhe lesbar
war. [MITTEL — RESEARCH_FACHWERKBAU.md; Stiewe 2007]

**BVILLAGE-Implikation**: Der `wealth`-Parameter steuert nicht nur Material-
qualität und Querschnittsgröße. Er steuert die Kodierungsintensität der
Statusbotschaft: Ornamentdichte, Vorkragungstiefe, Geschosszahl, Infill-
Materialwahl. Diese Variablen sind nicht unabhängig — sie sind kohärente
Signale desselben sozialen Anspruchs.

### 1.3 Rechtsdokument

Das Gebäude ist Träger von Rechtsverhältnissen, die über den Eigentümer
hinausgehen. Vorkragungsrechte waren stadtrechtlich geregelt — das Recht,
in den öffentlichen Straßenraum auszukragen, war eine stadtrechtliche
Konzession, keine selbstverständliche Baufreiheit.
[MITTEL — Stiewe 2007; Boockmann 1987]

Grenzverläufe, Nutzungsrechte, Dienstbarkeiten — sie alle wurden am
physischen Gebäude abgelesen, nicht an Katasterdokumenten. Wände,
Dachtraufen, Fenster waren Rechtsobjekte.

**BVILLAGE-Implikation**: Die `ConstraintsPolicy` muss stadtrechtliche
Regelungen als lokale Hard-Constraints abbilden — insbesondere für
Vorkragung, Traufhöhe und Parzellenausnutzung. Diese Constraints sind
nicht physikalisch, sondern juristisch. Sie variieren zwischen Städten
und über die Zeit.

### 1.4 Kollektives Werk

Der Bau eines Fachwerkhauses war keine Einzelleistung. Der Abbund
(Vorfertigung) erforderte den Zimmermann als Fachmann. Das Aufrichten
dagegen konnte von vielen ungelernten Helfern durchgeführt werden, die
zum Richtfest mit Naturalien entlohnt wurden. [HART — RESEARCH_FACHWERKBAU.md]

Diese Arbeitsteilung machte den Bau für breite Bevölkerungsschichten
zugänglich. Gleichzeitig verankerte sie das Gebäude in sozialen
Verpflichtungen: Wer beim Richtfest half, hatte Ansprüche auf
Gegenseitigkeit. Das Haus entstand im sozialen Schuldengeflecht.
[MITTEL — Bedal 1993; Binding 1993]

**BVILLAGE-Implikation**: Die `settlement_type`-Dimension beeinflusst,
wie dieser kollektive Aspekt gewichtet ist. Städtische Handwerkergesellschaft
(Zunft organisiert Arbeit, Geld zahlt Lohn) vs. ländliche Dorfgemeinschaft
(Gegenseitigkeitspflicht, Naturalentlohnung, sozialer Zusammenhalt als
Produktionsfaktor) — beides erzeugt dasselbe Ergebnis, aber aus anderen
sozialen Dynamiken.

### 1.5 Wirtschaftliche Anlage

Das Haus ist Kapital. Es kann vermietet, verpfändet, vererbt, verkauft
werden. Städtische Oberstockwerke wurden an Mieter vergeben. Keller an
Händler. Ladenfronten an Gewerbetreibende.
[MITTEL — Spufford 2002; Boockmann 1987]

Für den Bauherrn ist das Haus also gleichzeitig Wohnung, Werkstatt,
Lager, Repräsentationsraum und Kapitalanlage — oft alles unter einem Dach,
oft mit fließenden Grenzen zwischen diesen Nutzungen.

**BVILLAGE-Implikation**: Der `InteriorPlanner` muss diese Nutzungsvielfalt
kennen. Erdgeschoss-Kommerz, Mittelgeschoss-Wohnen, Obergeschoss-Lager
ist kein Sonderfall — es ist der städtische Normalfall für wohlhabende
Handwerker und Kaufleute.

---

## 2. Der Bauprozess als sozialer Akt

### 2.1 Entscheidung: Wer baut?

Die Entscheidung zu bauen ist keine rein ökonomische. Sie ist eingebettet
in soziale Anlässe: Heirat, Erbschaft, Zunftzulassung, Stadtbürgerrecht.
Wer neu in die Zunft eintritt, braucht ein standesgemäßes Haus. Wer
erbt, muss den Rechtsanspruch durch Nutzung demonstrieren.
[MITTEL — Boockmann 1987; Epstein 1998]

Das erklärt die demographisch nachweisbaren Bauphasen: Pestwiederaufbau
(1360–1400), Zunftblüte (15. Jh.), Nachkriegswiederaufbau (nach 1648).
Bauen folgt sozialen Opportunitätsfenstern, nicht nur Kapitalverfügbarkeit.

### 2.2 Beauftragung: Wer plant?

Für Profanbauten des Mittelstands gilt: Der Zimmermann plant und baut.
Es gibt keinen Architekten im modernen Sinne. Der Bauherr kommuniziert
Typus, Größe und Ausstattungsgrad. Der Zimmermann übersetzt in Konstruktion.
[MITTEL — Binding 1993; Long 2001]

Für gehobene Stadtbauten und öffentliche Gebäude: Der Werkmeister als
spezialisierter Planungsverantwortlicher, der Zunftmeister als Ausführender.
Für Kirchenbauten: Die Bauhütte mit institutionalisierter Geometrie und
Wissensakkumulation. [MITTEL — Recht 1989; Binding 1993]

**BVILLAGE-Implikation**: `knowledge_infrastructure_tier` aus Achse 5
(rural vernacular / städtische Zunft / Bauhütte) bestimmt nicht nur
die Konstruktionskompetenz, sondern auch die Planungsstruktur. Ein
Dorfzimmermann plant anders als ein Stadtmeister — nicht nur technisch,
sondern prozessual.

### 2.3 Vorfertigung: Der Zimmerplatz

Vollständige Vorfertigung auf dem Zimmerplatz ist durch Abbundzeichen
physisch belegt. [HART — Eißing/Furrer 2023; Klein 2012]

Der Grundriss wird in Originalgröße auf dem Boden aufgerissen. Jedes
Bauteil wird markiert (Abbundzeichen: Wall, Position, Orientierung).
Das Gebäude existiert virtuell vollständig, bevor der erste Ständer
auf der Baustelle steht.

Das ist nicht Modernität — das ist die Lösung für das Problem der
Baustellenlogistik ohne Lagerkapazität und mit sozialer Termindisziplin
(Richtfest als angekündigtes Gemeinschaftsereignis).

### 2.4 Aufrichtung: Das Richtfest

Das Richtfest ist mittelalterliche Tradition, historisch belegbar.
[MITTEL — Bedal 1993]

Es ist gleichzeitig: logistisches Ereignis (viele Helfer für kurze Zeit),
soziales Ereignis (Verpflichtungsnetz wird aktiviert), religiöses Ereignis
(Segnung, Richtkranz, Gebete für das Haus und seine Bewohner) und
Demonstration des sozialen Netzwerks des Bauherrn.

**BVILLAGE-Implikation**: Das Richtfest ist kein modellierbares Detail —
es ist der Kontext, in dem Bauen als sozialer Akt am deutlichsten sichtbar
wird. Für die `CulturePolicy` relevant ist: Es gibt Anlässe, zu denen
gebaut wurde, und Anlässe, zu denen nicht gebaut wurde. Der Bauprozess
hat eine soziale Saisonalität.

### 2.5 Einzug und Nutzung

Der Einzug in ein neues Haus hatte rituelle Dimension: Schwellenkult
(die Schwelle als Übergang, Schutzzeichen), erste Feuerung im Herd als
Inbesitznahme. Auch Profanbauten sind nicht sakral neutral.
[SCHWACH — ethnologische Analogieschlüsse; Bedal 1993]

---

## 3. Warum Häuser so aussehen wie sie aussehen

### 3.1 Die Logik des Mehraufwands

Viele Entscheidungen im mittelalterlichen Hausbau erscheinen technisch
irrational: teurer als nötig, aufwändiger als funktional erforderlich.
Die Erklärung liegt nicht in der Technik, sondern in der sozialen Logik.

Eichenholz wo Tanne reicht: Eiche signalisiert Dauerhaftigkeit und
Reichtum — sie ist schwerer zu beschaffen, teurer, langlebiger.
Die Botschaft: Dieser Bau ist für Generationen.

Geschnitzte Knaggen wo glatte ausreichen: Ornament ist nicht Dekoration,
es ist Qualitätsnachweis. Komplexe Schnitzereien erforderten erfahrene
Meister. Sie waren der Beweis, dass man sich den Besten leisten konnte.
[MITTEL — Großmann 2009; Kaspar 1986]

Mehrfache Vorkragung wo einfache genügte: Jede zusätzliche Auskragung
erfordert komplexere Verbindungen, mehr Material, höhere handwerkliche
Präzision. Und sie ist von der Straße aus lesbar.

### 3.2 Die Logik der regionalen Konformität

Ein Haus, das konstruktiv "falsch" wirkt nach lokalen Normen, signalisiert
Fremdheit — auch wenn es technisch überlegen ist. Zunftordnungen schützten
lokale Standards explizit gegen auswärtige Meister.
[MITTEL — Epstein 1998; Wesoly 1985]

Das erklärt, warum Innovationen sich langsam ausbreiten: nicht wegen
technischer Trägheit, sondern wegen sozialer Kosten der Abweichung.
Ein Zimmermann, der anders baut als seine Zunftbrüder, riskiert Ruf
und Auftragslage.

**BVILLAGE-Implikation**: Historische Plausibilität ist soziale Kohärenz,
nicht nur physikalische Korrektheit. Regionale Konformität ist ein
Qualitätsmerkmal — nicht Konservativismus. Der `StylePolicy`-Parameter
`regional_conformity` sollte explizit modelliert werden.

### 3.3 Die Logik der Einschränkungen

Nicht alle Entscheidungen sind Kommunikation. Manche sind Zwang.

Stadtrechtliche Einschränkungen: Vorkragungstiefe, Traufhöhe, Parzellenbreite
sind oft normiert. Was nach oben begrenzt, ermutigt zur Ausschöpfung des
Maximalrahmens: wenn 0,8 m Vorkragung erlaubt sind, baut der Ehrgeizige
0,8 m — nicht 0,4 m. [MITTEL — Stiewe 2007; Boockmann 1987]

Ressourceneinschränkungen: Holzmangel erzwingt schlankere Querschnitte.
Das ist nicht Sparsamkeit als Tugend — es ist Reaktion auf Marktbedingungen.

Soziale Einschränkungen: Wer unter dem Zunftmindestniveau baut, verliert
Ansehen. Wer über dem Standesniveau baut, macht sich verdächtig.
Der Spielraum ist nach oben und unten begrenzt.
[MITTEL — Epstein 1998; Boockmann 1987]

---

## 4. Gebäudetypen als soziale Kategorien

Die morphologischen Typen des BVILLAGE-Systems sind nicht nur technische
Kategorien. Sie sind soziale Positionen im Siedlungsgefüge.

### 4.1 Das Bauernhaus (ländlich)

Einhaus-Logik: Wohnen, Wirtschaften, Lagern unter einem Dach.
Die Produktionsfunktion dominiert. Repräsentation ist sekundär —
aber nicht abwesend: Toreinfahrt, Firsthöhe, Tordekoration sind
sichtbare Statusmarker auch in bäuerlichem Kontext.
[MITTEL — Bedal 1993; Stiewe 2007]

Soziale Position: Bauer als Wirtschaftssubjekt (Grundherr, Steuerzahler,
Wehrpflichtiger). Das Haus materialisiert diese Position.

### 4.2 Das Handwerkerhaus (städtisch)

Erdgeschoss für Werkstatt und Laden, Obergeschoss für Wohnen, Dachgeschoss
für Lager. Die Trennung von Produktion und Wohnen ist graduell, nicht absolut.
[MITTEL — Boockmann 1987; RESEARCH_FACHWERK_HISTORISCH.md]

Soziale Position: Zunftmitglied mit definierten Rechten und Pflichten.
Das Haus muss Zunftmindeststandards erfüllen — nach oben ist es
individueller Ehrgeiz.

### 4.3 Das Kaufmannshaus (städtisch, wohlhabend)

Repräsentation als primäre Funktion der Fassade. Gewölbekeller für
Warenlager, Kontor im Erdgeschoss, Wohnen in den Mittelgeschossen,
Lager und Gesinde in den Obergeschossen. Maximale Raumausnutzung
der Parzelle — in die Höhe, weil die Breite begrenzt ist.
[MITTEL — Spufford 2002; RESEARCH_FACHWERK_HISTORISCH.md]

Kanonische Parzelle: 6–10 m Breite, 12–20 m Tiefe. [MITTEL — Stiewe 2007]
Stockwerkszahl als Wohlstandsindex: 4 Stockwerke = etablierter Bürger,
7–8 Stockwerke = Patrizier. [MITTEL — RESEARCH_FACHWERKBAU.md]

### 4.4 Das Ackerbürgerhaus (Kleinstadt)

Hybrid aus Stadt und Land. Schauseite zur Straße mit Laden und Büro.
Rückseite mit Stall und Garten. Weder Bauernhaus noch Stadthaus —
die Mitte, die überall verbreitet ist.
[MITTEL — RESEARCH_FACHWERK_HISTORISCH.md; Stiewe 2007]

**BVILLAGE-Implikation**: `settlement_type` × `wealth` × `primary_function`
ergibt die soziale Kategorie, die dann die morphologischen Parameter steuert.
Diese drei Parameter sind nicht unabhängig — sie konstituieren zusammen
den sozialen Kontext, aus dem das Gebäude wächst.

---

## 5. Was sich nicht ändern darf — und was sich muss

### 5.1 Invarianten

Über alle Epochen, Regionen und Wohlstandsstufen hinweg gibt es
Konstanten im mittelalterlichen Profanbau:

- **Grünholzverbau**: Frisch geschlagenes Holz ist Standard.
  Trockenes Holz ist Ausnahme. [HART — Eißing/Furrer 2023]
- **Modulares Maßsystem**: Abmessungen sind Vielfache eines Grundmaßes.
  Kein metrisches System. [MITTEL — Binding 1993]
- **Zapfen-Schlitz als Universalverbindung**: Die Variante wechselt,
  das Prinzip bleibt. [HART — Eißing/Furrer 2023; Klein 2012]
- **Soziale Einbettung des Bauprozesses**: Kein Gebäude entsteht ohne
  soziales Netzwerk. [MITTEL — Bedal 1993]

### 5.2 Wandelnde Parameter

Was sich ändert — epochal, regional, sozial:

- Konstruktionssystem (Ständerbau → Stockwerksbau): epochal, regional geshiftet
- Ornamentdichte: epochal + wealth
- Infill-Material: regional + epochal (Holzmangel → Ziegel)
- Vorkragungstiefe: epochal + wealth + städtisches Stadtrecht
- Querschnittsdimensionen: epochal (Holzmangel erzwingt Schlankung nach ~1650)
- Fassadenbehandlung (sichtbar vs. verputzt): epochal (ab ~1700 Statuswandel)

---

## 6. BVILLAGE-Syntheseregeln

Diese Regeln destillieren Achse 6 in operative Prinzipien für die
Policy-Implementierung.

### Regel 1: Technische und soziale Plausibilität sind gleich obligatorisch

Ein Gebäude, das physikalisch korrekt, aber sozial inkoherent ist, ist
historisch falsch. Ein Patrizierhaus mit Flechtwerk-Infill. Ein Bauernhaus
mit 6 Stockwerken. Ein städtisches Handwerkerhaus ohne Werkstattfläche.
Der `PhysicalPlausibilityValidator` prüft Physik. Die `CulturePolicy` prüft
soziale Kohärenz. Beide Validierungen sind harte Grenzen.

### Regel 2: wealth ist ein Bündel, kein Skalar

`wealth` steuert gleichzeitig: Materialqualität, Ornamentdichte,
Querschnittsgröße, Vorkragungstiefe, Geschosszahl, Infill-Material,
Fassadenbehandlung. Diese Dimensionen sind nicht unabhängig — sie
korrelieren, weil sie dasselbe soziale Signal senden. Eine
`WealthPolicy` muss ein konsistentes Bündel liefern, nicht
unabhängige Einzelparameter.

### Regel 3: settlement_type moduliert den wealth-Effekt

Derselbe `wealth`-Wert erzeugt in Stadt und Dorf verschiedene Häuser.
Städtischer Reichtum materialisiert in Höhe, Vorkragung, Ornament.
Ländlicher Reichtum materialisiert in Firsthöhe, Stallgröße,
Tordekoration, Parzellengröße. Der `settlement_type` ist nicht
dekorativ — er ist strukturell für die Übersetzung von wealth
in konkrete Morphologie.

### Regel 4: Constraints haben Herkunft

Jeder `ConstraintsPolicy`-Parameter hat eine Herkunft: physikalisch
(Statik), rechtlich (Stadtrecht), sozial (Zunftnorm), ökonomisch
(Materialverfügbarkeit). Diese Herkunft muss im Code dokumentiert
sein. Ein Constraint ohne Herkunft ist eine willkürliche Grenze —
und damit historisch nicht verteidigbar.

### Regel 5: Bauen ist ein Prozess, nicht ein Zustand

Das Gebäude entsteht in einer Sequenz: Entscheidung, Beauftragung,
Abbund, Aufrichtung, Ausbau, Nutzung, Umbau, Verfall. BVILLAGE
generiert einen Zustand — aber dieser Zustand ist Momentaufnahme
eines Prozesses. Der Generator muss wissen, in welchem Prozessstadium
das Gebäude sich befindet: Neubau (1350), Bestand mit Erweiterung (1420),
Bestand nach Pesterbschaft (1380)?

---

## 7. Offene Fragen für BVILLAGE

**Frage 1 — Wie wird Bauherrschaft modelliert?**
Der Bauherr ist der entscheidende Akteur: sein Kapital, sein sozialer
Status, seine Zunftzugehörigkeit, seine Absicht. BVILLAGE braucht
ein `BuildingContext`-Objekt, das diese Dimension trägt — über die
abstrakten Parameter `wealth` und `settlement_type` hinaus.

**Frage 2 — Wie werden Rechtsconstraints spezifiziert?**
Vorkragungsrechte, Traufhöhen, Parzellenausnutzung variieren zwischen
Städten. Für eine historisch genaue Generierung städtischer Bauten
braucht die `ConstraintsPolicy` stadtspezifische Regelprofile.
Das ist Forschungsaufwand, der noch aussteht.

**Frage 3 — Wie wird Gebäudealter modelliert?**
Ein Haus von 1280, das 1380 noch steht, sieht anders aus als ein
Neubau von 1380. Reparaturen, Ergänzungen, Umbauten akkumulieren
sich. BVILLAGE generiert heute Neubauten — aber historische Siedlungen
bestehen aus Häusern verschiedener Epochen und Zustände.

**Frage 4 — Wie wird kollektive Arbeit im Generator abgebildet?**
Die Frage ist nicht für den Generator selbst relevant — aber für die
Parametergrenzen: Was war überhaupt machbar ohne professionelle
Vollzeitbauarbeiter? Das limitiert Komplexität und Präzision
für ländliche Kontexte.

---

## 8. Quellen und wissenschaftliche Grundlage

### 8.1 Zitierte Werke

**Bedal, Konrad:** Historische Hausforschung. Münster: Coppenrath, 1993.
*Standardwerk der deutschen Hausforschung. Bauprozess, soziale Einbettung,
Richtfest, Schwellenkult. Primärquelle für Abschnitte 2 und 5.*

**Binding, Günther:** Baubetrieb im Mittelalter. Darmstadt: WBG, 1993.
*Bauorganisation, Planung, Bauherrschaft, Zimmerplatz. Primärquelle
für Abschnitt 2.*
[MITTEL/HART]

**Boockmann, Hartmut:** Die Stadt im späten Mittelalter. München: Beck, 1987.
*Stadtrechtliche Rahmenbedingungen, Sozialstruktur, Repräsentation.
Relevant für Abschnitte 1 und 3.*

**Eißing, Thomas; Furrer, Benno; Kayser, Christian et al.:** Vorindustrieller
Holzbau. 2. Aufl. Heidelberg: Propylaeum, 2023.
DOI: https://doi.org/10.11588/sbhbf.2023.1.99050 — PDF frei zugänglich.
*Dendrochronologische Methodik, Abbundzeichen, Grünholzverbau.
[HART]-Grundlage für Abschnitt 5.1.*

**Epstein, Stephan R.:** Craft Guilds, Apprenticeship, and Technological
Change in Preindustrial Europe. In: Journal of Economic History 58 (1998),
H. 3, S. 684–713.
*Zunftsystem, soziale Kosten der Abweichung, regionale Konformität.
Relevant für Abschnitte 3.2 und 4.*
[MITTEL]

**Großmann, G. Ulrich:** Der Fachwerkbau in Deutschland.
Petersberg: Imhof, 2009.
*Vorkragung als Repräsentationsmerkmal. Ornamentik als Statuscode.
Primärquelle für Abschnitte 1.2 und 3.1.*
[MITTEL]

**Kaspar, Fred:** Fachwerkbauten des 14. bis 16. Jahrhunderts in Westfalen.
Münster: Coppenrath, 1986. ISBN 3-88547-298-8.
*Ornamentik als Qualitätsnachweis. Regionalmonographie.
Relevant für Abschnitt 3.1.*
[MITTEL/HART]

**Klein, Ulrich:** Zum aktuellen Forschungsstand des hoch- und
spätmittelalterlichen Holzbaus in Deutschland. In: DGAMN-Mitteilungen
Bd. 24. Paderborn 2012, S. 9–38.
DOI: https://doi.org/10.11588/dgamn.2012.1.17131 — PDF frei zugänglich.
*Abbundzeichen als Beleg für Vorfertigung. [HART]-Grundlage.*

**Long, Pamela O.:** Openness, Secrecy, Authorship. Baltimore: Johns
Hopkins University Press, 2001.
*Planungsstruktur, Zimmermann als Planer, Wissenstransfer.
Relevant für Abschnitt 2.2.*

**Recht, Roland:** Les Bâtisseurs des cathédrales gothiques. Straßburg:
Éditions des Musées de Strasbourg, 1989.
*Bauhüttenorganisation, Werkmeister, Planungsverantwortung.*

**Schulze, Hans K.:** Grundstrukturen der Verfassung im Mittelalter.
Stuttgart: Kohlhammer, 1985–2011.
*Eigentumsrecht, Besitzkonstituierung durch Nutzung.
Relevant für Abschnitt 1.1.*
[MITTEL]

**Spufford, Peter:** Power and Profit. London: Thames & Hudson, 2002.
*Handel, Kapital, Gebäude als Wirtschaftsobjekt.
Relevant für Abschnitte 1.5 und 4.3.*
[MITTEL/HART]

**Stiewe, Heinrich:** Fachwerkhäuser in Deutschland. Darmstadt: WBG, 2007.
*Sozialgeschichte, Statuswandel, Bauordnungen, Parzellenmaße.
Primärquelle für Abschnitte 1, 3 und 4.*

**Wesoly, Kurt:** Lehrlinge und Handwerksgesellen am Mittelrhein.
Frankfurt: Waldemar Kramer, 1985.
*Zunftnormen, soziale Einschränkungen nach oben und unten.
Relevant für Abschnitt 3.3.*
[MITTEL]

---

### 8.2 Weiterführende Literatur

**Dyer, Christopher:** Standards of Living in the Later Middle Ages.
Cambridge: Cambridge University Press, 1989.
*Quantitative Studie zu Lebensstandards, Haushaltsgrößen, materielle Kultur.
Englischer Fokus, methodisch übertragbar.*

**Freigang, Christian (Hrsg.):** Gotische Architektur in Frankreich.
München: Hirmer, 2018.
*Sozialgeschichte der Auftragsarchitektur: Bauherren, Intentionen,
Repräsentation. Für Sakralbau, aber konzeptionell übertragbar.*

**Herlihy, David; Klapisch-Zuber, Christiane:** Tuscans and their Families.
New Haven: Yale University Press, 1985.
*Quantitative Sozialgeschichte. Haushaltsgrößen, Besitzverhältnisse.
Florentiner Fokus, methodisch vorbildhaft für Nutzungsplanung.*

**Wiesner-Hanks, Merry E.:** Women and Gender in Early Modern Europe.
Cambridge: Cambridge University Press, 2008.
*Frauen als Bauherrschaft, Eigentumsrechte, Nutzungskontrolle.
Relevant für vollständige Haushaltsmodellierung.*

---

*BVILLAGE Research Foundation — Achse 6 — v1.0*
