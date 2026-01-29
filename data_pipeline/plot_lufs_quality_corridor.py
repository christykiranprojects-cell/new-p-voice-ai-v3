import os
import re
import pandas as pd
import matplotlib.pyplot as plt


CSV_PATH = r"D:\new_p_voice_ai_v3\data_pipeline\artifacts\quality_matrix\quality_metrics_report_v3.csv"
OUTPUT_PNG = r"D:\new_p_voice_ai_v3\data_pipeline\artifacts\quality_matrix\integrated_vs_momentary_lufs_corridor.png"

INTEGRATED_TARGET = -20.0
INTEGRATED_MIN = -16.0
INTEGRATED_MAX = -24.0

MOMENTARY_MIN = -16.0
MOMENTARY_MAX = -12.0


def extract_audio_number(filename: str):
    match = re.match(r"(\d+)", filename)
    return match.group(1) if match else ""


def plot_lufs_corridor():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Quality metrics CSV not found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    x = df["integrated_lufs"]
    y = df["momentary_max_lufs"]

    plt.figure(figsize=(12, 8))

    plt.scatter(x, y, s=60, alpha=0.9)

    # Annotate each point with audio number
    for _, row in df.iterrows():
        audio_num = extract_audio_number(row["file"])
        if audio_num:
            plt.text(
                row["integrated_lufs"],
                row["momentary_max_lufs"] + 0.15,
                audio_num,
                fontsize=9,
                ha="center",
                va="bottom"
            )

    # Integrated LUFS lines
    plt.axvline(INTEGRATED_TARGET, linestyle="--", label="Target LUFS")
    plt.axvline(INTEGRATED_MIN, linestyle=":", label="Integrated Min")
    plt.axvline(INTEGRATED_MAX, linestyle=":", label="Integrated Max")

    # Momentary LUFS lines
    plt.axhline(MOMENTARY_MIN, linestyle=":", label="Momentary Min")
    plt.axhline(MOMENTARY_MAX, linestyle=":", label="Momentary Max")

    plt.xlabel("Integrated LUFS")
    plt.ylabel("Momentary Max LUFS")
    plt.title("Integrated vs Momentary LUFS — Quality Corridor")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=150)
    plt.close()

    print(f"LUFS corridor plot saved → {OUTPUT_PNG}")


if __name__ == "__main__":
    plot_lufs_corridor()
