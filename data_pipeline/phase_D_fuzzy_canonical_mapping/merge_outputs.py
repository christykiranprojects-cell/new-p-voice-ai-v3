# ======================================================
# PHASE D — MERGE FUZZY CSV OUTPUTS (FINAL)
# ======================================================
# - Merges all per-audio fuzzy CSVs
# - Preserves QUANTITY correctly
# - Sorts FILE_NAME numerically (1.wav, 2.wav, 10.wav)
# - Sorts POSITION within each FILE_NAME
# ======================================================

import os
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PATHS
# --------------------------------------------------

FUZZY_DIR = r"D:\new_p_voice_ai_v3\data_pipeline\artifacts\fuzzy_canonical_mapping"

OUTPUT_CSV = os.path.join(
    FUZZY_DIR,
    "fuzzy_canonical_merged.csv"
)

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def extract_file_number(file_name: str) -> int:
    """
    Extract numeric part from FILE_NAME.
    Example: '10.wav' -> 10
    """
    try:
        return int(file_name.split(".")[0])
    except Exception:
        return 10**9  # push bad filenames to bottom


# --------------------------------------------------
# MERGE LOGIC
# --------------------------------------------------

def merge_fuzzy_csvs():
    csv_files = sorted(Path(FUZZY_DIR).glob("*_fuzzy.csv"))

    if not csv_files:
        raise RuntimeError(" No fuzzy CSV files found to merge")

    dfs = []

    for file in csv_files:
        print(f"Reading {file.name}")

        df = pd.read_csv(
            file,
            dtype={
                "FILE_NAME": str,
                "POSITION": "Int64",
                "RAW_NAME": str,
                "MAPPED_NAME": str,
                "ITEM_CODE": str,
                "MEDICINE_TYPE": str,
                "QUANTITY": str,      # 
                "MATCH_SCORE": float,
                "SOURCE": str,
            }
        )

        if df.empty:
            print(f"⚠ Skipping empty file: {file.name}")
            continue

        # Normalize QUANTITY (avoid NaN / dtype corruption)
        df["QUANTITY"] = (
            df["QUANTITY"]
            .astype(str)
            .str.strip()
            .replace({"nan": ""})
        )

        dfs.append(df)

    if not dfs:
        raise RuntimeError("All fuzzy CSV files were empty")

    # --------------------------------------------------
    # CONCAT
    # --------------------------------------------------

    merged_df = pd.concat(dfs, ignore_index=True)

    # --------------------------------------------------
    # SORT FILE_NAME NUMERICALLY + POSITION
    # --------------------------------------------------

    merged_df["_file_num"] = merged_df["FILE_NAME"].apply(extract_file_number)

    merged_df = merged_df.sort_values(
        by=["_file_num", "POSITION"],
        ascending=[True, True]
    )

    merged_df = merged_df.drop(columns=["_file_num"])

    # --------------------------------------------------
    # FINAL SAVE
    # --------------------------------------------------

    merged_df.to_csv(OUTPUT_CSV, index=False)

    print("\nFUZZY MERGED CSV CREATED")
    print(f"{OUTPUT_CSV}")
    print(f"Total rows: {len(merged_df)}")


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    merge_fuzzy_csvs()
