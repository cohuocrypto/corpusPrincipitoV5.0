import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent

VERSION = "v5_0_frozen"
FROZEN_DIR = ROOT / "data" / "frozen" / VERSION

FILES_TO_FREEZE = [
    ROOT / "data" / "processed" / "dialogues_v5_semantic_clusters.parquet",
    ROOT / "data" / "processed" / "dialogues_v5_semantic_clusters.csv",
    ROOT / "data" / "processed" / "v5_validation_report.json",
    ROOT / "data" / "processed" / "semantic_alignment_report.json",
    ROOT / "data" / "processed" / "semantic_cluster_report.json"
]


def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)

    return h.hexdigest()


def main():
    FROZEN_DIR.mkdir(parents=True, exist_ok=True)

    manifest = {
        "version": VERSION,
        "status": "frozen",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "files": []
    }

    for file_path in FILES_TO_FREEZE:
        if not file_path.exists():
            raise FileNotFoundError(f"No existe: {file_path}")

        target = FROZEN_DIR / file_path.name
        shutil.copy2(file_path, target)

        manifest["files"].append({
            "file": file_path.name,
            "sha256": sha256_file(target),
            "size_bytes": target.stat().st_size
        })

    with open(FROZEN_DIR / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    summary = {
        "version": VERSION,
        "status": "frozen",
        "description": "Corpus Principito V5.0 with narrative enrichment, emotion annotation, semantic alignment and clustering.",
        "main_file": "dialogues_v5_semantic_clusters.parquet",
        "created_at": manifest["created_at"]
    }

    with open(FROZEN_DIR / "corpus.summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("Frozen release created:", FROZEN_DIR)


if __name__ == "__main__":
    main()