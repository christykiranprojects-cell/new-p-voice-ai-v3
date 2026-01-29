import re

STOPWORDS = {
    "AND", "SAID", "TOLD", "TELL",
    "PLEASE", "GIVE", "TAKE"
}

NOISE_TOKENS = {
    "THE", "A", "AN", "OF", "TO", "FOR"
}


def normalize_for_matching(text: str) -> str:
    """
    Normalizes medicine names for fuzzy matching.
    IMPORTANT:
    - Preserves short variant tokens (Z, DS, XR, CV, etc.)
    - Removes conversational noise only
    """

    if not text:
        return ""

    text = text.upper()
    text = re.sub(r"[^A-Z0-9\. ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    tokens = []

    for t in text.split():
        if t in STOPWORDS or t in NOISE_TOKENS:
            continue

        # 🔒 Preserve short variant tokens
        if len(t) <= 2:
            tokens.append(t)
        else:
            tokens.append(t)

    return " ".join(tokens)
