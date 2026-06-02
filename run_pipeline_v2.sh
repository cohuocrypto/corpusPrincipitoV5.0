#!/usr/bin/env bash
set -e

python3 scripts/07_detect_characters.py
python3 scripts/08_emotion_polarity.py
python3 scripts/09_validate_v2.py
python3 scripts/10_freeze_v2.py