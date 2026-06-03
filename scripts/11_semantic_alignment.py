import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "data" / "processed" / "dialogues_v2_enriched.parquet"
OUTPUT_FILE = ROOT / "data" / "processed" / "dialogues_v5_semantic_alignment.parquet"
OUTPUT_CSV = ROOT / "data" / "processed" / "dialogues_v5_semantic_alignment.csv"
REPORT_FILE = ROOT / "data" / "processed" / "semantic_alignment_report.json"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def main():
    print("=== Semantic Alignment V5 ===")

    df = pd.read_parquet(INPUT_FILE)

    model = SentenceTransformer(MODEL_NAME)

    embeddings = model.encode(
        df["dialogue"].astype(str).tolist(),
        show_progress_bar=True,
        normalize_embeddings=True
    )

    df["embedding_index"] = range(len(df))

    alignment_group = []
    alignment_score = []
    aligned_to = []

    for i, row in df.iterrows():
        current_lang = row["language"]
        current_chapter = row["chapter_id"]

        candidates = df[
            (df["chapter_id"] == current_chapter)
            & (df["language"] != current_lang)
        ]

        if candidates.empty:
            alignment_group.append(f"group_{i}")
            alignment_score.append(0.0)
            aligned_to.append(None)
            continue

        candidate_indices = candidates["embedding_index"].tolist()

        sims = cosine_similarity(
            embeddings[i].reshape(1, -1),
            embeddings[candidate_indices]
        )[0]

        best_pos = int(np.argmax(sims))
        best_score = float(sims[best_pos])
        best_idx = candidate_indices[best_pos]

        alignment_group.append(f"align_{min(i, best_idx)}_{max(i, best_idx)}")
        alignment_score.append(round(best_score, 4))
        aligned_to.append(df.loc[best_idx, "record_id"])

    df["parallel_group"] = alignment_group
    df["alignment_score"] = alignment_score
    df["aligned_to_record_id"] = aligned_to
    df["alignment_method"] = "cosine_multilingual_embeddings_v1"

    df.to_parquet(OUTPUT_FILE, index=False)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    report = {
        "rows": int(len(df)),
        "mean_alignment_score": round(float(np.mean(alignment_score)), 4),
        "min_alignment_score": round(float(np.min(alignment_score)), 4),
        "max_alignment_score": round(float(np.max(alignment_score)), 4),
        "method": "cosine similarity with multilingual sentence embeddings"
    }

    import json
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("Archivo generado:", OUTPUT_FILE)
    print("Reporte:", REPORT_FILE)
    print(report)


if __name__ == "__main__":
    main()