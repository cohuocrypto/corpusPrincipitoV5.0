from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_FROZEN = ROOT / "data" / "frozen"
OUTPUT_GRAPHS = ROOT / "outputs" / "graphs"

RAW_FILES = {
    "en": DATA_RAW / "ElPrincipito_EN.txt",
    "es": DATA_RAW / "ElPrincipito_ES.txt",
    "fr": DATA_RAW / "ElPrincipito_FR.txt",
}

for p in [DATA_RAW, DATA_PROCESSED, DATA_FROZEN, OUTPUT_GRAPHS]:
    p.mkdir(parents=True, exist_ok=True)

EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
RANDOM_STATE = 42
N_CLUSTERS = 8
