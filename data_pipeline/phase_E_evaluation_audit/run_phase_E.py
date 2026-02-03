import os
import json
import pandas as pd

from .load_inputs import (
    load_phase_d_predictions,
    load_ground_truth
)
from .metrics import (
    compute_classification_metrics,
    compute_quantity_mae,
    compute_wer_cer
)
from .audit import build_failure_audit, summarize_failures


PHASE_D_PRED_CSV = (
    r"D:\new_p_voice_ai_v3\data_pipeline\artifacts"
    r"\fuzzy_canonical_mapping\phase_D_fuzzy_all.csv"
)

GROUND_TRUTH_XLSX = (
    r"D:\new_p_voice_ai_v3\Data_Base\_ground_truth.xlsx"
)

OUT_DIR = (
    r"D:\new_p_voice_ai_v3\data_pipeline\artifacts"
    r"\evaluation_audit_phase_E"
)

os.makedirs(OUT_DIR, exist_ok=True)


def run_phase_E():
    print("Phase E — Evaluation")

    pred_df = load_phase_d_predictions(PHASE_D_PRED_CSV)
    gt_df = load_ground_truth(GROUND_TRUTH_XLSX)

    # HARD ALIGNMENT GUARANTEE
    if len(pred_df) != len(gt_df):
        raise ValueError(
            f"Row count mismatch: pred={len(pred_df)} gt={len(gt_df)}"
        )

    eval_df = pd.DataFrame({
        "ROW_INDEX": range(len(gt_df)),
        "MAPPED_NAME": pred_df["MAPPED_NAME"],
        "GT_NAME": gt_df["GT_NAME"],
        "QUANTITY": pred_df["QUANTITY"],
        "GT_QUANTITY": gt_df["GT_QUANTITY"],
    })

    # ---------------- METRICS ----------------
    cls_metrics = compute_classification_metrics(eval_df)
    quantity_mae = compute_quantity_mae(eval_df)
    wer_cer_df = compute_wer_cer(eval_df)

    mean_wer = round(float(wer_cer_df["WER"].mean()), 2)
    mean_cer = round(float(wer_cer_df["CER"].mean()), 2)

    rows_evaluated = round(float(len(eval_df)), 2)
    rows_with_quantity = round(
        float(
            eval_df[
                eval_df["QUANTITY"].notna() &
                eval_df["GT_QUANTITY"].notna()
            ].shape[0]
        ),
        2
    )

    # ---------------- AUDIT ----------------
    failure_df = build_failure_audit(eval_df)
    summary_df = summarize_failures(failure_df)

    # ---------------- OUTPUTS ----------------
    with open(os.path.join(OUT_DIR, "metrics.json"), "w") as f:
        json.dump(
            {
                **cls_metrics,
                "quantity_mae": quantity_mae,
                "mean_wer": mean_wer,
                "mean_cer": mean_cer,
                "rows_evaluated": rows_evaluated,
                "rows_with_quantity": rows_with_quantity,
            },
            f,
            indent=2
        )

    eval_df.to_csv(
        os.path.join(OUT_DIR, "aligned_predictions_vs_gt.csv"),
        index=False
    )

    wer_cer_df.to_csv(
        os.path.join(OUT_DIR, "wer_cer_report.csv"),
        index=False
    )

    failure_df.to_csv(
        os.path.join(OUT_DIR, "failure_audit.csv"),
        index=False
    )

    summary_df.to_csv(
        os.path.join(OUT_DIR, "failure_summary.csv"),
        index=False
    )

    print("Phase E completed successfully")


if __name__ == "__main__":
    run_phase_E()
