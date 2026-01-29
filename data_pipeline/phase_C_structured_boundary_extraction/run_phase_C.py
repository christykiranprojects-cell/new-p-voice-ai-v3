# ======================================================
# PHASE C RUNNER — STRUCTURED BOUNDARY EXTRACTION
# ======================================================
# Responsibilities:
# - Aggregate Whisper segments into logical transcripts
# - Guarantee safe spacing between segments
# - Invoke deterministic boundary extraction (Phase C)
# - Persist structured JSON artifacts (per file)
# - Persist ONE consolidated CSV artifact
# ======================================================

import os
import json
import re
import pandas as pd

from .snapshot_loader import load_medicine_type_snapshot
from .extractor import extract_items

# ------------------------------------------------------
# PATHS
# ------------------------------------------------------

TRANSCRIPT_DIR = r"D:\new_p_voice_ai_v3\data_pipeline\artifacts\transcripts_raw"
OUTPUT_DIR = r"D:\new_p_voice_ai_v3\data_pipeline\artifacts\structured_boundary_extraction"
CONSOLIDATED_CSV = os.path.join(
    OUTPUT_DIR,
    "phase_C_structured_boundary_consolidated.csv"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------------------------------
# HELPERS
# ------------------------------------------------------

def extract_numeric_index(file_name: str) -> int:
    """
    Converts:
      1.wav  → 1
      10.wav → 10
    """
    m = re.search(r"(\d+)", file_name)
    return int(m.group(1)) if m else -1


# ------------------------------------------------------
# MAIN
# ------------------------------------------------------

def run_phase_C():
    print("▶ Starting Phase C — Structured Boundary Extraction")

    # --------------------------------------------------
    # Load frozen MEDICINE_TYPE snapshot
    # --------------------------------------------------
    snapshot = load_medicine_type_snapshot()

    consolidated_rows = []

    # --------------------------------------------------
    # Process each transcription CSV
    # --------------------------------------------------
    for file in sorted(os.listdir(TRANSCRIPT_DIR)):
        if not file.lower().endswith(".csv"):
            continue

        csv_path = os.path.join(TRANSCRIPT_DIR, file)
        df = pd.read_csv(csv_path)

        required_cols = {"file_name", "segment_id", "raw_transcript"}
        if not required_cols.issubset(df.columns):
            raise ValueError(
                f"Missing required columns in {file}: "
                f"{required_cols - set(df.columns)}"
            )

        # --------------------------------------------------
        # Aggregate segments into ONE logical transcript
        # --------------------------------------------------
        grouped = (
            df.sort_values("segment_id")
              .groupby("file_name", as_index=False)["raw_transcript"]
              .apply(lambda x: " ".join(s.strip() for s in x if s.strip()))
        )

        extracted_items = []

        # --------------------------------------------------
        # Run Phase C extraction per audio file
        # --------------------------------------------------
        for _, row in grouped.iterrows():
            full_transcript = row["raw_transcript"]
            file_name = row["file_name"]

            items = extract_items(full_transcript, snapshot)

            for it in items:
                it["file_name"] = file_name
                extracted_items.append(it)

                consolidated_rows.append({
                    "file_name": file_name,
                    "position": it.get("position"),
                    "raw_name": it.get("raw_name"),
                    "raw_form": it.get("raw_form"),
                    "raw_quantity": (
                        pd.to_numeric(it.get("raw_quantity"), errors="coerce")
                    ),
                    "boundary_confident": it.get("boundary_confident"),
                    "text_span": it.get("text_span")
                })

        # --------------------------------------------------
        # Save per-file structured JSON
        # --------------------------------------------------
        output_path = os.path.join(
            OUTPUT_DIR,
            file.replace(".csv", "_structured.json")
        )

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(extracted_items, f, indent=2, ensure_ascii=False)

        print(f"✔ Phase C JSON written → {output_path}")

    # --------------------------------------------------
    # Save consolidated CSV (NUMERIC SORT FIX)
    # --------------------------------------------------
    if consolidated_rows:
        consolidated_df = pd.DataFrame(consolidated_rows)

        consolidated_df["_file_index"] = consolidated_df["file_name"].apply(
            extract_numeric_index
        )

        consolidated_df.sort_values(
            by=["_file_index", "position"],
            inplace=True
        )

        consolidated_df.drop(columns="_file_index", inplace=True)

        consolidated_df.to_csv(
            CONSOLIDATED_CSV,
            index=False
        )

        print(f"✔ Consolidated CSV written → {CONSOLIDATED_CSV}")

    print("✔ Phase C finished successfully.")


if __name__ == "__main__":
    # Execute as module:
    # python -m data_pipeline.phase_C_structured_boundary_extraction.run_phase_C
    run_phase_C()



# RUN IN TERMINAL
# python -m data_pipeline.phase_C_structured_boundary_extraction.run_phase_C

