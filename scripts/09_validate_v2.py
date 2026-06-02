"""
09_validate_v2.py
V2.0 - Validacion de corpus narrativo enriquecido.

Entrada:
    data/processed/dialogues_v2_enriched.parquet

Salida:
    data/processed/v2_validation_report.json

Valida:
- Existencia de columnas V2.
- Porcentaje de personajes desconocidos.
- Cobertura emocional.
- Rangos de polaridad, subjectivity y confidence.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PROCESSED = ROOT / "data" / "processed"
INPUT_FILE = DATA_PROCESSED / "dialogues_v2_enriched.parquet"
OUTPUT_REPORT = DATA_PROCESSED / "v2_validation_report.json"

REQUIRED_COLUMNS = [
    "dialogue_id",
    "character",
    "speaker",
    "speaker_confidence",
    "attribution_method",
    "chapter_id",
    "emotion",
    "emotion_score",
    "polarity",
    "subjectivity",
    "affect_method",
]


def safe_rate(condition) -> float:
    return round(float(condition.mean()), 4) if len(condition) else 0.0


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"No existe {INPUT_FILE}. Ejecuta primero: python3 scripts/08_emotion_polarity.py"
        )

    df = pd.read_parquet(INPUT_FILE)
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    report = {
        "version": "2.0.0-dev",
        "status": "validation_passed" if not missing_columns else "validation_failed",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input_file": str(INPUT_FILE),
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "required_columns": REQUIRED_COLUMNS,
        "missing_columns": missing_columns,
        "coverage": {},
        "quality_flags": [],
    }

    if not missing_columns:
        report["coverage"] = {
            "character_known_rate": safe_rate(df["character"].fillna("unknown") != "unknown"),
            "character_unknown_rate": safe_rate(df["character"].fillna("unknown") == "unknown"),
            "emotion_non_neutral_rate": safe_rate(df["emotion"].fillna("neutral") != "neutral"),
            "chapter_available_rate": safe_rate(df["chapter_id"].notna()),
            "speaker_confidence_mean": round(float(df["speaker_confidence"].mean()), 4),
            "emotion_score_mean": round(float(df["emotion_score"].mean()), 4),
            "polarity_mean": round(float(df["polarity"].mean()), 4),
            "subjectivity_mean": round(float(df["subjectivity"].mean()), 4),
        }

        if not df["polarity"].between(-1, 1).all():
            report["quality_flags"].append("polarity_out_of_range")
        if not df["subjectivity"].between(0, 1).all():
            report["quality_flags"].append("subjectivity_out_of_range")
        if not df["speaker_confidence"].between(0, 1).all():
            report["quality_flags"].append("speaker_confidence_out_of_range")
        if report["coverage"]["character_unknown_rate"] > 0.70:
            report["quality_flags"].append("high_unknown_character_rate")
        if report["coverage"]["emotion_non_neutral_rate"] < 0.10:
            report["quality_flags"].append("low_emotion_coverage")

        report["distributions"] = {
            "characters": df["character"].value_counts(dropna=False).head(30).to_dict(),
            "emotions": df["emotion"].value_counts(dropna=False).to_dict(),
            "attribution_methods": df["attribution_method"].value_counts(dropna=False).to_dict(),
        }

    OUTPUT_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Reporte generado:", OUTPUT_REPORT)
    print(json.dumps(report, indent=2, ensure_ascii=False))

    if missing_columns:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
