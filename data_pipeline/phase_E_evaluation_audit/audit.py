import pandas as pd


def build_failure_audit(eval_df: pd.DataFrame) -> pd.DataFrame:
    failures = eval_df[
        eval_df["MAPPED_NAME"] != eval_df["GT_NAME"]
    ].copy()

    failures["ERROR_TYPE"] = "FUZZY_NAME_MISMATCH"

    return failures[[
        "ROW_INDEX",
        "MAPPED_NAME",
        "GT_NAME",
        "QUANTITY",
        "GT_QUANTITY",
        "ERROR_TYPE"
    ]]


def summarize_failures(failure_df: pd.DataFrame) -> pd.DataFrame:
    return (
        failure_df
        .groupby("ERROR_TYPE")
        .size()
        .reset_index(name="count")
    )
