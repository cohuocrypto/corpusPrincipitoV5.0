#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"

$PYTHON_BIN scripts/01_build_base_corpus.py
$PYTHON_BIN scripts/02_enrich_metadata.py
$PYTHON_BIN scripts/03_embeddings_clusters.py
$PYTHON_BIN scripts/04_validate_phase11.py
$PYTHON_BIN scripts/05_freeze_version.py --version v4_0_phase11
$PYTHON_BIN scripts/06_draw_graph.py
