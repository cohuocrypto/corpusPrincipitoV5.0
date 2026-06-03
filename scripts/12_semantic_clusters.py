import pandas as pd
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "data" / "processed" / "dialogues_v5_semantic_alignment.parquet"
OUTPUT_FILE = ROOT / "data" / "processed" / "dialogues_v5_semantic_clusters.parquet"
OUTPUT_CSV = ROOT / "data" / "processed" / "dialogues_v5_semantic_clusters.csv"
REPORT_FILE = ROOT / "data" / "processed" / "semantic_cluster_report.json"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
N_CLUSTERS = 12


def main():
    print("=== Semantic Clustering V5 ===")

    df = pd.read_parquet(INPUT_FILE)

    model = SentenceTransformer(MODEL_NAME)

    embeddings = model.encode(
        df["dialogue"].astype(str).tolist(),
        show_progress_bar=True,
        normalize_embeddings=True
    )

    kmeans = KMeans(
        n_clusters=N_CLUSTERS,
        random_state=42,
        n_init="auto"
    )

    labels = kmeans.fit_predict(embeddings)

    distances = kmeans.transform(embeddings)
    min_dist = distances.min(axis=1)
    max_dist = max(min_dist) if max(min_dist) != 0 else 1

    probabilities = 1 - (min_dist / max_dist)

    df["semantic_cluster"] = labels
    df["cluster_probability"] = np.round(probabilities, 4)
    df["cluster_method"] = "kmeans_multilingual_embeddings_v1"

    silhouette = silhouette_score(embeddings, labels)

    cluster_counts = (
        df["semantic_cluster"]
        .value_counts()
        .sort_index()
        .to_dict()
    )

    report = {
        "rows": int(len(df)),
        "n_clusters": N_CLUSTERS,
        "silhouette_score": round(float(silhouette), 4),
        "cluster_counts": {str(k): int(v) for k, v in cluster_counts.items()},
        "method": "KMeans over multilingual sentence embeddings"
    }

    import json
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    df.to_parquet(OUTPUT_FILE, index=False)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print("Archivo generado:", OUTPUT_FILE)
    print("Reporte:", REPORT_FILE)
    print(report)


if __name__ == "__main__":
    main()