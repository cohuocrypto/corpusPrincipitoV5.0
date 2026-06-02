import re
import numpy as np

CHARACTER_KEYWORDS = {
    "little_prince": ["little prince", "principito", "petit prince"],
    "narrator": ["i ", "yo ", "je ", "me ", "my ", "mi ", "mon "],
    "rose": ["rose", "rosa", "fleur", "flower"],
    "fox": ["fox", "zorro", "renard"],
    "king": ["king", "rey", "roi"],
    "businessman": ["businessman", "hombre de negocios", "business man"],
    "lamplighter": ["lamplighter", "farolero", "allumeur"],
    "geographer": ["geographer", "geógrafo", "geographe", "géographe"],
    "snake": ["snake", "serpiente", "serpent"],
    "switchman": ["switchman", "guardagujas", "aiguilleur"],
    "merchant": ["merchant", "comerciante", "marchand"],
    "conceited_man": ["conceited", "vanidoso", "vaniteux"],
    "drinker": ["drinker", "bebedor", "buveur"],
}

EMOTION_LEXICON = {
    "joy": ["happy", "glad", "alegr", "feliz", "content", "heureux", "joie", "smile"],
    "sadness": ["sad", "triste", "cry", "llor", "pleur", "lonely", "solitario", "seul"],
    "fear": ["fear", "miedo", "peur", "terrible", "danger", "peligro", "dangereux"],
    "anger": ["angry", "ira", "enojo", "fâch", "furious", "irrit"],
    "love": ["love", "amor", "aimer", "querer", "friend", "amigo", "ami"],
    "curiosity": ["why", "por qué", "pourquoi", "question", "pregunta", "demanda"],
    "neutral": []
}

POSITIVE = ["good", "bien", "bon", "beautiful", "hermos", "beau", "love", "amor", "friend", "amigo", "ami", "important", "importante"]
NEGATIVE = ["bad", "mal", "mauvais", "sad", "triste", "fear", "miedo", "peur", "alone", "solo", "seul", "danger", "peligro"]

CONSTRUCT_LEXICON = {
    "Meaning": ["meaning", "sentido", "signification", "essential", "esencial", "invisible"],
    "Responsibility": ["responsible", "responsable", "responsabilidad", "answerable"],
    "Trust Bond": ["tame", "domesticar", "apprivoiser", "friend", "amigo", "ami", "bond", "vínculo"],
    "Ritual": ["rite", "ritual", "habit", "costumbre", "same hour", "misma hora"],
    "Quality": ["beautiful", "hermosa", "beau", "quality", "calidad", "unique", "única"],
    "Automation": ["order", "orden", "obey", "obedecer", "machine", "automatic", "automático"],
    "Productivism": ["business", "negocios", "count", "contar", "own", "poseer", "profit"],
    "Theory": ["geographer", "geógrafo", "book", "libro", "science", "ciencia", "proof"],
    "Understanding": ["understand", "comprender", "entender", "comprendre", "learn", "aprender"],
    "Iteration": ["again", "otra vez", "encore", "repeat", "repetir", "return", "volver"],
    "Hidden Value": ["invisible", "hidden", "oculto", "secret", "secreto", "heart", "corazón"],
    "Sustainability": ["water", "agua", "eau", "desert", "desierto", "sustain", "cuidar"]
}

SOCIO_MAP = {
    "Meaning": "Purpose",
    "Responsibility": "Accountability",
    "Trust Bond": "Team Cohesion",
    "Ritual": "Process Awareness",
    "Quality": "Craftsmanship",
    "Automation": "Burnout Risk",
    "Productivism": "Burnout Risk",
    "Theory": "Continuous Learning",
    "Understanding": "Empathy",
    "Iteration": "Adaptability",
    "Hidden Value": "Value Perception",
    "Sustainability": "Sustainable Pace",
}


def infer_character(text: str) -> str:
    t = " " + text.lower() + " "
    scores = {c: sum(1 for kw in kws if kw in t) for c, kws in CHARACTER_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "unknown"


def infer_emotion(text: str) -> str:
    t = text.lower()
    scores = {e: sum(1 for kw in kws if kw in t) for e, kws in EMOTION_LEXICON.items() if e != "neutral"}
    if not scores or max(scores.values()) == 0:
        return "neutral"
    return max(scores, key=scores.get)


def polarity_score(text: str) -> float:
    t = text.lower()
    pos = sum(1 for kw in POSITIVE if kw in t)
    neg = sum(1 for kw in NEGATIVE if kw in t)
    if pos + neg == 0:
        return 0.0
    return float((pos - neg) / (pos + neg))


def detect_constructs(text: str) -> list[str]:
    t = text.lower()
    found = []
    for construct, kws in CONSTRUCT_LEXICON.items():
        if any(kw in t for kw in kws):
            found.append(construct)
    return found


def primary_construct(constructs: list[str]) -> str:
    return constructs[0] if constructs else "Unclassified"


def sociotechnical_variable(primary: str) -> str:
    return SOCIO_MAP.get(primary, "Unclassified")
