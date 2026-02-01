import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# ------------------ PATHS ------------------
LATENCY_DIR = Path(r"D:\new_p_voice_ai_v3\data_pipeline\artifacts\Latency")
CONSOLIDATED_CSV = LATENCY_DIR / "consolidated" / "audio_latency_consolidated.csv"
PLOT_OUTPUT = LATENCY_DIR / "audio_latency_plot.png"

# ------------------ SAFETY CHECK ------------------
if not CONSOLIDATED_CSV.exists():
    raise FileNotFoundError(
        "Consolidated CSV not found. Run generate_latency_report.py first."
    )

# ------------------ LOAD ------------------
df = pd.read_csv(CONSOLIDATED_CSV)

# ------------------ PLOT ------------------
plt.figure(figsize=(14, 6))
plt.plot(
    df["audio_number"],
    df["audio_duration_sec"],
    marker="o"
)

plt.xlabel("Audio Number")
plt.ylabel("Audio Duration (Seconds)")
plt.title("Audio Latency per Recording")
plt.grid(True)
plt.tight_layout()

plt.savefig(PLOT_OUTPUT)
plt.close()

print("Latency plot created:")
print(PLOT_OUTPUT)
