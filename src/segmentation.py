import re
import pandas as pd

CHAPTER_PATTERNS = {
    "es": r"(CAP[IÍ]TULO\s+[IVXLCDM]+|Cap[ií]tulo\s+\d+)",
    "fr": r"(CHAPITRE\s+[IVXLCDM]+|Chapitre\s+\d+)",
    "en": r"(CHAPTER\s+[IVXLCDM]+|Chapter\s+\d+)",
}


def split_chapters(text: str, lang: str) -> pd.DataFrame:
    pattern = CHAPTER_PATTERNS[lang]
    chunks = re.split(pattern, text, flags=re.IGNORECASE)
    chapters = []
    if len(chunks) < 3:
        chapters.append({"language": lang, "chapter_id": 1, "chapter_title": "FULL_TEXT", "chapter_text": text})
    else:
        for i in range(1, len(chunks), 2):
            title = chunks[i].strip()
            body = chunks[i + 1].strip() if i + 1 < len(chunks) else ""
            chapters.append({
                "language": lang,
                "chapter_id": len(chapters) + 1,
                "chapter_title": title,
                "chapter_text": body,
            })
    return pd.DataFrame(chapters)


def repair_broken_lines(text: str) -> str:
    lines = text.splitlines()
    repaired, buffer = [], ""
    for line in lines:
        line = line.strip()
        if not line:
            if buffer:
                repaired.append(buffer.strip())
                buffer = ""
            continue
        if line.startswith("—"):
            if buffer:
                repaired.append(buffer.strip())
            buffer = line
            continue
        if buffer and not buffer.endswith((".", "!", "?", ":", "…", '"')):
            buffer += " " + line
        else:
            if buffer:
                repaired.append(buffer.strip())
            buffer = line
    if buffer:
        repaired.append(buffer.strip())
    return "\n".join(repaired)


def extract_dialogues_from_chapter(text: str, lang: str, chapter_id: int, chapter_title: str) -> pd.DataFrame:
    rows = []
    quotes = re.findall(r'"([^\"]+)"', text)
    dashes = re.findall(r'^\s*[—-]\s*(.+)', text, flags=re.MULTILINE)
    candidates = quotes + dashes
    seen = set()
    for idx, dialogue in enumerate(candidates):
        d = re.sub(r"\s+", " ", dialogue.strip())
        if len(d.split()) < 3 or d in seen:
            continue
        seen.add(d)
        rows.append({
            "record_id": f"{lang}_ch{chapter_id:02d}_dlg{idx:04d}",
            "language": lang,
            "chapter_id": int(chapter_id),
            "chapter_title": chapter_title,
            "dialogue": d,
            "length_chars": len(d),
            "length_words": len(d.split()),
        })
    return pd.DataFrame(rows)


def build_chapters_and_dialogues(corpus: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    chapter_frames, dialogue_frames = [], []
    for lang, text in corpus.items():
        chapters = split_chapters(text, lang)
        chapters["chapter_text_clean"] = chapters["chapter_text"].apply(repair_broken_lines)
        chapter_frames.append(chapters)
        print(f"{lang}: capítulos detectados = {len(chapters)}")
        for _, row in chapters.iterrows():
            dialogue_frames.append(extract_dialogues_from_chapter(row["chapter_text_clean"], lang, row["chapter_id"], row["chapter_title"]))
    chapters_df = pd.concat(chapter_frames, ignore_index=True)
    dialogues_df = pd.concat([d for d in dialogue_frames if not d.empty], ignore_index=True)
    dialogues_df = dialogues_df.drop_duplicates(subset=["language", "chapter_id", "dialogue"]).reset_index(drop=True)
    dialogues_df["dialogue_id"] = [f"D{i:06d}" for i in range(len(dialogues_df))]
    return chapters_df, dialogues_df
