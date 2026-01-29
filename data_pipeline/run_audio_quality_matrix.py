import os
import re
import pandas as pd
from audio_quality_matrix import analyze_audio_quality


# =============================
# INPUT PATH
# =============================
AUDIO_DIR = r"D:\new_p_voice_ai_v3\Data_Base\Raw_Audios"

# =============================
# OUTPUT PATH
# =============================
OUTPUT_DIR = r"D:\new_p_voice_ai_v3\data_pipeline\artifacts\quality_matrix"
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "quality_metrics_report_v3.csv")

# =============================
# SUPPORTED FORMATS
# =============================
SUPPORTED_AUDIO_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".flac",
    ".ogg",
    ".aac",
    ".wma"
}


def extract_number(filename: str) -> int:
    """
    Extract numeric prefix from filenames like:
    1.wav, 2.mp3, 10.m4a
    Enables natural numeric sorting
    """
    match = re.match(r"(\d+)", filename)
    return int(match.group(1)) if match else float("inf")


def run_audio_quality_matrix():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = [
        f for f in os.listdir(AUDIO_DIR)
        if os.path.splitext(f)[1].lower() in SUPPORTED_AUDIO_EXTENSIONS
    ]

    # Numeric sorting (format-agnostic)
    files = sorted(files, key=extract_number)

    rows = []

    for file in files:
        path = os.path.join(AUDIO_DIR, file)
        rows.append(analyze_audio_quality(path))

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"Audio Quality Matrix saved → {OUTPUT_CSV}")


if __name__ == "__main__":
    run_audio_quality_matrix()
