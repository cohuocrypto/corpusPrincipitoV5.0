import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config import RAW_FILES, DATA_PROCESSED
from src.io_text import load_clean_corpus
from src.segmentation import build_chapters_and_dialogues


def main():
    corpus = load_clean_corpus(RAW_FILES)
    chapters_df, dialogues_df = build_chapters_and_dialogues(corpus)
    chapters_df.to_csv(DATA_PROCESSED / "chapters_multilingual.csv", index=False, encoding="utf-8-sig")
    dialogues_df.to_csv(DATA_PROCESSED / "dialogues_multilingual.csv", index=False, encoding="utf-8-sig")
    chapters_df.to_parquet(DATA_PROCESSED / "chapters.parquet", engine="pyarrow")
    dialogues_df.to_parquet(DATA_PROCESSED / "dialogues_base.parquet", engine="pyarrow")
    print("OK 01_build_base_corpus")
    print("chapters:", chapters_df.shape, "dialogues:", dialogues_df.shape)

if __name__ == "__main__":
    main()
