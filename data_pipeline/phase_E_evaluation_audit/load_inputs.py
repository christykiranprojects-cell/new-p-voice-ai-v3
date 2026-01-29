import pandas as pd
import os


def load_phase_d_predictions(csv_path: str) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(csv_path)

    df = pd.read_csv(csv_path)

    required = {"MAPPED_NAME", "QUANTITY"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns in Phase D CSV: {missing}"
        )

    df["MAPPED_NAME"] = (
        df["MAPPED_NAME"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    df["QUANTITY"] = pd.to_numeric(df["QUANTITY"], errors="coerce")

    return df.reset_index(drop=True)


def load_ground_truth(xlsx_path: str) -> pd.DataFrame:
    if not os.path.exists(xlsx_path):
        raise FileNotFoundError(xlsx_path)

    df = pd.read_excel(xlsx_path)

    required = {"CLEANED_MEDICINE_NAME", "Quantity"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns in ground truth: {missing}"
        )

    df["GT_NAME"] = (
        df["CLEANED_MEDICINE_NAME"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    df["GT_QUANTITY"] = pd.to_numeric(df["Quantity"], errors="coerce")

    return df.reset_index(drop=True)
