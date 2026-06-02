# V5.0 Corpus Narrativo Enriquecido

Objetivo: enriquecer la V4.0 con metadatos narrativos.

## Nuevas variables

- character
- speaker_confidence
- chapter_context
- emotion
- polarity
- subjectivity

## Entrada

- data/frozen/v4_0/dialogues.parquet
- data/frozen/v4_0/sentences.parquet
- data/frozen/v4_0/chapters.parquet

## Salida

- data/processed/dialogues_v2_enriched.parquet
- data/frozen/v4_0/manifest.json