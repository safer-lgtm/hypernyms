# hypernyms

## Forschung und Entwicklungsprojekt
### **Titel**: *Rekonstruktion von Hypernym-Taxonomien mittels LLMs im Vergleich zu menschlichen linguistischen Wortnetzen*

### **Autor**: *Safouan Er-Ryfy*

### Projektziel
> Das Ziel dieses Projekts ist es, Hypernym-Taxonomien mithilfe von Large Language Models (LLMs) – insbesondere LLaMA 3.1 – zu rekonstruieren. Die dabei automatisch generierten Taxonomien werden mit linguistischen Wortnetzen wie GermaNet verglichen. Als Grundlage dienen Begriffe aus dem deutschsprachigen E-Mail-Korpus CodEAlltag.
Die zentrale Fragestellung lautet:   
Können LLMs wie LLaMA 3.1 bessere oder gleichwertige Hypernym-Taxonomien liefern wie klassische Wortnetze?

### Quantitativer Vergleich mit GermaNet

> Die GermaNet-API ([GitHub](https://github.com/Germanet-sfs/germanetpy)) ermöglicht den Zugriff auf das deutsche WordNet, in dem Nomen, Verben und Adjektive semantisch miteinander verknüpft sind. Bedeutungsähnliche Wörter werden in sogenannten *Synsets* gruppiert und über verschiedene Relationen miteinander verbunden.
Zur Bewertung der generierten Hypernyme wird ein Vergleich mit den Einträgen aus GermaNet durchgeführt. So kann eingeschätzt werden, wie gut das Sprachmodell im Vergleich zu einer linguistisch kuratierten Ressource abschneidet.
Für die Nutzung von GermaNet ist eine *Lizenz* erforderlich, die über die [Lizenzseite der Universität Tübingen](https://uni-tuebingen.de/fakultaeten/philosophische-fakultaet/fachbereiche/neuphilologie/seminar-fuer-sprachwissenschaft/arbeitsbereiche/allg-sprachwissenschaft-computerlinguistik/ressourcen/lexica/germanet-1/lizenzen/) beantragt werden kann. Nach Erhalt der Zugangsdaten können die Inhalte aus *`GN_V190_XML`* beispielsweise in den *`data/`*-Ordner eines Google-Colab-Projekts hochgeladen werden.
Anschließend lässt sich GermaNet wie folgt laden:
```bash
# Laden der GermaNet- Daten
germanet = Germanet("data/") # Pfad zu den entpackten XML-Dateien
```

> Um die Hypernymsketten aus GermaNet zu holen wird zunächst der *Breadth-First Search* (BFS) Algorithmus eingesetzt, ein Verfahren zur ebenenweisen Durchsuchung von Knoten. Dabei wird eine Warteschlange (*Queue*) verwendet, um Begriffe zunächst auf derselben Ebene zu verarbeiten, bevor in höhere Ebenen übergegangen wird. In diesem Projekt wird BFS eingesetzt, um alle Synsets eines Wortes sowie deren übergeordnete Hypernyme systematisch zu erfassen. Eine anschauliche Einführung bietet dieser [Blogartikel](https://medium.com/@tahsinsoyakk/breadth-first-search-bfs-a-comprehensive-guide-4672bbc5e48c).


#### Auswertung von LLaMA-Hyponymen
![grafik](https://github.com/user-attachments/assets/d1dcc484-04ae-414d-9838-baa0b870eb4e)


Die Kategorisierung der vom LLaMA-Modell vorgeschlagenen, aber in GermaNet nicht enthaltenen Hyponyme ermöglicht es, systematische Lücken sowie sprachliche Besonderheiten gezielt zu identifizieren – ein wichtiger Schritt für die lexikalisch-semantische Analyse.

1. Falsch geschriebene oder unvollständige Wörter  
   Beispiele: `Klausurergebni`, `Teilnehmerinn`, `E-mail`  
   Diese Begriffe weisen Tippfehler, abgeschnittene Endungen oder umgangssprachliche Schreibweisen auf.

2. Abkürzungen  
   Beispiele: `LV`, `PPT`, `SV-Nummer`  
   Die Begriffe stammen aus spezifischen Kontexten und liegen als Abkürzungen vor, die in dieser Form nicht in GermaNet enthalten sind.

3. Personennamen  
   Beispiele: `Sören`, `Vincent`, `Daniel`  
   Individuelle Eigennamen werden in GermaNet grundsätzlich nicht erfasst.

4. Technische oder fachspezifische Begriffe  
   Beispiele: `MacBook`, `Hadoop`, `Excel-Datei`, `Modulübersicht`  
   Diese Begriffe entstammen spezialisierten Domänen wie IT oder Hochschulverwaltung, die außerhalb des Abdeckungsbereichs von GermaNet liegen.

5. Alltagswörter  
   Beispiele: `bitte`, `jemand`, `was`, `Infos`  
   Solche Wörter besitzen keine klare lexikalische Bedeutung im Sinne der Hypernymie und gelten daher als ungeeignet für die Taxonomiebildung.

6. Zusammengesetzte Nomen  
   Beispiele: `Akkulturationsmodell`, `Ersatzlampe`, `Beispieltexte`  
   Komplexe Komposita werden oft nicht erkannt, da GermaNet in der Regel nur die Grundformen einzelner Lexeme erfasst.

7. Regionale Begriffe  
   Beispiele: `Schnitzstübl`, `Hexenfeuer`, `Mönkhag`  
   Diese Begriffe sind vermutlich regional geprägt und werden daher nicht von standardisierten Wortnetzen abgedeckt.

8. Groß- und Kleinschreibung (Case Sensitivity)  
   Beispiele: `mail`, `KAFFEE`  
   GermaNet ist case-sensitiv. Begriffe wie `Mail` oder `Kaffee` sind zwar enthalten, werden bei abweichender Schreibung jedoch nicht erkannt.

9. Kürzel und hochschulspezifischer Sprachgebrauch (Österreich)  
   Beispiele: `VO`, `STEOP`, `Hausübung`, `Vorschreibung`  
   Diese Begriffe stammen aus dem österreichischen Hochschulkontext bzw. aus verwaltungsinternem Vokabular und sind nicht Bestandteil von GermaNet.

### Analyse und Evaluaierung (Stichprobe)


| Hyponym | LLaMA-Hypernym | Bewertung | Begründung |
|-------------------------|------------------------------------|-----------|------------|
| **Rückmeldung** | Mitteilung | Korrekt | Eine spezielle Form der Mitteilung dar |
| **Kostenvoranschlag** | Angebot | Korrekt | Eine bestimmte Art von Angebot |
| **Film** | Kunstwerk | Korrekt | Zählt zu den Kunstwerken |
| **Kurs** | Bildung | Korrekt | Ein Mittel der Bildung |
| **Organisation** | Einrichtung | Korrekt | Eine spezielle Einrichtung |
| **Gottesdienst** | Zeremonie | Korrekt | Eine religiöse Zeremonie |
| **Mangel** | Defizit | Akzeptabel | Ähnliche Bedeutungskategorie |
| **Ergebnis** | Leistung | Teilweise korrekt | Etwa bei sportlichen Leistungen zutreffend |
| **Vernissage** | Feier | Teilweise korrekt | Spezifische Kunstfeier |
| **Fragebogen** | Frage | Falsch | Kein Fragetyp |
| **wandern** | Bewegung | Falsch | Keine Bewegungsart |
| **Fehler** | Mangel | Falsch | Unterschiedliche Konzepte |
| **Glaser** | Hersteller | Falsch | Ein Glaser übt einen Beruf aus, ist kein Hersteller |
| **Griff** | Werkzeug | Falsch |  Keine Unterkategorie |
| **Auspuff** | Fahrzeug | Falsch | Kein Fahrzeugstyp |
| **Flüchtling** | Asylsuchender | Teilweise falsch | Nicht alle Flüchtlinge sind Asylsuchende |

##### Evaluierung (Trefferquote)

| Kategorie | Anzahl | Anteil | Charakteristika | Beispiele |
|-----------|--------|--------|-----------------|-----------|
| **Korrekte Hypernyme** | 7 | 44% | Klare taxonomische Beziehung, präzise Abstraktion | Film→Kunstwerk, Gottesdienst→Zeremonie |
| **Akzeptable Näherungen** | 1 | 6% | Semantisch verwandt, aber keine strikte Taxonomie | Mangel→Defizit |
| **Kontextabhängige Fälle** | 2 | 13% | Nur in spezifischen Domänen gültig | Ergebnis→Leistung (Sport), Vernissage→Feier (Kunst) |
| **Systematische Fehler** | 6 | 37% | Verwechslung fundamentaler Relationen | Griff→Werkzeug (Teil-Ganzes), Glaser→Hersteller (Rollenfehler) |

##### Erkenntnisse und Schluss

LLaMA zeigt gemischte Ergebnisse bei der Generierung von Hypernymen. Grob lässt sich festhalten:

In etwa der Hälfte der Fälle liefert das Modell brauchbare taxonomische Oberbegriffe – insbesondere für konkrete Objektkategorien und institutionelle Begriffe. Dennoch treten typische Schwächen auf:

- Verwechslung von Hypernymie mit Teil-Ganzes-Relationen
- Zu allgemeine oder stark kontextabhängige Vorschläge
- Unsicherheiten bei Rollenzuweisungen und abstrakten Konzepten

Für den praktischen Einsatz bedeutet das:

- LLaMA eignet sich gut für erste Entwürfe und anwendungsorientierte Szenarien.
- Für den Aufbau wissenschaftlich belastbarer Taxonomien ist es jedoch ohne menschliche Prüfung nicht zuverlässig genug.

LLaMA kann den Aufbau von Hypernym-Taxonomien sinnvoll unterstützen, ersetzt jedoch keine systematisch kuratierten lexikalischen Ressourcen. Für präzise Anwendungen bleibt eine menschliche Validierung unerlässlich.
