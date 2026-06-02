import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
from src.config import DATA_PROCESSED
from src.narrative_metadata import infer_character, infer_emotion, polarity_score, detect_constructs, primary_construct, sociotechnical_variable


def main():
    input_path = DATA_PROCESSED / "dialogues_base.parquet"
    if not input_path.exists():
        raise FileNotFoundError("Ejecuta primero scripts/01_build_base_corpus.py")
    df = pd.read_parquet(input_path)
    df["character"] = df["dialogue"].apply(infer_character)
    df["emotion"] = df["dialogue"].apply(infer_emotion)
    df["polarity"] = df["dialogue"].apply(polarity_score)
    df["constructs"] = df["dialogue"].apply(detect_constructs)
    df["primary_construct"] = df["constructs"].apply(primary_construct)
    df["sociotechnical_variable"] = df["primary_construct"].apply(sociotechnical_variable)
    df.to_parquet(DATA_PROCESSED / "dialogues_metadata.parquet", engine="pyarrow")
    df.to_csv(DATA_PROCESSED / "dialogues_metadata.csv", index=False, encoding="utf-8-sig")
    print("OK 02_enrich_metadata", df.shape)

if __name__ == "__main__":
    main()
