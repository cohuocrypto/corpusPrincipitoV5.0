import re
import unicodedata
from pathlib import Path
import chardet


def load_text_mac(path: Path) -> str:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo requerido: {path}")
    raw = path.read_bytes()
    detected = chardet.detect(raw)
    encodings_to_try = [detected.get("encoding"), "utf-8", "utf-8-sig", "mac_roman", "cp1252", "latin-1"]
    for enc in encodings_to_try:
        if not enc:
            continue
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return raw.decode("utf-8", errors="ignore")


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    replacements = {
        "“": '"', "”": '"', "‘": "'", "’": "'", "«": '"', "»": '"',
        "–": "—", "−": "—", "\ufeff": ""
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"Page\s+\d+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<PARSED TEXT.*?>", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def repair_ocr_text(text: str) -> str:
    text = re.sub(r"\bY es\b", "Yes", text)
    text = re.sub(r"\bY ou\b", "You", text)
    text = re.sub(r"\bcan not\b", "cannot", text)
    text = re.sub(r"([a-záéíóúñàâêîôûç])-\s*\n\s*([a-záéíóúñàâêîôûç])", r"\1\2", text)
    return text


def load_clean_corpus(paths: dict) -> dict:
    corpus = {}
    for lang, path in paths.items():
        text = load_text_mac(path)
        text = normalize_text(text)
        text = repair_ocr_text(text)
        corpus[lang] = text
        print(f"{lang}: {len(text):,} caracteres")
    return corpus
