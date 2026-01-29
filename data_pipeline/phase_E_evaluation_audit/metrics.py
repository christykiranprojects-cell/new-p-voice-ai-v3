import numpy as np
import pandas as pd


def compute_classification_metrics(eval_df: pd.DataFrame) -> dict:
    """
    Canonical Phase-E classification metrics.
    Closed-set, forced-alignment evaluation:
    - TP: exact name match
    - FN: mismatch
    - FP: 0
    - TN: 0 (not applicable)
    """

    tp = int((eval_df["MAPPED_NAME"] == eval_df["GT_NAME"]).sum())
    fn = int((eval_df["MAPPED_NAME"] != eval_df["GT_NAME"]).sum())

    fp = 0
    tn = 0  # not applicable by design

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    accuracy = recall  # in forced-alignment, accuracy == recall

    return {
        "tp": tp,
        "fn": fn,
        "fp": fp,
        "tn": tn,
        "accuracy": round(accuracy, 2),
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "f1_score": round(f1, 2),
    }


def compute_quantity_mae(eval_df: pd.DataFrame) -> float:
    valid = eval_df[
        eval_df["QUANTITY"].notna() &
        eval_df["GT_QUANTITY"].notna()
    ]

    if valid.empty:
        return float("nan")

    mae = float(
        np.mean(
            np.abs(valid["QUANTITY"] - valid["GT_QUANTITY"])
        )
    )

    return round(mae, 2)


def compute_wer_cer(eval_df: pd.DataFrame) -> pd.DataFrame:
    from jiwer import wer, cer

    rows = []
    for _, r in eval_df.iterrows():
        rows.append({
            "WER": wer(r["GT_NAME"], r["MAPPED_NAME"]),
            "CER": cer(r["GT_NAME"], r["MAPPED_NAME"]),
        })

    return pd.DataFrame(rows)
