from typing import List, Dict
from rapidfuzz import fuzz


def compute_fuzzy_scores(query: str, candidates: List[str]) -> List[Dict]:
    results = []

    for cand in candidates:
        token_score = fuzz.token_set_ratio(query, cand)
        partial_score = fuzz.partial_ratio(query, cand)

        final = round(0.60*token_score + 0.40*partial_score, 4)

        results.append({
            "candidate": cand,
            "score": final
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results
