# ======================================================
# TOKENIZATION & NORMALIZATION RULES
# ======================================================

import re

STOPWORD_TOKENS = {"AND", "SAID"}


def tokenize(text: str):
    """
    Tokenize while preserving decimals and punctuation
    """
    return re.findall(r"[A-Z0-9\.]+|[,]", text.upper())


def split_alpha_numeric(token: str):
    """
    Split glued alpha-numeric tokens safely.
    - ANXILOR1  → ANXILOR 1
    - DOLO650   → DOLO 650
    - DO NOT split decimals (2.5 stays 2.5)
    """
    if "." in token:
        return [token]

    m1 = re.match(r"^([A-Z]+)(\d+)$", token)
    if m1:
        return [m1.group(1), m1.group(2)]

    m2 = re.match(r"^(\d+)([A-Z]+)$", token)
    if m2:
        return [m2.group(1), m2.group(2)]

    return [token]


def normalize_tokens(tokens):
    out = []
    for tok in tokens:
        out.extend(split_alpha_numeric(tok))
    return out


def is_quantity(tok: str) -> bool:
    """
    Accept quantities like:
    4
    4.
    4,
    """
    return tok.rstrip(".,").isdigit()


def is_valid_medicine_name(name: str) -> bool:
    toks = name.split()
    return not (toks and toks[0] in STOPWORD_TOKENS)
