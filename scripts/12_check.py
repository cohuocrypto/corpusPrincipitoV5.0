import pandas as pd
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
PARQUET_FILE = (
    ROOT
    / "data"
    / "processed"
    / "dialogues_v2_enriched.parquet"
)
df = pd.read_parquet(PARQUET_FILE)
#print(df.columns)
print(df["subjectivity"].describe())