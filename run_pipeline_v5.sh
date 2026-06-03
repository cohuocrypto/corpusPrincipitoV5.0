#!/usr/bin/env bash
set -e

python3 scripts/07_detect_characters.py
python3 scripts/08_emotion_polarity.py
python3 scripts/09_validate_v2.py
python3 scripts/11_semantic_alignment.py
python3 scripts/12_semantic_clusters.py
python3 scripts/13_validate_v5.py
python3 scripts/14_freeze_v5.py