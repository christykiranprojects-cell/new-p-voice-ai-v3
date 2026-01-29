# ======================================================
# PHASE C — STRUCTURED BOUNDARY EXTRACTION
# PARAMETRIC START-BOUNDARY REPAIR
# ======================================================

from .boundary_rules import (
    tokenize,
    normalize_tokens,
    is_quantity,
    is_valid_medicine_name,
)

# ------------------------------------------------------
# PARAMETERS (TUNABLE, NOT HARD-CODED)
# ------------------------------------------------------

MAX_PREFIX_LEN = 4  # AND, AM, AN, OD, XR, etc.

# ------------------------------------------------------
# HELPERS
# ------------------------------------------------------

def _strip_leading_delimiters(text: str) -> str:
    while text.startswith(","):
        text = text[1:].lstrip()
    return text


def _skip_delimiters(tokens, idx):
    while idx < len(tokens) and tokens[idx] == ",":
        idx += 1
    return idx


def is_ml_token(tok: str) -> bool:
    return tok in {"ML", "MLS"}


def _attempt_parametric_prefix_merge(tokens):
    """
    Parametric ASR repair:
    AND PROX   → ANDPROX
    AN GEL     → ANGEL
    OD FAST    → ODFAST

    Conditions:
    - First token short (≤ MAX_PREFIX_LEN)
    - Second token alphabetic
    - Merged token forms a valid medicine name
    """
    if len(tokens) < 2:
        return tokens

    t1, t2 = tokens[0], tokens[1]

    if (
        len(t1) <= MAX_PREFIX_LEN
        and t1.isalpha()
        and t2.isalpha()
    ):
        merged = t1 + t2
        if is_valid_medicine_name(merged):
            return [merged] + tokens[2:]

    return tokens


# ------------------------------------------------------
# MEDICINE TYPE MATCHER
# ------------------------------------------------------

def match_medicine_type(tokens, idx, token_map, alias_lookup):
    for alias, parts in token_map.items():
        if tokens[idx:idx + len(parts)] == parts:
            return alias_lookup[alias], len(parts)
    return None, 0


# ------------------------------------------------------
# QUANTITY FINDER
# ------------------------------------------------------

def find_quantity(tokens, start_idx, lookahead=8):
    j = start_idx
    steps = 0

    while j < len(tokens) and steps <= lookahead:
        tok = tokens[j]

        if tok == ",":
            j += 1
            steps += 1
            continue

        if is_quantity(tok):
            return tok.rstrip("., "), j

        j += 1
        steps += 1

    return None, None


# ------------------------------------------------------
# CORE EXTRACTION
# ------------------------------------------------------

def extract_items(raw_transcript: str, snapshot: dict):
    tokens = normalize_tokens(tokenize(raw_transcript))

    alias_lookup = snapshot["alias_lookup"]
    token_map = snapshot["token_map"]

    items = []
    seen_order_lines = set()

    pos = 0
    seg_start = 0
    i = 0

    while i < len(tokens):
        med_type, tlen = match_medicine_type(tokens, i, token_map, alias_lookup)

        if med_type:
            qty, qty_idx = find_quantity(tokens, i + tlen)

            predicted_tokens = tokens[seg_start:i]

            # Strip trailing ML
            if predicted_tokens and is_ml_token(predicted_tokens[-1]):
                predicted_tokens = predicted_tokens[:-1]

            # 🔒 PARAMETRIC PREFIX REPAIR
            predicted_tokens = _attempt_parametric_prefix_merge(
                predicted_tokens
            )

            predicted = _strip_leading_delimiters(
                " ".join(predicted_tokens).strip()
            )

            if not predicted or not is_valid_medicine_name(predicted):
                predicted = "UNKNOWN"

            end_idx = (qty_idx + 1) if qty else i + tlen

            order_key = (predicted, med_type, qty)

            if order_key not in seen_order_lines:
                seen_order_lines.add(order_key)

                items.append({
                    "position": pos,
                    "text_span": " ".join(tokens[seg_start:end_idx]),
                    "raw_name": predicted,
                    "raw_form": med_type,
                    "raw_quantity": qty,
                    "boundary_confident": qty is not None
                })
                pos += 1

            seg_start = _skip_delimiters(tokens, end_idx)
            i = seg_start
            continue

        i += 1

    return items
