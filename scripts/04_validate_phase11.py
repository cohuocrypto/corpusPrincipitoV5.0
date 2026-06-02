import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import json
import pandas as pd
from src.config import DATA_PROCESSED

REQUIRED = [
    "dialogue_id", "language", "chapter_id", "character", "emotion", "polarity",
    "semantic_cluster", "embedding", "primary_construct", "sociotechnical_variable"
]


def main():
    path = DATA_PROCESSED / "dialogues_analytic_matrix.parquet"
    if not path.exists():
        raise FileNotFoundError("Ejecuta primero scripts/03_embeddings_clusters.py")
    df = pd.read_parquet(path)
    missing = [c for c in REQUIRED if c not in df.columns]
    report = {
        "phase": "Fase 11 - Enriquecimiento de Metadatos Narrativos y Variables Sociotécnicas",
        "rows": int(len(df)),
        "columns": list(df.columns),
        "required_columns": REQUIRED,
        "missing_columns": missing,
        "status": "PASS" if not missing else "FAIL",
        "null_counts_required": {c: int(df[c].isna().sum()) for c in REQUIRED if c in df.columns},
        "character_distribution": df["character"].value_counts().to_dict() if "character" in df else {},
        "emotion_distribution": df["emotion"].value_counts().to_dict() if "emotion" in df else {},
        "semantic_clusters": sorted(df["semantic_cluster"].dropna().unique().astype(int).tolist()) if "semantic_cluster" in df else [],
    }
    out = DATA_PROCESSED / "phase11_validation_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if missing:
        raise ValueError(f"Fase 11 incompleta. Faltan columnas: {missing}")

if __name__ == "__main__":
    main()
