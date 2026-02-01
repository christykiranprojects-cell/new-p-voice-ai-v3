import pandas as pd
from pathlib import Path
import json

# ============================================================
# CONFIG (CPU ONLY)
# ============================================================
CPU_REALTIME_FACTOR = 0.4  # Whisper large-v1 on CPU (assumed)

# ------------------ PATHS ------------------
INPUT_DIR = Path(r"D:\new_p_voice_ai_v3\data_pipeline\artifacts\transcripts_raw")

LATENCY_DIR = Path(r"D:\new_p_voice_ai_v3\data_pipeline\artifacts\Latency")
CONSOLIDATED_DIR = LATENCY_DIR / "consolidated"

LATENCY_DIR.mkdir(parents=True, exist_ok=True)
CONSOLIDATED_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUTPUT = LATENCY_DIR / "audio_latency_stats.json"
CSV_OUTPUT = CONSOLIDATED_DIR / "audio_latency_consolidated.csv"

# ============================================================
# LOAD & REDUCE (one row per audio file)
# ============================================================
frames = []

for csv_file in sorted(INPUT_DIR.glob("transcription_*.csv")):
    df = pd.read_csv(csv_file)

    # Take only the last segment per audio
    idx = df.groupby("file_name")["segment_id"].idxmax()
    df_max = df.loc[idx, ["file_name", "end_time_sec"]]

    frames.append(df_max)

latency_df = pd.concat(frames, ignore_index=True)

# ============================================================
# AUDIO NUMBER & DURATION
# ============================================================
latency_df["audio_number"] = (
    latency_df["file_name"]
    .str.replace(".wav", "", regex=False)
    .astype(int)
)

latency_df["audio_duration_sec"] = latency_df["end_time_sec"]

latency_df = latency_df.sort_values("audio_number")

latency_df = latency_df[
    ["audio_number", "file_name", "audio_duration_sec"]
]

# ============================================================
# CPU PROCESSING TIME (COMPUTED)
# ============================================================
latency_df["processing_time_sec_cpu"] = (
    latency_df["audio_duration_sec"] / CPU_REALTIME_FACTOR
)

latency_df["realtime_factor_cpu"] = CPU_REALTIME_FACTOR

# ============================================================
# SUMMARY STATS
# ============================================================
total_audio_sec = float(latency_df["audio_duration_sec"].sum())
total_processing_sec = float(latency_df["processing_time_sec_cpu"].sum())

summary = {
    "hardware": "CPU",
    "assumed_realtime_factor": CPU_REALTIME_FACTOR,
    "total_recordings": int(len(latency_df)),
    "average_latency_sec": round(float(latency_df["audio_duration_sec"].mean()), 3),
    "min_latency_sec": round(float(latency_df["audio_duration_sec"].min()), 3),
    "max_latency_sec": round(float(latency_df["audio_duration_sec"].max()), 3),
    "total_latency_sec": round(total_audio_sec, 3),
    "total_latency_hours": round(total_audio_sec / 3600.0, 3),
    "total_processing_time_sec_cpu": round(total_processing_sec, 3),
    "total_processing_time_hours_cpu": round(total_processing_sec / 3600.0, 3)
}

# ============================================================
# REALTIME FACTOR MATRIX (COMPUTED)
# ============================================================
realtime_factor_matrix = {
    "definition": "audio_duration_sec / processing_time_sec",
    "unit": "x realtime",
    "cpu": {
        "assumed_factor": CPU_REALTIME_FACTOR,
        "total_audio_sec": round(total_audio_sec, 3),
        "total_processing_time_sec": round(total_processing_sec, 3),
        "overall_realtime_factor": round(
            total_audio_sec / total_processing_sec, 3
        )
    }
}

# ============================================================
# SAVE JSON
# ============================================================
output_json = {
    "summary": summary,
    "realtime_factor_matrix": realtime_factor_matrix,
    "per_audio_latency": latency_df[
        [
            "audio_number",
            "file_name",
            "audio_duration_sec",
            "processing_time_sec_cpu",
            "realtime_factor_cpu"
        ]
    ].to_dict(orient="records")
}

with open(JSON_OUTPUT, "w", encoding="utf-8") as f:
    json.dump(output_json, f, indent=4)

# ============================================================
# SAVE CONSOLIDATED CSV
# ============================================================
latency_df[
    [
        "audio_number",
        "file_name",
        "audio_duration_sec",
        "processing_time_sec_cpu",
        "realtime_factor_cpu"
    ]
].to_csv(CSV_OUTPUT, index=False)

print("CPU latency artifacts generated successfully")
print("JSON:", JSON_OUTPUT)
print("CSV :", CSV_OUTPUT)
