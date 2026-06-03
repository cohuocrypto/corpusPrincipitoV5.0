# Multilingual Narrative Knowledge Graph Corpus

# Corpus Principito V5.0 — Multilingual Narrative Human Metrics Corpus
# español

Repositorio reproducible para construir, enriquecer, validar y congelar un corpus narrativo multilingüe basado en *El Principito*, orientado al análisis narrativo, emocional, semántico y sociotécnico.

## Estado del proyecto

**Versión:** 5.0.0-frozen
**Estado:** estable / publicable
**Idiomas:** inglés, español y francés
**Corpus:** 1404 diálogos procesados
**Cobertura de personajes:** 90.17%
**Emociones no neutrales:** 68.87%
**Subjetividad promedio:** 0.4265

## Objetivo

Construir un corpus narrativo multilingüe enriquecido con:

* segmentación por capítulos y diálogos;
* detección de personajes;
* atribución de hablante;
* análisis emocional;
* polaridad;
* subjetividad;
* embeddings multilingües;
* alineación semántica multilingüe;
* clustering semántico;
* validación formal;
* congelamiento reproducible con manifiestos y reportes.

## Preparación

Por derechos de autor, los textos fuente no se redistribuyen en este repositorio.
Cada usuario debe colocar sus propios archivos base en:

```text
data/raw/ElPrincipito_EN.txt
data/raw/ElPrincipito_ES.txt
data/raw/ElPrincipito_FR.txt
```

## Instalación

```bash
python3 -m pip install -r requirements.txt

python3 -m spacy download es_core_news_sm
python3 -m spacy download fr_core_news_sm
python3 -m spacy download en_core_web_sm
```

## Dependencias principales

```text
pandas
numpy
scikit-learn
sentence-transformers
spacy
pyarrow
chardet
rapidfuzz
unidecode
```

Si se usan técnicas avanzadas de reducción dimensional o clustering externo, instalar también:

```bash
python3 -m pip install umap-learn hdbscan
```

## Ejecución completa

```bash
./run_pipeline_v5.sh
```

## Ejecución por etapas

### Corpus base

```bash
python3 scripts/01_build_base_corpus.py
python3 scripts/02_enrich_metadata.py
python3 scripts/03_embeddings_clusters.py
python3 scripts/04_validate_phase11.py
python3 scripts/05_freeze_version.py --version v4_0_phase11
python3 scripts/06_draw_graph.py
```

### Enriquecimiento narrativo V2.1

```bash
python3 scripts/07_detect_characters.py
python3 scripts/08_emotion_polarity.py
python3 scripts/09_validate_v2.py
python3 scripts/10_freeze_v2.py
```

### Capa semántica V5.0

```bash
python3 scripts/11_semantic_alignment.py
python3 scripts/12_semantic_clusters.py
python3 scripts/13_validate_v5.py
python3 scripts/14_freeze_v5.py
```

## Scripts principales

| Script                      | Descripción                                |
| --------------------------- | ------------------------------------------ |
| `01_build_base_corpus.py`   | Construye el corpus base multilingüe.      |
| `02_enrich_metadata.py`     | Enriquece metadatos narrativos iniciales.  |
| `03_embeddings_clusters.py` | Genera embeddings y clusters iniciales.    |
| `04_validate_phase11.py`    | Valida la matriz analítica de Fase 11.     |
| `05_freeze_version.py`      | Congela una versión con hash SHA-256.      |
| `06_draw_graph.py`          | Genera grafo narrativo-sociotécnico.       |
| `07_detect_characters.py`   | Detecta personajes y hablantes.            |
| `08_emotion_polarity.py`    | Calcula emoción, polaridad y subjetividad. |
| `09_validate_v2.py`         | Valida la versión narrativa enriquecida.   |
| `10_freeze_v2.py`           | Congela la versión V2.1.                   |
| `11_semantic_alignment.py`  | Calcula alineación semántica multilingüe.  |
| `12_semantic_clusters.py`   | Calcula clusters semánticos.               |
| `13_validate_v5.py`         | Valida la versión V5.0 final.              |
| `14_freeze_v5.py`           | Congela la versión V5.0 publicable.        |
`15. Narrative Semantic Graph`




## Validación final

Para validar la versión completa:

```bash
python3 scripts/13_validate_v5.py
```

El resultado esperado es:

```text
status: validation_passed
```

## Congelamiento final

Para congelar la versión publicable:

```bash
python3 scripts/14_freeze_v5.py
```

Esto genera:

```text
data/frozen/v5_0_frozen/manifest.json
data/frozen/v5_0_frozen/corpus.summary.json
```


con hashes SHA-256 de los artefactos principales.
```bash
python3 scripts/15_draw_graph.py
```
esto genera:
```text
outputs/graphs/narrative_graph.graphml
outputs/graphs/narrative_graph.gexf
outputs/graphs/narrative_graph.png
outputs/graphs/graph_metrics.json
```

## Citación

Si usas este repositorio, cita:

```text
Cohuo Ávila, M. A. Corpus Principito V5.0: Multilingual Narrative Human Metrics Corpus. GitHub repository. Version 5.0.0-frozen.
```
Puede citar todas las versiones utilizando el DOI 10.5281/zenodo.20520566. Este DOI representa todas las versiones y siempre se corresponderá con la más reciente.

## Licencia

El código fuente se distribuye bajo licencia MIT.

Los textos literarios no se redistribuyen por restricciones de derechos de autor.
Cada usuario debe proporcionar sus propios textos fuente en `data/raw/`.

## Próximas extensiones

La versión V5.0 deja preparado el corpus para futuras capas:

```text
Human Narrative Agile Constructs
Human Factors Mapping
Agile Principles Mapping
Narrative Sociotechnical Graph
Character Embeddings
```
# Corpus Principito V5.0 — Multilingual Narrative Human Metrics Corpus
# english
Reproducible repository to build, enrich, validate and freeze a multilingual narrative corpus based on *The Little Prince*, oriented towards narrative, emotional, semantic and sociotechnical analysis.

## Project Status

**Version:** 5.0.0-frozen
**Status:** stable / publishable
**Languages:** English, Spanish, and French
**Corpus:** 1404 processed dialogues
**Character Coverage:** 90.17%
**Non-neutral Emotions:** 68.87%
**Average Subjectivity:** 0.4265

## Objective

To build an enriched multilingual narrative corpus with:

* segmentation by chapters and dialogues;

* character detection;

* speaker attribution;

* emotional analysis;

* polarity;

* subjectivity;

* multilingual embeddings;

* Multilingual semantic alignment;

* Semantic clustering;

* Formal validation;

* Reproducible freezing with manifests and reports.

## Preparation

Due to copyright, the source texts are not redistributed in this repository.

Each user must place their own source files in:

```text
data/raw/ElPrincipito_EN.txt
data/raw/ElPrincipito_ES.txt
data/raw/ElPrincipito_FR.txt
```
## Installation

```bash
python3 -m pip install -r requirements.txt

python3 -m spacy download es_core_news_sm
python3 -m spacy download fr_core_news_sm
python3 -m spacy download en_core_web_sm
```

## Main Dependencies

```text
pandas
numpy
scikit-learn
sentence-transformers
spacy
pyarrow
chardet
rapidfuzz
unidecode
```

If using advanced dimensionality reduction or external clustering techniques, also install:

```bash
python3 -m pip install umap-learn hdbscan
```

## Full Execution

```bash
./run_pipeline_v5.sh
```

## Staged Execution

### Corpus base

```bash
python3 scripts/01_build_base_corpus.py
python3 scripts/02_enrich_metadata.py
python3 scripts/03_embeddings_clusters.py
python3 scripts/04_validate_phase11.py
python3 scripts/05_freeze_version.py --version v4_0_phase11
python3 scripts/06_draw_graph.py
```
### Narrative Enrichment V2.1

```bash
python3 scripts/07_detect_characters.py
python3 scripts/08_emotion_polarity.py
python3 scripts/09_validate_v2.py
python3 scripts/10_freeze_v2.py
```

### Semantic layer V5.0

```bash
python3 scripts/11_semantic_alignment.py
python3 scripts/12_semantic_clusters.py
python3 scripts/13_validate_v5.py
python3 scripts/14_freeze_v5.py
```
```bash
python3 scripts/15_draw_graph.py
```
this generates:
```text
outputs/graphs/narrative_graph.graphml
outputs/graphs/narrative_graph.gexf
outputs/graphs/narrative_graph.png
outputs/graphs/graph_metrics.json
```
## Main scripts

| Script | Description |
| --------------------------- | ------------------------------------------ |
| `01_build_base_corpus.py` | Build the multilingual base corpus. |

`02_enrich_metadata.py` | Enrich initial narrative metadata. |

`03_embeddings_clusters.py` | Generate initial embeddings and clusters. |

`04_validate_phase11.py` | Validate the Phase 11 analytical matrix. |

`05_freeze_version.py` | Freeze a version with a SHA-256 hash. |

`06_draw_graph.py` | Generate a socio-technical narrative graph. |

`07_detect_characters.py` | Detect characters and speakers. |

`08_emotion_polarity.py` | Calculate emotion, polarity, and subjectivity. |

`09_validate_v2.py` | Validate the enriched narrative version. |

`10_freeze_v2.py` | Freezes version V2.1. |

`11_semantic_alignment.py` | Calculates multilingual semantic alignment. |

`12_semantic_clusters.py` | Calculates semantic clusters. |

`13_validate_v5.py` | Validates the final version V5.0. |

`14_freeze_v5.py` | Freezes the publishable version V5.0. |
##Main files generated

`15. Narrative Semantic Graph`

### Base corpus

```text
data/processed/dialogues_base.parquet
data/processed/chapters.parquet
```

### Enriched narrative corpus

```text
data/processed/dialogues_v2_enriched.parquet
data/processed/dialogues_v2_enriched.csv
data/processed/v2_validation_report.json
```

### Semantic alignment

```text
data/processed/dialogues_v5_semantic_alignment.parquet
data/processed/dialogues_v5_semantic_alignment.csv
data/processed/semantic_alignment_report.json
```

### Clustering semantic

```text
data/processed/dialogues_v5_semantic_clusters.parquet
data/processed/dialogues_v5_semantic_clusters.csv
data/processed/semantic_cluster_report.json
```

### V5 final validation

```text
data/processed/v5_validation_report.json
```

### Frozen version

```text
data/frozen/v5_0_frozen/
```

Files expected:

```text
dialogues_v5_semantic_clusters.parquet
dialogues_v5_semantic_clusters.csv
v5_validation_report.json
semantic_alignment_report.json
semantic_cluster_report.json
manifest.json
corpus.summary.json
```

## Main columns V5

```text
record_id
language
chapter_id
chapter_title
dialogue
length_chars
length_words
dialogue_id
characters
speaker
speaker_confidence
attribution_method
emotion
emotion_score
polarity
subjectivity
affect_method
parallel_group
alignment_score
aligned_to_record_id
alignment_method
semantic_cluster
cluster_probability
cluster_method
```

## Quality Metrics V2.1

```text
character_known_rate: 0.9017
character_unknown_rate: 0.0983
emotion_non_neutral_rate: 0.6887
chapter_available_rate: 1.0
speaker_confidence_mean: 0.5536
emotion_score_mean: 0.5066
polarity_mean: 0.0075
subjectivity_mean: 0.4265
quality_flags: []
```

## Emotional Distribution V2.1

```text
neutral 437 31.13%
curiosity 396 28.21%
love 329 23.43%
sadness 132 9.40%
fear 80 5.70%
anger 16 1.14%
joy 14 1.00%
```

## Character Distribution V2.1

```text
little_prince 529
unknown 138
rose 134
businessman 131
fox 122
king 97
snake 72
geographer 70
lamplighter 38
drunkard 30
conceited_man 22
switchman 16
merchant 5
```
## Final Validation

To validate the full version:

```bash
python3 scripts/13_validate_v5.py
```

The expected result is:

```text
status: validation_passed
```

## Final Freeze

To freeze the publishable version:

```bash
python3 scripts/14_freeze_v5.py
```
15. Narrative Semantic Graph

This generates:

```text
data/frozen/v5_0_frozen/manifest.json
data/frozen/v5_0_frozen/corpus.summary.json
```

with SHA-256 hashes of the main artifacts.


## Citation

If you use this repository, please cite:

```text
Cohuo Ávila, M. A. Corpus Principito V5.0: Multilingual Narrative Human Metrics Corpus. GitHub repository. Version 5.0.0-frozen.
```
You can cite all versions using the DOI 10.5281/zenodo.20520566. This DOI represents all versions and will always correspond to the most recent one.

## License

The source code is distributed under the MIT license.

The literary texts are not redistributed due to copyright restrictions.

Each user must provide their own source texts in `data/raw/`.


` ...

````````````````

`````````````` 
## Upcoming Extensions

Version V5.0 prepares the corpus for future layers:

```text
Human Narrative Agile Constructs
Human Factors Mapping
Agile Principles Mapping
Narrative Sociotechnical Graph
Character Embeddings
```
# Corpus du Petit Prince V5.0 — Corpus multilingue de métriques narratives humaines

# Français

Un dépôt reproductible pour la construction, l'enrichissement, la validation et la stabilisation d'un corpus narratif multilingue basé sur *Le Petit Prince*, destiné à l'analyse narrative, émotionnelle, sémantique et sociotechnique.

## État du projet

**Version :** 5.0.0-figée
**Statut :** stable / publiable
**Langues :** anglais, espagnol et français

**Corpus :** 1 404 dialogues traités
**Couverture des personnages :** 90,17 %

**Émotions non neutres :** 68,87 %
**Subjectivité moyenne :** 0,4265

## Objectif

Construire un corpus narratif multilingue enrichi avec :

* segmentation par chapitres et dialogues ;

* détection des personnages ;

* attribution des locuteurs ;

* analyse émotionnelle ;

* Polarité ;

* Subjectivité ;

* Représentations vectorielles multilingues ;

* Alignement sémantique multilingue ;

* Regroupement sémantique ;

* Validation formelle ;

* Gel reproductible avec manifestes et rapports.

## Préparation

Pour des raisons de droits d'auteur, les textes sources ne sont pas redistribués dans ce dépôt.

Chaque utilisateur doit placer ses propres fichiers de base dans :

```text
data/raw/ElPrincipito_EN.txt
data/raw/ElPrincipito_ES.txt
data/raw/ElPrincipito_FR.txt
```

## Installation

```bash
python3 -m pip install -r requirements.txt

python3 -m spacy download es_core_news_sm
python3 -m spacy download fr_core_news_sm
python3 -m spacy download en_core_web_sm
```

## Principales dépendances

```text
pandas
numpy
scikit-learn
sentence-transformers
spacy
pyarrow
chardet
rapidfuzz
unidecode

```

Si vous utilisez des techniques avancées de réduction de dimensionnalité ou un clustering externe, installez également :

```bash
python3 -m pip install umap-learn hdbscan

```

## Exécution complète

```bash
./run_pipeline_v5.sh
```

## Exécution par phases

### Corpus de base

```bash
python3 scripts/01_build_base_corpus.py
python3 scripts/02_enrich_metadata.py
python3 scripts/03_embeddings_clusters.py
python3 scripts/04_validate_phase11.py
python3 scripts/05_freeze_version.py --version v4_0_phase11
python3 scripts/06_draw_graph.py
```
### Enrichissement narratif V2.1

```bash
python3 scripts/07_detect_characters.py
python3 scripts/08_emotion_polarity.py
python3 scripts/09_validate_v2.py
python3 scripts/10_freeze_v2.py
```

### Couche sémantique V5.0

```bash
python3 scripts/11_semantic_alignment.py
python3 scripts/12_semantic_clusters.py
python3 scripts/13_validate_v5.py
python3 scripts/14_freeze_v5.py
```
```bash
python3 scripts/15_draw_graph.py

```
Ce script génère :

```texte
outputs/graphs/narrative_graph.graphml

outputs/graphs/narrative_graph.gexf

outputs/graphs/narrative_graph.png

outputs/graphs/graph_metrics.json
```
## Scripts principaux

| Script | Description |

| --------------------------- | ------------------------------------------ |

| `01_build_base_corpus.py` | Construction du corpus de base multilingue. |

`02_enrich_metadata.py` | Enrichir les métadonnées narratives initiales. |

`03_embeddings_clusters.py` | Générer les plongements et les clusters initiaux. |

`04_validate_phase11.py` | Valider la matrice analytique de la Phase 11. |

`05_freeze_version.py` | Figer une version avec un hachage SHA-256. |

`06_draw_graph.py` | Générer un graphe narratif socio-technique. |

`07_detect_characters.py` | Détecter les personnages et les locuteurs. |

`08_emotion_polarity.py` | Calculer l'émotion, la polarité et la subjectivité. |

`09_validate_v2.py` | Valider la version narrative enrichie. |

`10_freeze_v2.py` | Fige la version V2.1. |

`11_semantic_alignment.py` | Calcule l'alignement sémantique multilingue. |

`12_semantic_clusters.py` | Calcule les regroupements sémantiques. |

`13_validate_v5.py` | Valide la version finale V5.0. |

`14_freeze_v5.py` | Fige la version publiable V5.0. |
'15. Narrative Semantic Graph'

## Validation finale

Pour valider la version complète :

```bash
python3 scripts/13_validate_v5.py
```

Le résultat attendu est :

```text
status: validation_passed
```

## Gel final

Pour figer la version publiable :

```bash
python3 scripts/14_freeze_v5.py
```

Ceci génère :

```text
data/frozen/v5_0_frozen/manifest.json
data/frozen/v5_0_frozen/corpus.summary.json
```

avec les hachages SHA-256 des principaux artefacts.

## Citation

Si vous utilisez ce dépôt, veuillez citer :

```texte
Cohuo Ávila, M. A. Corpus Principito V5.0 : Corpus multilingue de métriques narratives humaines. Dépôt GitHub. Version 5.0.0-frozen.

``` Vous pouvez citer toutes les versions à l’aide du DOI 10.5281/zenodo.20520566. Ce DOI représente toutes les versions et correspondra toujours à la plus récente.

## Licence

Le code source est distribué sous licence MIT.

Les textes littéraires ne sont pas redistribués en raison des restrictions liées au droit d’auteur.

Chaque utilisateur doit fournir ses propres textes sources dans `data/raw/`.

` ...
````````````````

`````````````` ## Extensions à venir

La version V5.0 prépare le corpus pour les couches futures :

```texte
Constructions agiles narratives humaines
Cartographie des facteurs humains
Cartographie des principes agiles
Graphe sociotechnique narratif
Représentation vectorielle des caractères
```