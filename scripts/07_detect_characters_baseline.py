"""
07_detect_characters.py
V2.0 - Deteccion inicial de personajes / hablantes.

Entrada preferida:
    data/frozen/v1_0/dialogues.parquet
Fallbacks:
    data/processed/dialogues.parquet
    data/processed/dialogues_multilingual.csv

Salida:
    data/interim/dialogues_v2_characters.parquet
    data/interim/dialogues_v2_characters.csv

Notas:
- No modifica la V1 congelada.
- Usa reglas transparentes y reproducibles.
- El objetivo es crear una primera capa narrativa: character, speaker_confidence, attribution_method.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_INTERIM = ROOT / "data" / "interim"
DATA_FROZEN_V1 = ROOT / "data" / "frozen" / "v1_0"
DATA_INTERIM.mkdir(parents=True, exist_ok=True)

INPUT_CANDIDATES = [
    DATA_FROZEN_V1 / "dialogues.parquet",
    DATA_PROCESSED / "dialogues.parquet",
    DATA_PROCESSED / "dialogues_multilingual.csv",
]

OUTPUT_PARQUET = DATA_INTERIM / "dialogues_v2_characters.parquet"
OUTPUT_CSV = DATA_INTERIM / "dialogues_v2_characters.csv"

# Diccionario multilingue de pistas lexicas por personaje.
# Se puede ampliar sin cambiar el resto del pipeline.
CHARACTER_PATTERNS: Dict[str, List[str]] = {
    "little_prince": [
        r"\bpetit prince\b", r"\blittle prince\b", r"\bprincipito\b",
        r"\bmon ami\b", r"\bmy friend\b", r"\bmi amigo\b",
    ],
    "fox": [
        r"\brenard\b", r"\bfox\b", r"\bzorro\b",
        r"\bapprivois", r"\btame\b", r"\bdomestic",
    ],
    "rose": [
        r"\brose\b", r"\brosa\b", r"\bfleur\b", r"\bflower\b", r"\bflor\b",
        r"\bepine", r"\bthorn", r"\bespina",
    ],
    "king": [
        r"\broi\b", r"\bking\b", r"\brey\b", r"\bsire\b", r"\bmajest",
        r"\border\b", r"\bordeno\b", r"\bordonne",
    ],
    "businessman": [
        r"\bbusinessman\b", r"\bhomme d'affaires\b", r"\bhombre de negocios\b",
        r"\bstars\b", r"\bestrellas\b", r"\betoiles\b", r"\bcount",
        r"\bcompte\b", r"\bcuento\b",
    ],
    "lamplighter": [
        r"\blamplighter\b", r"\ballumeur\b", r"\bfarolero\b",
        r"\blamp\b", r"\blanterne\b", r"\bfarol\b", r"\bconsigne\b",
    ],
    "geographer": [
        r"\bgeographer\b", r"\bgeographe\b", r"\bgeografo\b", r"\bgeógrafo\b",
        r"\bexplorer\b", r"\bexplorateur\b", r"\bexplorador\b",
    ],
    "snake": [
        r"\bsnake\b", r"\bserpent\b", r"\bserpiente\b",
        r"\bvenom\b", r"\bpoison\b", r"\bveneno\b",
    ],
    "drunkard": [
        r"\bdrunkard\b", r"\bbuveur\b", r"\bbebedor\b",
        r"\bdrink\b", r"\bboire\b", r"\bbeber\b",
    ],
    "conceited_man": [
        r"\bconceited\b", r"\bvaniteux\b", r"\bvanidoso\b",
        r"\badmirer\b", r"\badmirateur\b", r"\badmirador\b",
    ],
    "switchman": [
        r"\bswitchman\b", r"\baiguilleur\b", r"\bguardagujas\b",
        r"\btrain\b", r"\btren\b", r"\bvoyageurs\b", r"\btravelers\b",
    ],
    "merchant": [
        r"\bmerchant\b", r"\bmarchand\b", r"\bcomerciante\b",
        r"\bpills\b", r"\bpilules\b", r"\bpildoras\b", r"\bpíldoras\b",
    ],
    "pilot_narrator": [
        r"\bpilot\b", r"\bpilote\b", r"\bpiloto\b", r"\bavion\b", r"\bplane\b", r"\bdesert\b", r"\bdesierto\b",
    ],
}

# Pistas de estilo para dialogos muy conocidos sin contexto amplio.
SIGNATURE_RULES: List[Tuple[str, str, float]] = [
    (r"domest|apprivois|tame", "fox", 0.95),
    (r"responsable.*domest|responsible.*tamed|responsable.*apprivois", "fox", 0.98),
    (r"dessine-moi un mouton|draw me a sheep|dibujame un cordero|dibújame un cordero", "little_prince", 0.98),
    (r"epines|thorns|espinas", "rose", 0.85),
    (r"consigne|orders are orders|la consigna|ordenes son ordenes|órdenes son órdenes", "lamplighter", 0.90),
    (r"je possede les etoiles|i own the stars|poseo las estrellas", "businessman", 0.95),
]


def read_dialogues() -> pd.DataFrame:
    for path in INPUT_CANDIDATES:
        if path.exists():
            print(f"Leyendo entrada: {path}")
            if path.suffix == ".parquet":
                return pd.read_parquet(path)
            return pd.read_csv(path)
    tried = "\n".join(str(p) for p in INPUT_CANDIDATES)
    raise FileNotFoundError(f"No se encontro archivo de dialogos. Rutas probadas:\n{tried}")


def get_text_column(df: pd.DataFrame) -> str:
    for candidate in ["dialogue", "text", "sentence", "segment"]:
        if candidate in df.columns:
            return candidate
    raise ValueError("No encuentro columna de texto. Usa una columna llamada dialogue, text, sentence o segment.")


def normalize_for_rules(text: str) -> str:
    text = str(text).lower()
    replacements = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n",
        "à": "a", "â": "a", "ê": "e", "î": "i", "ô": "o", "û": "u", "ç": "c",
        "ë": "e", "ï": "i", "ü": "u",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return re.sub(r"\s+", " ", text).strip()


def infer_character(text: str) -> Tuple[str, float, str]:
    clean = normalize_for_rules(text)

    for pattern, character, confidence in SIGNATURE_RULES:
        if re.search(pattern, clean, flags=re.IGNORECASE):
            return character, confidence, "signature_rule"

    scores = {}
    for character, patterns in CHARACTER_PATTERNS.items():
        hits = sum(1 for pattern in patterns if re.search(pattern, clean, flags=re.IGNORECASE))
        if hits > 0:
            scores[character] = hits

    if not scores:
        return "unknown", 0.20, "no_rule_match"

    best_character = max(scores, key=scores.get)
    best_score = scores[best_character]
    total = sum(scores.values())
    confidence = min(0.85, 0.45 + (best_score / total) * 0.35 + min(best_score, 3) * 0.05)
    return best_character, round(confidence, 3), "lexical_rule"


def main() -> None:
    df = read_dialogues().copy()
    text_col = get_text_column(df)

    if "dialogue_id" not in df.columns:
        df.insert(0, "dialogue_id", range(1, len(df) + 1))

    inferred = df[text_col].apply(infer_character)
    df["character"] = inferred.apply(lambda x: x[0])
    df["speaker"] = df["character"]
    df["speaker_confidence"] = inferred.apply(lambda x: x[1])
    df["attribution_method"] = inferred.apply(lambda x: x[2])

    # Asegura columna chapter_id para compatibilidad. Si V1 no la tiene, queda pendiente.
    if "chapter_id" not in df.columns:
        df["chapter_id"] = pd.NA

    df.to_parquet(OUTPUT_PARQUET, index=False)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print("Archivo generado:", OUTPUT_PARQUET)
    print("Registros:", len(df))
    print("Distribucion de personajes:")
    print(df["character"].value_counts(dropna=False).head(20))


if __name__ == "__main__":
    main()
