import json
import re
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "data" / "processed" / "dialogues_base.parquet"
OUTPUT_DIR = ROOT / "data" / "interim"
OUTPUT_FILE = OUTPUT_DIR / "dialogues_v2_characters.parquet"

RULES_FILE = ROOT / "config" / "character_rules.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_rules():
    if not RULES_FILE.exists():
        raise FileNotFoundError(f"No existe el archivo de reglas: {RULES_FILE}")

    with open(RULES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize(text):
    text = str(text).lower()
    text = re.sub(r"[^\w\sáéíóúñàâêîôûçü]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def keyword_score(text, keywords):
    text_norm = normalize(text)
    score = 0

    for kw in keywords:
        kw_norm = normalize(kw)
        if re.search(rf"\b{re.escape(kw_norm)}\b", text_norm):
            score += 1

    return score


def detect_by_keywords(dialogue, rules):
    scores = {}

    for character, keywords in rules.items():
        scores[character] = keyword_score(dialogue, keywords)

    best_character = max(scores, key=scores.get)
    best_score = scores[best_character]

    if best_score == 0:
        return "unknown", 0.0, "no_match"

    confidence = min(0.95, 0.55 + best_score * 0.10)

    return best_character, confidence, "keyword_rules"


def apply_keyword_detection(df, rules):
    characters = []
    confidences = []
    methods = []

    for _, row in df.iterrows():
        character, confidence, method = detect_by_keywords(
            row["dialogue"],
            rules
        )
        characters.append(character)
        confidences.append(confidence)
        methods.append(method)

    df["character"] = characters
    df["speaker"] = characters
    df["speaker_confidence"] = confidences
    df["attribution_method"] = methods

    return df


def propagate_between_same_speakers(df):
    df = df.sort_values(
        ["language", "chapter_id", "dialogue_id"]
    ).reset_index(drop=True)

    for i in range(1, len(df) - 1):
        current = df.loc[i, "character"]

        if current != "unknown":
            continue

        same_language = (
            df.loc[i - 1, "language"] == df.loc[i, "language"]
            and df.loc[i + 1, "language"] == df.loc[i, "language"]
        )

        same_chapter = (
            df.loc[i - 1, "chapter_id"] == df.loc[i, "chapter_id"]
            and df.loc[i + 1, "chapter_id"] == df.loc[i, "chapter_id"]
        )

        same_speaker = (
            df.loc[i - 1, "character"] == df.loc[i + 1, "character"]
            and df.loc[i - 1, "character"] != "unknown"
        )

        if same_language and same_chapter and same_speaker:
            speaker = df.loc[i - 1, "character"]
            df.loc[i, "character"] = speaker
            df.loc[i, "speaker"] = speaker
            df.loc[i, "speaker_confidence"] = 0.70
            df.loc[i, "attribution_method"] = "sandwich_propagation"

    return df


def propagate_by_previous_speaker(df, window=2):
    df = df.sort_values(
        ["language", "chapter_id", "dialogue_id"]
    ).reset_index(drop=True)

    for i in range(len(df)):
        if df.loc[i, "character"] != "unknown":
            continue

        current_lang = df.loc[i, "language"]
        current_chapter = df.loc[i, "chapter_id"]

        previous_candidates = []

        for j in range(max(0, i - window), i):
            if (
                df.loc[j, "language"] == current_lang
                and df.loc[j, "chapter_id"] == current_chapter
                and df.loc[j, "character"] != "unknown"
            ):
                previous_candidates.append(df.loc[j, "character"])

        if previous_candidates:
            speaker = previous_candidates[-1]
            df.loc[i, "character"] = speaker
            df.loc[i, "speaker"] = speaker
            df.loc[i, "speaker_confidence"] = 0.55
            df.loc[i, "attribution_method"] = "previous_speaker_window"

    return df


def propagate_by_chapter_dominance(df, threshold=0.55):
    groups = df.groupby(["language", "chapter_id"])

    for (lang, chapter), group in groups:
        known = group[group["character"] != "unknown"]

        if len(known) < 3:
            continue

        distribution = known["character"].value_counts(normalize=True)
        dominant_character = distribution.index[0]
        dominance = distribution.iloc[0]

        if dominance >= threshold:
            idx_unknown = group[group["character"] == "unknown"].index

            df.loc[idx_unknown, "character"] = dominant_character
            df.loc[idx_unknown, "speaker"] = dominant_character
            df.loc[idx_unknown, "speaker_confidence"] = 0.60
            df.loc[idx_unknown, "attribution_method"] = "chapter_dominance"

    return df


def add_record_id_if_missing(df):
    if "record_id" not in df.columns:
        df["record_id"] = [
            f"{row.language}_ch{int(row.chapter_id):02d}_dlg{i:04d}"
            for i, row in df.iterrows()
        ]
    return df


def add_dialogue_id_if_missing(df):
    if "dialogue_id" not in df.columns:
        df["dialogue_id"] = (
            df.groupby(["language", "chapter_id"])
            .cumcount()
        )
    return df


def main():
    print("=== V2.1 Character Detection Improved ===")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"No existe archivo de entrada: {INPUT_FILE}")

    df = pd.read_parquet(INPUT_FILE)

    df = add_dialogue_id_if_missing(df)
    df = add_record_id_if_missing(df)

    rules = load_rules()

    print("Registros de entrada:", len(df))

    df = apply_keyword_detection(df, rules)
    df = propagate_between_same_speakers(df)
    df = propagate_by_previous_speaker(df, window=2)
    df = propagate_by_chapter_dominance(df, threshold=0.55)

    df.to_parquet(OUTPUT_FILE, index=False)

    print("Archivo generado:", OUTPUT_FILE)
    print("\nDistribución de personajes:")
    print(df["character"].value_counts())

    total = len(df)
    unknown = int((df["character"] == "unknown").sum())
    coverage = round((1 - unknown / total) * 100, 2)

    print("\nCobertura:")
    print(f"Total: {total}")
    print(f"Unknown: {unknown}")
    print(f"Cobertura personajes: {coverage}%")

    print("\nMétodos usados:")
    print(df["attribution_method"].value_counts())


if __name__ == "__main__":
    main()