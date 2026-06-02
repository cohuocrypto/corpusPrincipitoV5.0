"""
10_freeze_v2.py
V2.0 - Congelamiento de version.

Entrada:
    data/processed/dialogues_v2_enriched.parquet
    data/processed/dialogues_v2_enriched.csv
    data/processed/v2_validation_report.json

Salida:
    data/frozen/v2_0/dialogues_v2_enriched.parquet
    data/frozen/v2_0/dialogues_v2_enriched.csv
    data/frozen/v2_0/v2_validation_report.json
    data/frozen/v2_0/manifest.json
    data/frozen/v2_0/corpus.summary.json
"""

from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PROCESSED = ROOT / "data" / "processed"
FROZEN_DIR = ROOT / "data" / "frozen" / "v2_0"
FROZEN_DIR.mkdir(parents=True, exist_ok=True)

FILES_TO_FREEZE = [
    DATA_PROCESSED / "dialogues_v2_enriched.parquet",
    DATA_PROCESSED / "dialogues_v2_enriched.csv",
    DATA_PROCESSED / "v2_validation_report.json",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_metadata(path: Path) -> Dict[str, object]:
    return {
        "filename": path.name,
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def main() -> None:
    missing = [str(path) for path in FILES_TO_FREEZE if not path.exists()]
    if missing:
        raise FileNotFoundError("Faltan archivos para congelar:\n" + "\n".join(missing))

    frozen_files = []
    for source in FILES_TO_FREEZE:
        target = FROZEN_DIR / source.name
        shutil.copy2(source, target)
        frozen_files.append(file_metadata(target))

    df = pd.read_parquet(DATA_PROCESSED / "dialogues_v2_enriched.parquet")

    summary = {
        "version": "2.0.0",
        "status": "frozen",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "description": "Corpus narrativo enriquecido con identificacion inicial de personajes, emocion, polaridad y subjetividad.",
        "rows": int(len(df)),
        "columns": list(df.columns),
        "languages": sorted(df["language"].dropna().unique().tolist()) if "language" in df.columns else [],
        "characters": df["character"].value_counts(dropna=False).to_dict() if "character" in df.columns else {},
        "emotions": df["emotion"].value_counts(dropna=False).to_dict() if "emotion" in df.columns else {},
    }

    manifest = {
        "project": "The Little Prince Multilingual Narrative Corpus",
        "version": "2.0.0",
        "status": "frozen",
        "created_at": summary["created_at"],
        "source_version": "v1_0 frozen corpus",
        "methodological_layer": "V2 - Narrative metadata and affective enrichment",
        "new_variables": [
            "character",
            "speaker",
            "speaker_confidence",
            "attribution_method",
            "emotion",
            "emotion_score",
            "polarity",
            "subjectivity",
            "affect_method",
        ],
        "files": frozen_files,
        "reproducibility_note": "V2 is derived from V1 frozen outputs. V1 files are not modified.",
    }

    (FROZEN_DIR / "corpus.summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (FROZEN_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print("Version V2 congelada en:", FROZEN_DIR)
    print("Archivos:")
    for item in sorted(FROZEN_DIR.iterdir()):
        print(" -", item.name)


if __name__ == "__main__":
    main()
