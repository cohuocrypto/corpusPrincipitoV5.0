import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
from src.config import DATA_PROCESSED, EMBEDDING_MODEL, N_CLUSTERS, RANDOM_STATE


def main():
    input_path = DATA_PROCESSED / "dialogues_metadata.parquet"
    if not input_path.exists():
        raise FileNotFoundError("Ejecuta primero scripts/02_enrich_metadata.py")
    df = pd.read_parquet(input_path)
    texts = df["dialogue"].fillna("").tolist()
    model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)
    n_clusters = min(N_CLUSTERS, max(2, len(df)))
    labels = KMeans(n_clusters=n_clusters, random_state=RANDOM_STATE, n_init="auto").fit_predict(embeddings)
    df["semantic_cluster"] = labels.astype(int)
    # Parquet acepta arrays/listas; CSV guardará representación textual.
    df["embedding"] = embeddings.tolist()
    np.save(DATA_PROCESSED / "dialogue_embeddings.npy", embeddings)
    df.to_parquet(DATA_PROCESSED / "dialogues_analytic_matrix.parquet", engine="pyarrow")
    df.to_csv(DATA_PROCESSED / "dialogues_analytic_matrix.csv", index=False, encoding="utf-8-sig")
    print("OK 03_embeddings_clusters", df.shape)
    print("embedding_dim:", embeddings.shape[1])

if __name__ == "__main__":
    main()
