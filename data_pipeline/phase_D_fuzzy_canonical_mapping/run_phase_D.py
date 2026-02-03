import os
import pandas as pd

from .master_loader import load_master_table
from .mapper import map_row_to_master
from .merge_outputs import merge_fuzzy_csvs

# --------------------------------------------------
# PATHS
# --------------------------------------------------

PHASE_C_CSV = (
    r"D:\new_p_voice_ai_v3\data_pipeline\artifacts"
    r"\structured_boundary_extraction"
    r"\phase_C_structured_boundary_consolidated.csv"
)

MASTER_PATH = r"D:\new_p_voice_ai_v3\Data_Base\_master_sheet.xlsx"

OUTPUT_DIR = r"D:\new_p_voice_ai_v3\data_pipeline\artifacts\fuzzy_canonical_mapping"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_phase_D():
    print("Phase D — Fuzzy Canonical Mapping (CSV-Driven)")

    master_df = load_master_table(MASTER_PATH)
    phase_c_df = pd.read_csv(PHASE_C_CSV)

    required_cols = {
        "file_name",
        "position",
        "raw_name",
        "raw_form",
        "raw_quantity"
    }

    if not required_cols.issubset(phase_c_df.columns):
        raise ValueError(
            f"Missing required columns in Phase C CSV: "
            f"{required_cols - set(phase_c_df.columns)}"
        )

    mapped_rows = []

    for _, row in phase_c_df.iterrows():
        result = map_row_to_master(row.to_dict(), master_df)
        if result:
            mapped_rows.append(result)

    if not mapped_rows:
        raise RuntimeError("No fuzzy mappings produced")

    out_csv = os.path.join(
        OUTPUT_DIR,
        "phase_D_fuzzy_all.csv"
    )

    pd.DataFrame(mapped_rows).to_csv(out_csv, index=False)

    print(f"Fuzzy CSV written → {out_csv}")

    print("Merging fuzzy outputs...")
    merge_fuzzy_csvs()

    print("Phase D completed successfully")


if __name__ == "__main__":
    # python -m data_pipeline.phase_D_fuzzy_canonical_mapping.run_phase_D
    run_phase_D()

# RUNNER : 
# python -m data_pipeline.phase_D_fuzzy_canonical_mapping.run_phase_D
