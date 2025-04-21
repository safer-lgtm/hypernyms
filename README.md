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

