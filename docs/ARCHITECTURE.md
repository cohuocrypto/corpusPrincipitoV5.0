# Architecture

## Pipeline

RAW corpus
→ Unicode normalization
→ OCR cleaning
→ Chapter segmentation
→ Sentence segmentation
→ Dialogue extraction
→ Character detection
→ Emotion extraction
→ Multilingual embeddings
→ Semantic alignment
→ Structured NLP corpus
→ Validation
→ Frozen release

## Main outputs

- data/processed/dialogues_base.parquet
- data/processed/dialogues_v2_enriched.parquet
- data/processed/v2_validation_report.json
- data/frozen/