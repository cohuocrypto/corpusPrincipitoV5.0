import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from src.config import DATA_PROCESSED, DATA_FROZEN

FILES_TO_FREEZE = [
    "chapters.parquet",
    "dialogues_base.parquet",
    "dialogues_metadata.parquet",
    "dialogues_analytic_matrix.parquet",
    "dialogue_embeddings.npy",
    "phase11_validation_report.json",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="v4_0_phase11")
    args = parser.parse_args()
    version_dir = DATA_FROZEN / args.version
    version_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "version": args.version,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "description": "Corpus multilingüe enriquecido con metadatos narrativos, constructos afectivos, variables sociotécnicas, embeddings y clusters semánticos.",
        "files": {}
    }
    for name in FILES_TO_FREEZE:
        src = DATA_PROCESSED / name
        if not src.exists():
            print(f"WARN: no existe {src}, se omite")
            continue
        dst = version_dir / name
        shutil.copy2(src, dst)
        manifest["files"][name] = {"sha256": sha256(dst), "bytes": dst.stat().st_size}
    (version_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("OK 05_freeze_version", version_dir)

if __name__ == "__main__":
    main()
