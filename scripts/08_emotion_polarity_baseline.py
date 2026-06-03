"""
08_emotion_polarity.py
V2.0 - Enriquecimiento afectivo inicial.

Entrada:
    data/interim/dialogues_v2_characters.parquet

Salida:
    data/processed/dialogues_v2_enriched.parquet
    data/processed/dialogues_v2_enriched.csv

Variables nuevas:
    emotion
    emotion_score
    polarity
    subjectivity
    affect_method

Notas:
- Implementa un enfoque lexicon-based multilingue, explicable y reproducible.
- En una V2.1 puede sustituirse por modelos transformer multilingues.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_INTERIM = ROOT / "data" / "interim"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

INPUT_FILE = DATA_INTERIM / "dialogues_v2_characters.parquet"
OUTPUT_PARQUET = DATA_PROCESSED / "dialogues_v2_enriched.parquet"
OUTPUT_CSV = DATA_PROCESSED / "dialogues_v2_enriched.csv"

EMOTION_LEXICON: Dict[str, List[str]] = {
    "joy": [
        "joy", "happy", "happiness", "laugh", "smile", "play", "glad",
        "alegria", "feliz", "risa", "sonrisa", "jugar", "contento",
        "joie", "heureux", "rire", "sourire", "jouer", "content",
    ],
    "sadness": [
        "sad", "alone", "lonely", "cry", "tears", "miss", "sorrow",
        "triste", "solo", "soledad", "llorar", "lagrimas", "lágrimas", "pena",
        "triste", "seul", "solitude", "pleurer", "larmes", "chagrin",
    ],
    "fear": [
        "fear", "afraid", "danger", "death", "die", "bite", "venom",
        "miedo", "temor", "peligro", "muerte", "morir", "morder", "veneno",
        "peur", "danger", "mort", "mourir", "mordre", "venin",
    ],
    "anger": [
        "anger", "angry", "furious", "annoyed", "irritated", "hate",
        "enojo", "enojado", "furioso", "molesto", "irritado", "odio",
        "colere", "colère", "furieux", "agace", "agacé", "haine",
    ],
    "love": [
        "love", "friend", "friendship", "heart", "tame", "responsible", "care",
        "amor", "amigo", "amistad", "corazon", "corazón", "domesticar", "responsable", "cuidar",
        "amour", "ami", "amitie", "amitié", "coeur", "cœur", "apprivoiser", "responsable", "soin",
    ],
    "curiosity": [
        "why", "what", "where", "how", "question", "understand", "explore",
        "por que", "por qué", "que", "qué", "donde", "dónde", "como", "cómo", "pregunta", "comprender", "explorar",
        "pourquoi", "quoi", "ou", "où", "comment", "question", "comprendre", "explorer",
    ],
}

POSITIVE_WORDS = set("""
joy happy happiness laugh smile play glad good beautiful love friend friendship heart responsible care
alegria feliz risa sonrisa jugar contento bueno hermoso amor amigo amistad corazon corazón responsable cuidar
joie heureux rire sourire jouer content bon beau amour ami amitie amitié coeur cœur responsable soin
""".split())

NEGATIVE_WORDS = set("""
sad alone lonely cry tears sorrow fear afraid danger death die bite venom anger angry furious annoyed irritated hate bad
triste solo soledad llorar lagrimas lágrimas pena miedo temor peligro muerte morir morder veneno enojo enojado furioso molesto irritado odio malo
seul solitude pleurer larmes chagrin peur danger mort mourir mordre venin colere colère furieux agace agacé haine mauvais
""".split())

SUBJECTIVE_MARKERS = set("""
i me my mine feel think believe want wish hope love hate fear
yo mi mio siento creo quiero deseo espero amo odio temo
je moi mon mien sens crois veux desire désire espere espère aime deteste déteste crains
""".split())


def get_text_column(df: pd.DataFrame) -> str:
    for candidate in ["dialogue", "text", "sentence", "segment"]:
        if candidate in df.columns:
            return candidate
    raise ValueError("No encuentro columna textual: dialogue, text, sentence o segment.")


def normalize(text: str) -> str:
    text = str(text).lower()
    replacements = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n",
        "à": "a", "â": "a", "ê": "e", "î": "i", "ô": "o", "û": "u", "ç": "c",
        "ë": "e", "ï": "i", "ü": "u",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return re.sub(r"\s+", " ", text).strip()


def tokens(text: str) -> List[str]:
    return re.findall(r"[a-zA-ZáéíóúñÁÉÍÓÚÑàâêîôûçÀÂÊÎÔÛÇ]+", normalize(text))


def infer_emotion(text: str) -> Tuple[str, float]:
    clean = normalize(text)
    scores = {}
    for emotion, words in EMOTION_LEXICON.items():
        score = 0
        for word in words:
            pattern = r"\b" + re.escape(normalize(word)) + r"\b"
            if re.search(pattern, clean):
                score += 1
        scores[emotion] = score

    best_emotion = max(scores, key=scores.get)
    best_score = scores[best_emotion]
    total = sum(scores.values())

    if best_score == 0:
        return "neutral", 0.0
    return best_emotion, round(best_score / total, 3)


def infer_polarity_subjectivity(text: str) -> Tuple[float, float]:
    toks = tokens(text)
    if not toks:
        return 0.0, 0.0

    pos = sum(1 for t in toks if t in POSITIVE_WORDS)
    neg = sum(1 for t in toks if t in NEGATIVE_WORDS)
    subj = sum(1 for t in toks if t in SUBJECTIVE_MARKERS)

    affective_total = pos + neg
    if affective_total == 0:
        polarity = 0.0
    else:
        polarity = (pos - neg) / affective_total

    subjectivity = min(1.0, (affective_total + subj) / max(1, len(toks)) * 3)
    return round(float(polarity), 3), round(float(subjectivity), 3)


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"No existe {INPUT_FILE}. Ejecuta primero: python3 scripts/07_detect_characters.py"
        )

    df = pd.read_parquet(INPUT_FILE).copy()
    text_col = get_text_column(df)

    emotion_result = df[text_col].apply(infer_emotion)
    polarity_result = df[text_col].apply(infer_polarity_subjectivity)

    df["emotion"] = emotion_result.apply(lambda x: x[0])
    df["emotion_score"] = emotion_result.apply(lambda x: x[1])
    df["polarity"] = polarity_result.apply(lambda x: x[0])
    df["subjectivity"] = polarity_result.apply(lambda x: x[1])
    df["affect_method"] = "multilingual_lexicon_v1"

    df.to_parquet(OUTPUT_PARQUET, index=False)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print("Archivo generado:", OUTPUT_PARQUET)
    print("Registros:", len(df))
    print("Distribucion emocional:")
    print(df["emotion"].value_counts(dropna=False))
    print("Polaridad promedio:", round(df["polarity"].mean(), 4))


if __name__ == "__main__":
    main()
