import json
import re
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "data" / "interim" / "dialogues_v2_characters.parquet"
OUTPUT_FILE = ROOT / "data" / "processed" / "dialogues_v2_enriched.parquet"
OUTPUT_CSV = ROOT / "data" / "processed" / "dialogues_v2_enriched.csv"

LEXICON_FILE = ROOT / "config" / "emotion_lexicon_v2.json"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


POSITIVE_WORDS = [
    "love", "friend", "happy", "beautiful", "unique", "important", "smile", "laugh",
    "amor", "amigo", "feliz", "hermoso", "único", "importante", "sonreír", "reír",
    "aimer", "ami", "heureux", "beau", "unique", "important", "sourire", "rire"
]

NEGATIVE_WORDS = [
    "sad", "alone", "death", "die", "cry", "tears", "fear", "danger", "absurd",
    "triste", "solo", "muerte", "morir", "llorar", "lágrimas", "miedo", "peligro", "absurdo",
    "triste", "seul", "mort", "mourir", "pleurer", "larmes", "peur", "danger", "absurde"
]


def normalize(text):
    text = str(text).lower()
    text = re.sub(r"[^\w\sáéíóúñàâêîôûçüœ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_lexicon():
    if not LEXICON_FILE.exists():
        raise FileNotFoundError(f"No existe lexicon emocional: {LEXICON_FILE}")

    with open(LEXICON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def count_matches(text, terms):
    text_norm = normalize(text)
    count = 0

    for term in terms:
        term_norm = normalize(term)

        if " " in term_norm:
            if term_norm in text_norm:
                count += 1
        else:
            if re.search(rf"\b{re.escape(term_norm)}\b", text_norm):
                count += 1

    return count


def question_score(text):
    text_norm = normalize(text)

    question_terms = [
        "?", "why", "what", "where", "when", "how",
        "por qué", "qué", "dónde", "cuándo", "cómo",
        "pourquoi", "quoi", "où", "quand", "comment"
    ]

    score = 0

    if "?" in str(text):
        score += 2

    for term in question_terms:
        if term in text_norm:
            score += 1

    return score


def base_emotion_scores(dialogue, lexicon):
    scores = {}

    for emotion, terms in lexicon.items():
        scores[emotion] = count_matches(dialogue, terms)

    scores["curiosity"] = scores.get("curiosity", 0) + question_score(dialogue)

    return scores


def character_context_boost(scores, character, dialogue):
    text = normalize(dialogue)

    if character == "fox":
        scores["love"] = scores.get("love", 0) + 2
        if any(w in text for w in ["tame", "domesticar", "apprivoiser", "friend", "amigo", "ami"]):
            scores["love"] += 2

    elif character == "rose":
        scores["love"] = scores.get("love", 0) + 1
        scores["sadness"] = scores.get("sadness", 0) + 1

    elif character == "snake":
        scores["fear"] = scores.get("fear", 0) + 2
        scores["sadness"] = scores.get("sadness", 0) + 1

    elif character == "king":
        if any(w in text for w in ["order", "obey", "orden", "obedecer", "ordre", "obéir"]):
            scores["anger"] = scores.get("anger", 0) + 1

    elif character == "businessman":
        if any(w in text for w in ["absurd", "ridiculous", "absurdo", "ridículo", "absurde", "ridicule"]):
            scores["anger"] = scores.get("anger", 0) + 1

    elif character == "lamplighter":
        scores["sadness"] = scores.get("sadness", 0) + 1

    elif character == "little_prince":
        if "?" in dialogue:
            scores["curiosity"] = scores.get("curiosity", 0) + 2

    return scores


def chapter_context_boost(scores, chapter_id, character):
    try:
        chapter_id = int(chapter_id)
    except Exception:
        return scores

    # Capítulos aproximados frecuentes de El Principito
    # Rose: capítulos iniciales
    if chapter_id in [7, 8, 9]:
        scores["love"] = scores.get("love", 0) + 1
        scores["sadness"] = scores.get("sadness", 0) + 1

    # Asteroides / adultos: solo aumentar anger si hay marcas explícitas
    if chapter_id in [10, 11, 12, 13, 14, 15]:
       text = normalize(str(character))

    # Serpiente
    if chapter_id in [17, 26]:
        scores["fear"] = scores.get("fear", 0) + 1
        scores["sadness"] = scores.get("sadness", 0) + 1

    # Zorro
    if chapter_id in [21]:
        scores["love"] = scores.get("love", 0) + 2
        scores["sadness"] = scores.get("sadness", 0) + 1

    return scores


def choose_emotion(scores):
    total = sum(scores.values())

    if total == 0:
        return "neutral", 0.0

    emotion = max(scores, key=scores.get)
    best = scores[emotion]

    emotion_score = round(best / total, 4)

    return emotion, emotion_score


def compute_polarity(dialogue):
    pos = count_matches(dialogue, POSITIVE_WORDS)
    neg = count_matches(dialogue, NEGATIVE_WORDS)

    total = pos + neg

    if total == 0:
        return 0.0

    return round((pos - neg) / total, 4)


def compute_subjectivity(dialogue, emotion, emotion_score):
    text = normalize(dialogue)

    subjective_markers = [
        "i", "me", "my", "feel", "think", "want", "need",
        "yo", "me", "mi", "siento", "pienso", "quiero", "necesito",
        "je", "moi", "mon", "sens", "pense", "veux", "besoin"
    ]

    marker_count = count_matches(text, subjective_markers)

    base = 0.0

    if emotion != "neutral":
        base += 0.25

    base += min(0.40, emotion_score * 0.40)
    base += min(0.35, marker_count * 0.10)

    return round(min(1.0, base), 4)


def enrich_row(row, lexicon):
    dialogue = row["dialogue"]
    character = row.get("character", "unknown")
    chapter_id = row.get("chapter_id", None)

    scores = base_emotion_scores(dialogue, lexicon)
    scores = character_context_boost(scores, character, dialogue)
    scores = chapter_context_boost(scores, chapter_id, character)

    emotion, emotion_score = choose_emotion(scores)
    polarity = compute_polarity(dialogue)
    subjectivity = compute_subjectivity(dialogue, emotion, emotion_score)

    return pd.Series({
        "emotion": emotion,
        "emotion_score": emotion_score,
        "polarity": polarity,
        "subjectivity": subjectivity,
        "affect_method": "multilingual_lexicon_character_context_v2"
    })


def main():
    print("=== V2.1 Emotion and Polarity Improved ===")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"No existe archivo de entrada: {INPUT_FILE}")

    df = pd.read_parquet(INPUT_FILE)
    lexicon = load_lexicon()

    affect_df = df.apply(
        lambda row: enrich_row(row, lexicon),
        axis=1
    )

    df = pd.concat(
        [
            df.drop(
                columns=[
                    "emotion",
                    "emotion_score",
                    "polarity",
                    "subjectivity",
                    "affect_method"
                ],
                errors="ignore"
            ),
            affect_df
        ],
        axis=1
    )

    df.to_parquet(OUTPUT_FILE, index=False)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print("Archivo generado:", OUTPUT_FILE)
    print("CSV generado:", OUTPUT_CSV)
    print("Registros:", len(df))

    print("\nDistribución emocional:")
    print(df["emotion"].value_counts())

    print("\nPorcentajes:")
    print(round(df["emotion"].value_counts(normalize=True) * 100, 2))

    print("\nPolaridad promedio:", round(df["polarity"].mean(), 4))
    print("Subjetividad promedio:", round(df["subjectivity"].mean(), 4))


if __name__ == "__main__":
    main()