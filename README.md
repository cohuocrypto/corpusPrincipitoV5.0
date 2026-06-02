# Corpus Pipeline V4 - "El Principito" Human Metrics project : MarZ.

Este paquete contiene el código original en etapas reproducibles:

1. Construcción del corpus base.
2. Enriquecimiento de metadatos narrativos y variables sociotécnicas.
3. Embeddings multilingües y clusters semánticos.
4. Validación formal.
5. Congelamiento de versión con hash SHA-256.
6. Grafo narrativo-sociotécnico en PNG y GraphML.

## Preparación

Coloca los textos en: (por derechos de autor debes identificar tus libros base.)

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

## Ejecución completa

```bash
./run_pipeline.sh
```

Si falla, ejecuta etapa por etapa:

```bash
python3 scripts/01_build_base_corpus.py
python3 scripts/02_enrich_metadata.py
python3 scripts/03_embeddings_clusters.py
python3 scripts/04_validate_phase11.py
python3 scripts/05_freeze_version.py --version v4_0_phase11
python3 scripts/06_draw_graph.py
```

## Salida principal

```text
data/processed/dialogues_analytic_matrix.parquet
```

Columnas obligatorias de Fase 11:

- `character`
- `chapter_id`
- `emotion`
- `polarity`
- `semantic_cluster`
- `embedding`
- `primary_construct`
- `sociotechnical_variable`

