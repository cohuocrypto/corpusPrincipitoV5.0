# Corpus Pipeline V5 — *El Principito* Narrative Human Metrics Project : MarZ

Este repositorio contiene un pipeline reproducible para la construcción, enriquecimiento, validación y congelamiento de un corpus narrativo multilingüe basado en *El Principito*, orientado al análisis de factores humanos, emociones, personajes y variables sociotécnicas.

## Versión actual

**Versión:** V5 / V2.1 Frozen
**Estado:** estable y validada
**Corpus:** multilingüe EN–ES–FR
**Registros procesados:** 1404 diálogos
**Cobertura de personajes:** 90.17%
**Emociones no neutrales:** 68.87%
**Subjetividad promedio:** 0.4265
**Validación:** `validation_passed`

---

## Mejoras principales de esta versión

Esta versión incorpora mejoras respecto a la versión anterior:

1. Construcción del corpus base multilingüe.
2. Curaduría y normalización Unicode/OCR.
3. Segmentación por capítulos, oraciones y diálogos.
4. Extracción de metadatos narrativos.
5. Detección mejorada de personajes.
6. Atribución de hablante mediante reglas, ventana narrativa y dominancia por capítulo.
7. Análisis afectivo mejorado.
8. Cálculo de emoción, polaridad y subjetividad.
9. Validación formal de V2.1.
10. Congelamiento de versión reproducible.
11. Conservación de archivos CSV, Parquet y reportes JSON.

---

## Preparación

Coloca los textos base en:

```text
data/raw/ElPrincipito_EN.txt
data/raw/ElPrincipito_ES.txt
data/raw/ElPrincipito_FR.txt
```

Por derechos de autor, cada usuario debe proporcionar sus propios textos base.

---

## Instalación

```bash
python3 -m pip install -r requirements.txt

python3 -m spacy download es_core_news_sm
python3 -m spacy download fr_core_news_sm
python3 -m spacy download en_core_web_sm
```

---

## Ejecución completa V1–V5

```bash
./run_pipeline.sh
```

Para ejecutar la etapa narrativa enriquecida V2.1:

```bash
./run_pipeline_v2.sh
```

---

## Ejecución etapa por etapa

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

---

## Archivos principales de entrada

```text
data/processed/dialogues_base.parquet
```

Este archivo contiene el corpus base limpio sin anotaciones narrativas.

Columnas esperadas:

```text
record_id
language
chapter_id
chapter_title
dialogue
length_chars
length_words
dialogue_id
```

---

## Salida principal V2.1

```text
data/processed/dialogues_v2_enriched.parquet
data/processed/dialogues_v2_enriched.csv
```

Columnas principales:

```text
record_id
language
chapter_id
chapter_title
dialogue
length_chars
length_words
dialogue_id
character
speaker
speaker_confidence
attribution_method
emotion
emotion_score
polarity
subjectivity
affect_method
```

---

## Validación V2.1

El reporte de validación se genera en:

```text
data/processed/v2_validation_report.json
```

Resultado esperado:

```json
{
  "status": "validation_passed",
  "rows": 1404,
  "columns": 17,
  "coverage": {
    "character_known_rate": 0.9017,
    "character_unknown_rate": 0.0983,
    "emotion_non_neutral_rate": 0.6887,
    "chapter_available_rate": 1.0,
    "speaker_confidence_mean": 0.5536,
    "emotion_score_mean": 0.5066,
    "polarity_mean": 0.0075,
    "subjectivity_mean": 0.4265
  },
  "quality_flags": []
}
```

---

## Distribución de personajes V2.1

```text
little_prince    529
unknown          138
rose             134
businessman      131
fox              122
king              97
snake             72
geographer        70
lamplighter       38
drunkard          30
conceited_man     22
switchman         16
merchant           5
```

---

## Distribución emocional V2.1

```text
neutral      437   31.13%
curiosity    396   28.21%
love         329   23.43%
sadness      132    9.40%
fear          80    5.70%
anger         16    1.14%
joy           14    1.00%
```

---

## Métodos de atribución de personaje

```text
keyword_rules              629
previous_speaker_window    482
chapter_dominance           84
sandwich_propagation        71
no_match                   138
```

---

## Congelamiento de versión

Para congelar la versión validada:

```bash
python3 scripts/10_freeze_v2.py
```

Salida esperada:

```text
data/frozen/v2_1/
```

Archivos esperados:

```text
dialogues_v2_enriched.parquet
dialogues_v2_enriched.csv
v2_validation_report.json
manifest.json
corpus.summary.json
```

---

## Interpretación metodológica

La versión V5 / V2.1 Frozen transforma el corpus base en un corpus narrativo enriquecido. Cada diálogo queda asociado con personaje, hablante, confianza de atribución, emoción predominante, polaridad y subjetividad.

Esta versión permite estudiar patrones narrativos, afectivos y sociotécnicos en la obra, y constituye la base para futuras versiones orientadas a:

```text
V3.0 — Semantic Layer
V4.0 — Human Narrative Agile Constructs
V5.0 — Narrative Sociotechnical Graph
```

---

## Próxima versión recomendada

La siguiente fase debe centrarse en la capa semántica:

```text
semantic_cluster
cluster_probability
topic
alignment_score
parallel_group
```

Esto permitirá avanzar hacia el modelo HNAC:

```text
Character
↓
Emotion
↓
Semantic Cluster
↓
Narrative Construct
↓
Human Factor
↓
Agile Principle
```
