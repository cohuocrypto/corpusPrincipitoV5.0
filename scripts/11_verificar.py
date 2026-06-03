import pandas as pd
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
PARQUET_FILE = (
    ROOT
    / "data"
    / "interim"
    / "dialogues_v2_characters.parquet"
)
df = pd.read_parquet(PARQUET_FILE)
print(df.columns)
print(df.character.value_counts().head(20))


PARQUET_FILE = (
    ROOT
    / "data"
    / "processed"
    / "dialogues_v2_enriched.parquet"
)

df = pd.read_parquet(PARQUET_FILE)
print(df.columns)
print("=" * 60)
print("DISTRIBUCIÓN DE EMOCIONES")
print("=" * 60)

print(df["emotion"].value_counts())

print("\n")

print("=" * 60)
print("PORCENTAJES")
print("=" * 60)

print(
    round(
        df["emotion"].value_counts(normalize=True) * 100,
        2
    )
)

print("\n")

print("=" * 60)
print("POLARIDAD")
print("=" * 60)

print(df["polarity"].describe())

print("\n")

print("=" * 60)
print("SUBJETIVIDAD")
print("=" * 60)

print(df["subjectivity"].describe())


