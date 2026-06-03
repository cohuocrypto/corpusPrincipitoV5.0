import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "data" / "processed" / "dialogues_v5_semantic_clusters.parquet"
REPORT_FILE = ROOT / "data" / "processed" / "v5_validation_report.json"

REQUIRED_COLUMNS = [
    "record_id",
    "language",
    "chapter_id",
    "dialogue",
    "character",
    "speaker",
    "speaker_confidence",
    "emotion",
    "emotion_score",
    "polarity",
    "subjectivity",
    "parallel_group",
    "alignment_score",
    "aligned_to_record_id",
    "semantic_cluster",
    "cluster_probability"
]


def main():
    df = pd.read_parquet(INPUT_FILE)

    missing = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    quality_flags = []

    if missing:
        quality_flags.append("missing_required_columns")

    if (df["character"] == "unknown").mean() > 0.20:
        quality_flags.append("high_unknown_character_rate")

    if (df["emotion"] == "neutral").mean() > 0.40:
        quality_flags.append("high_neutral_emotion_rate")

    if df["alignment_score"].mean() < 0.30:
        quality_flags.append("low_alignment_score")

    if df["cluster_probability"].mean() < 0.30:
        quality_flags.append("low_cluster_probability")

    report = {
        "version": "5.0.0-frozen",
        "status": "validation_passed" if not quality_flags else "validation_warning",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input_file": str(INPUT_FILE),
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "required_columns": REQUIRED_COLUMNS,
        "missing_columns": missing,
        "coverage": {
            "character_known_rate": round(float((df["character"] != "unknown").mean()), 4),
            "emotion_non_neutral_rate": round(float((df["emotion"] != "neutral").mean()), 4),
            "alignment_score_mean": round(float(df["alignment_score"].mean()), 4),
            "cluster_probability_mean": round(float(df["cluster_probability"].mean()), 4),
            "subjectivity_mean": round(float(df["subjectivity"].mean()), 4)
        },
        "quality_flags": quality_flags,
        "distributions": {
            "languages": df["language"].value_counts().to_dict(),
            "characters": df["character"].value_counts().to_dict(),
            "emotions": df["emotion"].value_counts().to_dict(),
            "clusters": {
                str(k): int(v)
                for k, v in df["semantic_cluster"].value_counts().sort_index().to_dict().items()
            }
        }
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()