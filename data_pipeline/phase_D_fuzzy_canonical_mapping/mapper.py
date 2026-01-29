from .text_normalizer import normalize_for_matching
from .fuzzy_matcher import compute_fuzzy_scores


def map_row_to_master(row: dict, master_df):
    raw_name = row.get("raw_name", "")
    norm_name = normalize_for_matching(raw_name)

    if not norm_name:
        return None

    candidates = master_df["CLEANED_MEDICINE_NAME"].tolist()
    scores = compute_fuzzy_scores(norm_name, candidates)

    if not scores:
        return None

    best = scores[0]
    best_row = master_df[
        master_df["CLEANED_MEDICINE_NAME"] == best["candidate"]
    ].iloc[0]

    return {
        "FILE_NAME": row["file_name"],
        "POSITION": row["position"],
        "RAW_NAME": raw_name,
        "RAW_FORM": row["raw_form"],
        "MAPPED_NAME": best_row["CLEANED_MEDICINE_NAME"],
        "ITEM_CODE": best_row["ITEM_CODE"],
        "MEDICINE_TYPE": best_row["MEDICINE_TYPE"],
        "QUANTITY": row["raw_quantity"],  
        "MATCH_SCORE": best["score"],
        "SOURCE": "FUZZY"
    }
