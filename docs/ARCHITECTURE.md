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



Characters
Emotions
Semantic clusters

Graph edges:

character → emotion
character → semantic cluster
emotion → semantic cluster

## Main outputs

- data/processed/dialogues_base.parquet
- data/processed/dialogues_v2_enriched.parquet
- data/processed/v2_validation_report.json
- data/frozen/

# with Multilingual Narrative Knowledge Graph Corpus
##pipeline
07 Character Detection
08 Emotion + Polarity
09 Validation V2
10 Freeze V2

11 Semantic Alignment
12 Semantic Clustering
13 Validation V5
14 Freeze V5
15 Narrative Semantic Graph
## outputs
outputs/graphs/narrative_graph.graphml
outputs/graphs/narrative_graph.gexf
outputs/graphs/narrative_graph.png
outputs/graphs/graph_metrics.json
Graph nodes: