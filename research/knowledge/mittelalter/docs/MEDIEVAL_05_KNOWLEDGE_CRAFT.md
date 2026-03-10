# Achse 5 — Wissen, Handwerk und Wissensinfrastruktur
## Die Wissensgrundlage mittelalterlichen Bauens

```
Dokument-Typ:  Research Foundation
Achse:         5 von 7
Scope:         BVILLAGE — alle Domains, alle Haustypen
               Zeitraum: 500–1750 (Kern: 950–1500)
               Raum: Westeuropa und Byzanz
Status:        v2.1
Referenziert von:
  MEDIEVAL_WORLD_OVERVIEW.md
  ARCH_POLICIES.md (CulturePolicy, ConstructionCulturePolicy)
  DEV_ROADMAP.md (RES-001)
Referenziert:
  MEDIEVAL_07_EPOCHS_AND_BREAKS.md
  MEDIEVAL_06_BUILDING_AS_ACT.md
  MEDIEVAL_04_ECONOMY_TRADE.md
```

---

## Inhaltsverzeichnis

- [Vorbemerkung](#vorbemerkung-warum-achse-5-das-zentrum-ist)
- [1. Kernbefund: Drei strukturell verschiedene Wissensräume](#1-kernbefund-drei-strukturell-verschiedene-wissensräume)
- [2. Das Dreistufenmodell (HRR)](#2-das-dreistufenmodell-hrr)
  - [2.1 Tier 1 — Bauhütte](#21-tier-1--bauhütte-monumental--und-klerikalbauten)
  - [2.2 Tier 2 — Zimmererzunft](#22-tier-2--zimmererzunft-städtischer-und-bürgerlicher-profanbau)
  - [2.3 Tier 3 — Volkshandwerk](#23-tier-3--volkshandwerk-ländlicher-und-bäuerlicher-bau)
- [3. Strukturvergleich der drei Wissensstufen](#3-strukturvergleich-der-drei-wissensstufen)
- [4. Wissenstransfer zwischen den Stufen](#4-wissenstransfer-zwischen-den-stufen)
- [5. Wissenstransmission: Mechanismen ohne Schrift](#5-wissenstransmission-mechanismen-ohne-schrift)
- [6. Regionale Wissensinfrastrukturen: Gesamteuropa](#6-regionale-wissensinfrastrukturen-gesamteuropa)
  - [6.1 England](#61-england-masons-company-und-carpenters-company)
  - [6.2 Skandinavien](#62-skandinavien-mündliche-wissenstradition-der-stabkirchenerbauer)
  - [6.3 Al-Andalus](#63-islamische-bauwissenstradition-al-andalus)
  - [6.4 Byzanz](#64-byzantinisches-kaiserbauamt)
- [7. Epochale Entwicklung](#7-epochale-entwicklung-der-wissensinfrastruktur)
- [8. BVILLAGE-Implikationen](#8-bvillage-implikationen)
- [9. Primärquellen](#9-primärquellen)
- [10. Offene Forschungsfragen](#10-offene-forschungsfragen-für-bvillage)
- [11. Quellen](#11-quellen)

---

## Vorbemerkung: Warum Achse 5 das Zentrum ist

Das MEDIEVAL_WORLD_OVERVIEW benennt es explizit: Wenn eine Achse die anderen
dominiert, dann ist es Achse 5. Was gebaut werden kann, hängt nicht primär
vom verfügbaren Material, vom Rechtsrahmen oder von der Wirtschaftskraft ab —
sondern davon, was die Bauenden wissen.

Diese Achse ist kein Spezialdossier über Handwerksgeschichte. Sie ist
die Achse, die alle anderen in ihren Möglichkeiten limitiert oder freisetzt.
Ein waldreicher Landstrich ohne Zimmermannswissen produziert kein
Fachwerk-Hallenhaus. Eine prosperierende Stadt ohne erfahrene Zunft produziert
keine aufwändige Dachlandschaft. Die Ressource Wissen ist die bindende
Constraint über allen anderen Ressourcen.

**Scope-Erweiterung in v2.0**: Das Dreistufenmodell ist am HRR entwickelt
und bleibt sein Kern. Abschnitt 6 erschließt systematisch die
Wissensinfrastrukturen außerhalb des HRR. Befund: Das Dreistufenmodell ist
nicht universal — andere Kulturen haben andere Organisationsformen entwickelt,
die zu anderen Ergebnissen führen.

> [!IMPORTANT]
> `knowledge_infrastructure_tier` ist in der `CulturePolicy` ein **erstrangiger
> Parameter** — kein nachgeordneter. Er ist orthogonal zu `domain`, `archetype`
> und `epoch_band`. Der `SettlementBuilder` darf ihn nicht aus dem `archetype`
> ableiten, sondern muss ihn aus dem Kontext setzen.

---

## 1. Kernbefund: Drei strukturell verschiedene Wissensräume

Das mittelalterliche Bauwesen war keine einheitliche Wissenssphäre. Es
existierten drei strukturell verschiedene Organisationsformen, die denselben
Bautyp unter radikal unterschiedlichen Wissensbedingungen herstellten.

Diese Tatsache ist nicht stilistisch. Sie ist konstruktiv.

Gleiche Epoche, gleiche Region, gleicher Werkstoff, gleiche Bauaufgabe:
Die strukturelle Plausibilität des Ergebnisses hängt davon ab, welcher
Wissensinfrastruktur der Bau entstammte. Ein Klosterbau von 1350 und ein
bäuerliches Hallenhaus von 1350 teilen Materialparameter — aber nicht
Querschnittsdimensionen, nicht Verbindungstypologie, nicht
Innovationsgeschwindigkeit.[^binding2014-kernbefund]

---

## 2. Das Dreistufenmodell (HRR)

### 2.1 Tier 1 — Bauhütte (Monumental- und Klerikalbauten)

#### Organisation

Die Bauhütten waren projektgebundene Werkstattverbände für den Bau gotischer
Kathedralen, Kloster- und Stiftskirchen. Zur Hütte gehörten Werkmeister und
Handwerker verschiedener Gewerke: Steinmetze, Maurer, Zimmerleute, Schmiede,
Glaser. Die Steinmetzbruderschaft bildete eine überregionale Organisationsform,
die sich von städtischen Zünften strukturell unterschied — projektbezogen
und bauübergreifend vernetzt.[^binding1997-huette]

#### Wissensinfrastruktur

Der Werkmeister verfügte über Zugang zu geometrischem Spezialwissen —
**Triangulatur und Quadratur** — als konstruktivem Entwurfswerkzeug. Seit
dem 13. Jahrhundert entstanden Risszeichnungen als Planungsinstrument.

Villard de Honnecourts Bauhüttenbuch (um 1230–1235) belegt überregionalen
Wissensaustausch als systematische Praxis: Kopien von Grundrissdaten aus
Chartres, Reims, Laon und Lausanne.[^villard]

Die Werkmeisterbücher des 15./16. Jahrhunderts (Roritzer 1486,
Schmuttermayer ca. 1487, Lechler 1516) zeigen das Entwurfssystem: Alle
Abmessungen stehen in definierten proportionalen Relationen zur
Grundmaßeinheit.[^werkmeisterbuecher]

**Fundamentaler Befund zur Alphabetisierung:**

> „Für den Werkmeister, der allgemein nicht lesen und schreiben konnte,
> war der Anteil geistiger Impulse durch den zumeist theologisch gebildeten
> Bauherrn besonders groß."[^binding2014-analphabet]

Das Wissen war visuell-körperlich, nicht literarisch. Selbst der Werkmeister
der Großbauhütte war Analphabet — sein Aktionsradius (mehrere Kathedralprojekte,
supraregionale Wanderungen) war dennoch von einer anderen Größenordnung als
jede städtische Zunft.

#### Konstruktive Konsequenzen

- Geringere Überdimensionierung: schlankere Querschnitte trotz größerer Spannweiten.
- Komplexe Verbindungen: frühe Adoption von Zapfenverbindungen.
- Strukturell riskantere Entscheidungen, gedeckt durch spezialisiertes
  Erfahrungswissen und explizite geometrische Planung.

Gotische Gewölbehöhen als Risikoindikator:

| Kathedrale | Baujahr | Höhe Mittelschiff |
|---|---|---|
| Laon | 1155 | 24,0 m |
| Amiens | 1220 | 42,3 m |
| Beauvais | 1255 | 48,0 m |

Der Chor von Beauvais stürzte 1284 ein — nicht wegen der Höhe, sondern
wegen zu großer Arkadespannweite. Das ist kein Versagen der Wissensinfrastruktur,
sondern ihr Betrieb an der Grenze des Möglichen.[^beauvais]

---

### 2.2 Tier 2 — Zimmererzunft (Städtischer und bürgerlicher Profanbau)

#### Organisation

Mit der Entstehung der Zünfte im Hochmittelalter — ab dem 12. Jahrhundert —
entstand der Zimmermann als eigentlicher Berufsstand. Die Zunft regulierte
Ausbildung, Qualität, Lohn und Niederlassungsrecht. Sie war **lokal**,
nicht überregional. Lehrlinge wohnten 3–7 Jahre im Haus des Meisters,
absolvierten eine Gesellenprüfung und begaben sich auf Wanderschaft.[^schulz2010]

#### Wissensinfrastruktur

Der Zimmermeister kannte handwerkliche Faustregeln, regionale
Konstruktionsnormen und das Abbinden auf dem **Zimmerboden** (Reißboden).
Er verfügte über keinen Zugang zu den Werkmeisterbüchern oder dem
geometrischen Proportionswissen der Bauhütten.

Das Verhältnis zwischen Hütte und Zunft war allgemein kooperativ: der
Werkmeister der Hütte wurde gelegentlich als Sachverständiger bei
städtischen Bauaufgaben herangezogen. Das ist der Kanal, über den
Bauhüttenwissen sporadisch in den Profanbau einfloss:
**episodisch, nicht institutionalisiert**.[^binding1997-kooperation]

**Historiographische Kontroverse**: Epstein (1998) sieht Zünfte primär als
Innovationsermöglicher durch institutionalisierten Wissenstransfer via
Gesellenwanderschaft. Ogilvie (2019) sieht sie primär als Rent-Seeking-
Kartelle. Der empirische Befund zeigt breite Variation: Export-orientierte
Zünfte in Handelszentren zeigten mehr Offenheit als lokale Monopolisten.[^zunft-kontroverse]

#### Konstruktive Konsequenzen

- Professionelle Qualität innerhalb lokaler Normen.
- Mittlere Überdimensionierung entsprechend Zunftnorm.
- Prestigebauten (Rathäuser, Zunfthäuser, städtische Kirchen) mit anderen
  Wissensvoraussetzungen als Kathedralbau.

---

### 2.3 Tier 3 — Volkshandwerk (Ländlicher und bäuerlicher Bau)

#### Organisation

Das bäuerliche Bauen war kein Beruf. Es war **Gemeinschaftsarbeit**. Kein
Werkmeister, keine Zunft, kein Lehrvertrag. Das Wissen lebte kollektiv
in der Dorfgemeinschaft und wurde durch Beobachtung, Teilnahme und
generationelle Weitergabe reproduziert.

Der **Quellenbias** ist strukturell bedingt: Kein Volkshandwerk produzierte
Baurechnungen, Chroniken oder Werkmeisterbücher. Das erste
dendrochronologisch datierte bäuerliche Gebäude Bayerns vor 1500 wurde
erst 1980 entdeckt (1367, Höfstetten, Fränkisches Freilandmuseum Bad
Windsheim).[^bedal-1367]

> [!NOTE]
> Der Quellenbias gilt für alle drei Stufen — aber er ist für Tier 3 am
> stärksten. Die Forschungslage ist nicht gleichmäßig: Tier 1 ist durch
> Chroniken, Baurechnungen und Werkmeisterbücher gut belegt. Tier 3 durch
> ausschließlich physische Baubestände, und nur soweit sie erhalten sind.

#### Wissensinfrastruktur

Das konstruktive Wissen war ausschließlich **lokal**. Tradierte Maßverhältnisse
aus dem kollektiven Gedächtnis. Kein geometrisches Proportionswissen. Kein
Reißboden-Aufriss. Keine institutionalisierte Wanderschaft.

Die **Konservativität war maximal**: Abweichung vom Bekannten bedeutete
Risiko ohne jedes institutionelles Sicherheitsnetz. Diese Konservativität
war keine Dummheit — sie war rational unter den gegebenen Wissensbedingungen.[^bedal-konservativ]

#### Konstruktive Konsequenzen

- Höchste Überdimensionierungsfaktoren aller drei Gruppen.
- Einfachste Verbindungen: Verblattungen dominant.
- Stärkste regionale Differenzierung: Jedes Tal entwickelte über Generationen
  eigene Lösungen ohne Kontakt nach außen.
- Langsamste Innovationsadoption: Generationenzeitraum statt Jahrzehnte.[^klein2012]

---

## 3. Strukturvergleich der drei Wissensstufen

<a name="tier-comparison-table"></a>

| Merkmal | Tier 1 — Bauhütte | Tier 2 — Zunft | Tier 3 — Volkshandwerk |
|---|---|---|---|
| **Organisation** | Projektgebundene Werkstattverbände | Lokale Berufsorganisation | Gemeinschaftsarbeit, kein Berufsstand |
| **Ausbildungsweg** | Wanderung über mehrere Baustellen | Lehrzeit 3–7 J., Wanderschaft | Beobachtung, mündliche Weitergabe |
| **Aktionsradius** | Supraregional | Lokal bis regional | Lokal (Tal, Dorf) |
| **Geometriewissen** | Triangulatur, Quadratur, Proportionssysteme | Faustregeln, Zimmerbodenaufriss | Tradierte Maßverhältnisse |
| **Planungsinstrument** | Risszeichnung (ab 13. Jh.) | Reißboden, Abbundzeichen | Keins (mental) |
| **Alphabetisierung** | Werkmeister: Analphabet | Meister: teils alphabetisiert | Nicht relevant |
| **Innovationsrate** | Hoch (Jahrzehnte) | Mittel (Generationen) | Sehr gering (konservativ) |
| `overdimension_factor` | Niedrig | Mittel | Hoch |
| `joint_complexity_level` | Hoch (Zapfen, Schwalbe) | Mittel | Niedrig (Blatt dominant) |
| `regional_isolation_factor` | Sehr niedrig | Mittel | Sehr hoch |

---

## 4. Wissenstransfer zwischen den Stufen

Der Transfer zwischen den drei Stufen war real, aber **niemals systematisch**.
Er war episodisch, personen- und ortsbezogen, und extrem langsam.

**Tier 1 → Tier 2**: Episodisch, nicht institutionalisiert. Werkmeister
als gelegentlicher Sachverständiger bei städtischen Bauaufgaben. Städtische
Zunfthandwerker beobachteten Bauhüttenbaustellen, ohne die geometrischen
Planungsprinzipien zu erlernen.[^binding1997-transfer]

**Tier 2 → Tier 3**: Minimal. Das Zunftsystem lebte von Wissensabgrenzung
als Marktschutz. Diffusion allenfalls durch Migration, Beobachtung über
Generationen, oder Städtenähe.

**Diffusionsgeschwindigkeit empirisch**: Dendrochronologische Studien
zeigen, dass konstruktive Neuerungen 50–100 Jahre benötigten, um aus dem
urbanen Zunfthandwerk in das ländliche Volkshandwerk überzugehen.
Topographisch (Flusstäler vs. abgelegene Täler) variiert dieser Zeitraum
erheblich.[^diffusion-zeit]

**Tier 1 → Tier 3**: Praktisch inexistent. Die soziale, institutionelle
und räumliche Distanz war zu groß.[^tier1-tier3]

> [!NOTE]
> Die Diffusionsgeschwindigkeit ist räumlich messbar: Konstruktive
> Innovationen verbreiteten sich entlang von Wanderrouten — Handelswegen,
> Flusstälern, Pilgerrouten. Die Diffusionskarte einer Verbindungsneuerung
> spiegelt die Mobilitätsmuster ihrer Träger.

---

## 5. Wissenstransmission: Mechanismen ohne Schrift

Alle drei Stufen teilten ein Grundmerkmal: Das Kernwissen war **nicht
schriftlich kodiert**. Selbst die Werkmeisterbücher des Tier 1 beschreiben
geometrische Verfahren, die nur durch körperliches Üben erlernbar sind —
die Bücher sind Gedächtnisstützen, keine Lehrbücher.

### 5.1 Abbundzeichen

Abbundzeichen sind eingemeißelte oder eingeritzte Markierungen an
vorgefertigten Bauteilen, die während des Abbunds auf dem Reißboden
die Montagezuordnung codieren. Sie sind **operative Sprache** des
Abbundprozesses, keine individuellen Markenzeichen.[^abbundzeichen]

> [!NOTE]
> **BVILLAGE-Relevanz**: Abbundzeichen sind kein Stilmerkmal. Sie sind ein
> Hinweis auf den Produktionsprozess. Ihre Systematik korreliert mit dem
> `knowledge_infrastructure_tier`.

### 5.2 Geometrie ohne Schrift: Triangulatur und Quadratur

Roritzers „Büchlein von der Fialen Gerechtigkeit" (1486): Aus einem
Grundquadrat werden alle weiteren Maße durch sequentielle Quadratur
abgeleitet. Das Verfahren erfordert kein Rechnen — aber jahrelange Übung.[^roritzer]

### 5.3 Körperwissen und Wanderschaft

Da das Wissen personal und körperlich war, war die Person die
Wissenseinheit. Wanderschaft war der **primäre Mechanismus der
Wissensausbreitung** in einer nicht-schriftlichen Handwerkskultur:

- Tier 1: supraregionale Wanderung über mehrere Länder.
- Tier 2: regionale Wanderschaft, locker institutionalisiert.
- Tier 3: keine Wanderschaft, lokale Transmission.

---

## 6. Regionale Wissensinfrastrukturen: Gesamteuropa

Das HRR-Dreistufenmodell ist ein heuristisches Instrument, kein
Universalmodell. Andere Regionen haben eigene Wissensinfrastrukturen
entwickelt, die in einigen Punkten parallel laufen, in anderen fundamental
abweichen.

### 6.1 England: Masons' Company und Carpenters' Company

England entwickelt parallel zum HRR-Zunftsystem eigene Gildensysteme
mit charakteristischen Unterschieden:

**Masons' Company (London, Gründung 13. Jh.)**: Königliche Charter sichert
das Monopol auf Steinmetzarbeiten in London. Struktur ähnelt HRR-Zunft:
Lehrzeit, Meisterstück, territorialer Marktschutz. Zusätzlich existiert
der englische Freemason-Verbund als überregionale Netzwerkstruktur parallel
zur städtischen Gilde — dem HRR-Bauhütten-Verbund ähnlich, aber ohne die
Dombauhütte als Kern.[^england-masons]

**Carpenters' Company (London, Gründung 1333, Royal Charter 1477)**:
Zunftorganisation für Zimmerleute. Der englische Zimmermann ist
Tier-2-Handwerker im HRR-Sinne, aber mit stärkerer Kronkontrolle
und weniger Stadtautonomie.[^england-carpenters]

**Wissensinfrastruktur-Differenz**: Der englische *vernacular carpenter*
hat oft Tier-2-Qualität bei Tier-3-Organisation — weil er häufiger als
selbständiger Handwerker für Freeholder arbeitet, nicht nur in
Dorfgemeinschaft.

> [!IMPORTANT]
> Für England verläuft die Grenze Tier 2 / Tier 3 anders als im HRR.
> `knowledge_infrastructure_tier` für englischen ländlichen Zimmermann:
> zwischen `urban_guild` und `vernacular`, nicht eindeutig zuzuordnen.
> Die Mapping-Funktion muss das als Kontinuum behandeln.

### 6.2 Skandinavien: Mündliche Wissenstradition der Stabkirchenerbauer

Die norwegischen Stabkirchen (ca. 9.–13. Jahrhundert, ursprünglich
geschätzt 1000–2000 Bauten, ~28 erhalten) sind das technologisch
anspruchsvollste Holzbausystem des mittelalterlichen Europa — und
entstehen ohne Zunftstruktur und ohne dokumentierte Werkmeisterbücher.[^stabkirchen-bestand]

**Wissensinfrastruktur**: Hochspezialisierte mündliche Wissenstradition
über Meister-Lehrlings-Weitergabe. Kein institutioneller Rahmen, aber:
- Komplexe Verbindungssysteme (Nut-Feder, Schwalbenschwanz)
- Strukturelle Risikobereitschaft (freistehende Säulen, Mehrgeschossigkeit)
- Supraregionale Standardisierung trotz fehlender Institution

Das widerspricht der HRR-Logik: Im HRR erzeugt fehlende Institution →
Tier 3 → Überdimensionierung und einfache Verbindungen. In Norwegen
vor 1250 erzeugt fehlende Institution → komplexe Verbindungen und
durchdachte Statik.[^stabkirchen-paradox]

**Erklärung**: Die freie Bauerngesellschaft (*Bonde*) mit eigenem
Rechtstatus und eigenem Kapital erzeugt eine spezifisch skandinavische
Wissensinfrastruktur: persönliche Meisterschaft ohne Zunft oder Bauhütte,
aber weit über Tier 3 hinausgehend.

> [!IMPORTANT]
> Für skandinavischen Kontext vor ca. 1250 ist ein vierter Wert nötig:
>
> ```
> knowledge_infrastructure_tier: oral_master_tradition
> ```
>
> `oral_master_tradition` hat `overdimension_factor`-Werte von Tier 2
> (niedrig bis mittel), `regional_isolation_factor`-Werte von Tier 3 (hoch),
> und `joint_complexity_level` hoch wie Tier 1.

### 6.3 Islamische Bauwissenstradition (Al-Andalus)

**Muhandis (مهندس)** — Islamischer Baumeister: Abgeleitet von *handasa*
(Geometrie). Ein spezialisierter Planender mit geometrisch-mathematischem
Ausbildungsweg. Der *muhandis* ist kein Handwerker — er ist Wissenschaftler
und Planer im Dienst des Herrschers oder des Waqf-Stiftungssystems.[^muhandis]

Der islamische Wissenstransfer hat eine schriftliche Basis, die der HRR-
Tradition fehlt: arabische Geometrie- und Architekturtraktate kodieren
geometrisches Bauwissen in verschriftlichter Form. Das ist ein fundamentaler
Unterschied zu Roritzers Werkmeisterbüchern — islamische Architekturtraktate
*schreiben* die Geometrie, HRR-Werkmeisterbücher *zeigen* sie ohne Text.[^islamische-traktate]

**Geometrische Ornamentalität**: Die islamische geometrische Ornamentik
(Girih-Muster, Muqarnas-Gewölbe) setzt planare Geometrie voraus, die
über HRR-Tier-1 in dieser Spezifik hinausgeht. Muqarnas-Gewölbe sind
ohne trigonometrische Grundkenntnisse nicht konstruierbar.[^muqarnas]

> [!IMPORTANT]
> Für Al-Andalus-Erweiterung:
>
> ```
> knowledge_infrastructure_tier: islamic_learned_tradition
> ```
>
> Charakteristika: hohe schriftliche Wissenskomponente, mathematisch-geometrische
> Basis, Trennung von Planung (muhandis) und Ausführung (ustā'), spezifische
> Ornamentgrammatik.

### 6.4 Byzantinisches Kaiserbauamt

**Kaiserliche Architekten** (*architekton*): Gebildete Professionelle —
oft mit Philosophiestudium und mathematischer Ausbildung. Isidoros von
Milet und Anthemios von Tralleis (Erbauer der Hagia Sophia, 532–537)
waren beide Mathematiker und Mechaniker, keine Handwerker.[^hagia-sophia]

**Wissensinfrastruktur**: Archimedes, Euklid, Heron von Alexandria sind
byzantinischen Architekten bekannt und werden aktiv genutzt. Akademische
Bildungstradition, die HRR-Tier-1 weit übersteigt.

**Provinzieller Bereich**: Außerhalb Konstantinopels bricht diese Tradition
schnell ab. Der Abstand zwischen Hauptstadt und Provinz ist im byzantinischen
Reich größer als im HRR.[^byzanz-provinz]

> [!IMPORTANT]
> Byzantinische Großbauten: `knowledge_infrastructure_tier: imperial_academic`
>
> Byzantinische Provinzbauten: `knowledge_infrastructure_tier: urban_guild`
> (näherungsweise — der byzantinische Provinzhandwerker hat keine vollständige
> HRR-Zunft-Entsprechung, aber die Parameter sind die nächste Annäherung)

---

## 7. Epochale Entwicklung der Wissensinfrastruktur

### Phase 1 — Frühphase (ca. 1150–1250)

Zunftsystem im Entstehen. Bauhütte voll aktiv (Hochgotik). Volkshandwerk
dominant im ländlichen Bereich. `knowledge_infrastructure_tier` = stark
polarisiert (monumental vs. vernacular, urban_guild als schwache Mittelstufe).

### Phase 2 — Hochphase der Zunft (ca. 1250–1347)

Die Zunft festigt sich. Profanbau der Mittelstädte professionalisiert sich.
Drei klare Stufen, mittlere Stufe gestärkt.[^zunft-hochphase]

### Phase 3 — Pestschock und Nachwirkung (1347–ca. 1430)

**BRUCH** — vgl. MEDIEVAL_07_EPOCHS_AND_BREAKS.md, Abschnitt 3.

Direkte Folgen:
- **Tier 1**: Projekte werden unterbrochen. Meistersterblichkeit = potenzieller
  Wissensverlust.
- **Tier 2**: Institution überlebt rechtlich, verliert aber Mitglieder.
  Paradoxer Rekonstruktionsboom erhöht Druck.
- **Tier 3**: Am wenigsten institutionell geschützt, aber kollektiv gepuffert.
  Ein ganzes Dorf kann aussterben.

**Regionaler Vergleich**: In Skandinavien und Al-Andalus ist der Pestschock
geringer → `knowledge_infrastructure_tier`-Disruption geringer.[^pest-regional]

> [!WARNING]
> **Offene Forschungsfrage F3**: Wie viel spezialisiertes Handwerkswissen ging
> durch Meistersterblichkeit real verloren? In der Literatur nicht quantifiziert.
> Der `epoch_band_modifier` für Pestübergang bleibt schwach belegt. Alle
> Tier-Werte für diesen Zeitraum sind Analogieschlüsse, keine Messwerte.

### Phase 4 — Stabilisierung und Werkmeisterbücher (ca. 1430–1520)

Werkmeisterbücher entstehen als Externalisierung von Tier-1-Wissen nach dem
Pestschock (Roritzer 1486, Schmuttermayer ca. 1487, Lechler 1516).
Übergang vom Ständerbau zum Stockwerksbau als Zunftinnovation, die langsam
ins Volkshandwerk diffundiert.[^werkmeisterbuecher-phase4]

### Phase 5 — Reformation und Typenstabilisierung (ca. 1520–1618)

Tier 1 verliert institutionelle Basis in protestantischen Gebieten.
Bauhütten-Zimmerleute treten in städtische Zünfte ein. Abstand
Tier 1 / Tier 2 verringert sich. Tier 3 bleibt unberührt.

---

## 8. BVILLAGE-Implikationen

### 8.1 Vollständige Werteliste knowledge_infrastructure_tier

```
knowledge_infrastructure_tier:
  monumental                  # HRR Bauhütte
  urban_guild                 # HRR Zunft, England Gilde, Byzanz Provinz
  vernacular                  # HRR Volkshandwerk, ländliches Europa
  oral_master_tradition       # Skandinavien vor ca. 1250
  islamic_learned_tradition   # Al-Andalus muhandis-System
  imperial_academic           # Konstantinopel Großbau
```

### 8.2 Parameter-Mapping nach tier

| BVILLAGE-Parameter | monumental | urban_guild | vernacular | oral_master | islamic |
|---|---|---|---|---|---|
| `overdimension_factor` | Niedrig | Mittel | Hoch | Mittel | Niedrig |
| `joint_complexity_level` | Hoch | Mittel | Niedrig | Hoch | Sehr hoch |
| `section_slenderness_tolerance` | Hoch | Mittel | Niedrig | Mittel | Mittel |
| `regional_isolation_factor` | Sehr niedrig | Mittel | Sehr hoch | Hoch | Mittel |
| `innovation_adoption_rate` | Jahrzehnte | Generationen | Generationen konservativ | Langsam | Schriftbasiert |
| `brace_typology_weight` | Zapfen dominant | Gemischt | Blatt dominant | Zapfen | Geometrisch |

> [!IMPORTANT]
> Der `PhysicalPlausibilityValidator` darf **keine** einheitliche
> Toleranzband-Definition für ein Jahrhundertband verwenden.
>
> Beispiel: Ein Querschnitt von 12×12 cm für einen Hauptständer ist für
> `vernacular` (1350) plausibel. Für `monumental` (1350) ist er
> unwahrscheinlich schlank — ohne dass sich das Material geändert hätte.
> Die Validierung muss `knowledge_infrastructure_tier` als Eingabeparameter
> kennen.

### 8.3 Epochale Schocks: epoch_band_modifier bei Pestübergang

| tier | `joint_complexity_level` | `innovation_adoption_rate` | `regional_isolation_factor` |
|---|---|---|---|
| `monumental` | kurzfristig ↓ | — | — |
| `urban_guild` | — | kurzfristig ↑ (Vereinfachung) | — |
| `vernacular` | — | — | kurzfristig ↑ (Dorfverluste) |
| `oral_master_tradition` | geringere Disruption | — | — |
| `islamic_learned_tradition` | geringste Disruption | — | — |

> [!WARNING]
> Alle Werte in dieser Tabelle sind Analogieschlüsse. Nicht direkt quantifiziert
> in der Literatur. Evidenzgrad: [SCHWACH].

---

## 9. Primärquellen

**Villard de Honnecourt**: Bauhüttenbuch. Paris, BnF, Ms. fr. 19093.
Um 1230–1235. *Direkte Evidenz für supraregionalen Wissensaustausch im Tier 1.*

**Matthäus Roritzer**: Büchlein von der Fialen Gerechtigkeit. Regensburg 1486.
*Erstes gedrucktes deutsches Werkmeisterbuch.*

**Matthäus Roritzer**: Geometria Deutsch. Regensburg 1487/88.

**Hans Schmuttermayer**: Fialenbüchlein. Nürnberg, um 1487.

**Lorenz Lechler**: Unterweisungen. 1516.
*In drei Handschriften erhalten: Köln, Heidelberg, Karlsruhe.*

**al-Khwarizmi**: Kitāb al-mukhtaṣar fī ḥisāb al-jabr. ca. 820.
*Mathematische Grundlage der islamischen Baugeometrie.*

**Ibn Khaldun**: Muqaddima. ca. 1377.
*Abschnitte über Bauwissen und Handwerkerorganisation.*

**Prokopios von Caesarea**: De Aedificiis. ca. 554 n.Chr.
*Beschreibt Hagia-Sophia-Bau; überliefert Isidoros und Anthemios.*

---

## 10. Offene Forschungsfragen für BVILLAGE

> [!WARNING]
> **F1 — Quantifizierung des overdimension_factor nach Wissensstufe:**
> Ljungqvist et al. (2022: 54.045 Fälle) könnten das beantworten — aber
> Daten müssten nach Bauherrntyp klassifiziert werden. Derzeit sind
> `overdimension_factor`-Werte Expertenschätzungen, keine Messgrößen.

> [!WARNING]
> **F2 — Diffusionsgeschwindigkeit regional quantifizieren:**
> Meeson (2012) gibt für England ca. 50–100 Jahre an (Tier 2 → Tier 3).
> Für den deutschen Sprachraum fehlt eine vergleichbare Studie.
> `innovation_adoption_rate` für Tier 3 hat hohe Unsicherheit.

> [!WARNING]
> **F3 — Pestschock und Wissensverlust:**
> Wie viel spezialisiertes Handwerkswissen ging durch Meistersterblichkeit
> real verloren? Nicht quantifiziert. BVILLAGE könnte durch explizite
> Modellierung einen originären Forschungsbeitrag leisten.

> [!WARNING]
> **F4 — Alphabetisierung und Wissensexternalisierung:**
> Wann begann die Alphabetisierung von Zimmermeistern (Tier 2) zu steigen,
> und wie veränderte das die Wissensinfrastruktur? Der Übergang zwischen
> mittelalterlichem und frühneuzeitlichem Wissensregime liegt im Unklaren.

> [!WARNING]
> **F5 — Islamische Wissenstradition und BVILLAGE-Parametrisierung:**
> Wie lässt sich die muhandis-Tradition in BVILLAGE-kompatible Parameter
> übersetzen? Dodds (1990), Milwright (2010) als Ausgangspunkte.

> [!WARNING]
> **F6 — Oral master tradition: Skandinavische Quantifizierung:**
> Wie unterscheiden sich Querschnittsdimensionen skandinavischer Stabkirchen
> von HRR-Tier-3-Gebäuden gleicher Größenordnung?

---

## 11. Quellen

**Anker, Leif:** The Norwegian Stave Churches. Oslo: Arfo, 1997. [HART]

**Bedal, Konrad / Historisches Lexikon Bayerns:** Bauernhäuser (Spätmittelalter).
historisches-lexikon-bayerns.de. [MITTEL]

**Binding, Günther:** Baubetrieb im Mittelalter. Darmstadt: WBG, 1997. [MITTEL/HART]

**Binding, Günther:** Bauwissen im Früh- und Hochmittelalter. In: Renn et al.
(Hg.): Wissensgeschichte der Architektur. MPRL Studies 5/3. Berlin 2014. [HART]

**Constable, Olivia Remie:** Trade and Traders in Muslim Spain.
Cambridge: CUP, 1994. [MITTEL]

**Dodds, Jerrilynn D.:** Architecture and Ideology in Early Medieval Spain.
University Park: Penn State UP, 1990. [MITTEL]

**Eißing, Thomas et al.:** Vorindustrieller Holzbau. Heidelberg: Propylaeum, 2023.
DOI: https://doi.org/10.11588/sbhbf.2023.1.99050 [HART]

**Epstein, Stephan R.:** Craft Guilds, Apprenticeship, and Technological Change.
Journal of Economic History 58 (1998), 684–713. [MITTEL]

**Haldon, John F.:** Byzantium in the Seventh Century. Cambridge: CUP, 1990. [MITTEL]

**Harvey, John H.:** The Medieval Architect. London: Wayland, 1972. [MITTEL]

**Klein, Ulrich:** Zum aktuellen Forschungsstand des Holzbaus in Deutschland.
DGAMN-Mitteilungen Bd. 24. Paderborn 2012.
DOI: https://doi.org/10.11588/dgamn.2012.1.17131 [MITTEL]

**Ljungqvist, Fredrik C. et al.:** Regional patterns of late medieval and
early modern European building activity.
Frontiers in Ecology and Evolution 10 (2022). [MITTEL]

**Mainstone, Rowland J.:** Hagia Sophia. London: Thames & Hudson, 1988. [HART]

**Meeson, Bob:** Structural Trends in English Medieval Buildings.
Vernacular Architecture 43 (2012), 58–75. [MITTEL]

**Milwright, Marcus:** An Introduction to Islamic Archaeology.
Edinburgh: Edinburgh UP, 2010. [MITTEL]

**Ogilvie, Sheilagh:** The European Guilds: An Economic Analysis.
Princeton: Princeton UP, 2019. [MITTEL]

**Salzman, Louis F.:** Building in England Down to 1540.
Oxford: Clarendon Press, 1952. [HART]

**Schulz, Knut:** Handwerk, Zünfte und Gewerbe. Darmstadt: WBG, 2010. [MITTEL]

**Shelby, Lon R. (ed.):** Gothic Design Techniques. Southern Illinois UP, 1977. [HART]

**Thue, Lars:** Norsk Bygningsleksikon. Oslo: Gyldendal, 2012. [HART]

---

<!-- FOOTNOTES -->

[^binding2014-kernbefund]: Binding: Bauwissen im Früh- und Hochmittelalter, MPRL Studies 5/3, 2014. Direkt belegbar durch datierte Baubestände. [HART]

[^binding1997-huette]: Binding: Baubetrieb im Mittelalter, 1997. Durch zeitgenössische Hüttenbücher und Bauurkunden belegt. [HART]

[^villard]: Villard de Honnecourt: Bauhüttenbuch, Paris BnF Ms. fr. 19093, um 1230–1235. Direkte Evidenz für supraregionalen Wissensaustausch. [HART]

[^werkmeisterbuecher]: Roritzer 1486; Schmuttermayer ca. 1487; Lechler 1516. Hüttenspezifisches Wissen, nicht für allgemeinen Handwerksbetrieb bestimmt. [HART]

[^binding2014-analphabet]: Binding: Bauwissen im Früh- und Hochmittelalter, MPRL Studies 5/3, 2014. Das Wissen war visuell-körperlich, nicht literarisch — belegt durch Werkmeisterbücher, die Geometrie ohne Textbeschreibung vermitteln. [HART]

[^beauvais]: Bauarchäologisch dokumentiert. Einsturz 1284 wegen zu großer Arkadespannweite, nicht wegen Gewölbehöhe. [HART]

[^schulz2010]: Schulz: Handwerk, Zünfte und Gewerbe, 2010. [MITTEL]

[^binding1997-kooperation]: Binding: Baubetrieb im Mittelalter, 1997. Durch Baustellenrechnungen einzelner Kathedralen belegt. [MITTEL]

[^zunft-kontroverse]: Epstein: Journal of Economic History 58 (1998). Ogilvie: The European Guilds, 2019. Prak, De Munck, Wallis 2008–2016. Forschungsdebatte unabgeschlossen. [MITTEL]

[^bedal-1367]: Bedal / Freilandmuseum Bad Windsheim. Publizierte Datierung. [HART]

[^bedal-konservativ]: Bedal im Historischen Lexikon Bayerns. Inhaltlicher Konsens. [MITTEL]

[^klein2012]: Klein: DGAMN-Mitteilungen Bd. 24, 2012. Durch Baubestandsanalysen bestätigt. [MITTEL]

[^binding1997-transfer]: Binding: Baubetrieb im Mittelalter, 1997. [MITTEL]

[^diffusion-zeit]: Meeson: Vernacular Architecture 43 (2012) für England. Ljungqvist et al.: Frontiers in Ecology and Evolution 10 (2022) für Kontinentaleuropa. Keine direkte Messung für deutschen Sprachraum. [MITTEL]

[^tier1-tier3]: Schluss aus strukturellen Bedingungen; nicht direkt belegt. [MITTEL]

[^abbundzeichen]: Eißing et al.: Vorindustrieller Holzbau, 2023. Klein: DGAMN-Mitteilungen, 2012. Durch hunderte datierte Fachwerkgebäude direkt nachweisbar. [HART]

[^roritzer]: Roritzer: Büchlein von der Fialen Gerechtigkeit, 1486. Faksimile-Ausgabe Shelby 1977. [HART]

[^england-masons]: Salzman: Building in England Down to 1540, 1952. Harvey: The Medieval Architect, 1972. [MITTEL]

[^england-carpenters]: Salzman: Building in England Down to 1540, 1952. [MITTEL]

[^stabkirchen-bestand]: Anker: The Norwegian Stave Churches, 1997. Thue: Norsk Bygningsleksikon, 2012. [HART]

[^stabkirchen-paradox]: Anker 1997; Thue 2012. Widerspruch zur HRR-Logik bisher nicht systematisch untersucht. [HART für Bestand; MITTEL für Interpretation]

[^muhandis]: Dodds: Architecture and Ideology, 1990. Constable: Trade and Traders in Muslim Spain, 1994. [MITTEL]

[^islamische-traktate]: Milwright: An Introduction to Islamic Archaeology, 2010. al-Khwarizmi ca. 820; Ibn Khaldun ca. 1377 als Primärquellen. [MITTEL]

[^muqarnas]: Für Bestand: erhaltene Gebäude in Granada, Córdoba, Sevilla. Für Wissensinfrastruktur: Milwright 2010. [HART für Bestand; MITTEL für Wissensinfrastruktur]

[^hagia-sophia]: Mainstone: Hagia Sophia, 1988. Prokopios: De Aedificiis, ca. 554 n.Chr. [HART]

[^byzanz-provinz]: Haldon: Byzantium in the Seventh Century, 1990. [MITTEL]

[^zunft-hochphase]: Binding: Baubetrieb im Mittelalter, 1997. Zunftquellen des 13./14. Jh. [MITTEL]

[^pest-regional]: Analogieschluss aus Pestmortalitätsdaten. Mortalität MITTEL belegt; Wirkung auf Wissensinfrastruktur SCHWACH. [SCHWACH]

[^werkmeisterbuecher-phase4]: Coenen: Die spätgotischen Werkmeisterbücher, 1990. Eißing et al. 2023. [MITTEL]

---

*BVILLAGE Research Foundation — Achse 5 — v2.1*
