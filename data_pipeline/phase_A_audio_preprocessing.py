# uv pip install pyloudnorm
# IMPORTANT: disable numba JIT BEFORE importing librosa


import os
os.environ["NUMBA_DISABLE_JIT"] = "1"
# Numba is a Python performance compiler built on LLVM (low-level compiler infrastructure) that uses Just-In-Time compilation 
# to convert numerical Python code—especially loops and array operations—into native machine code 
# at runtime. It is mainly used to accelerate scientific and signal-processing workloads, 
# such as those inside Librosa. 
# However, because it depends on runtime compilation, CPU architecture, and OS-level binaries, 
# it can introduce instability on some Windows environments, so we disable it to ensure 
# deterministic and stable execution.
# 1 MEANS True, Disable 
# NOTE: Numba takes slow Python math code and turns it into fast machine code (like C/C++) at runtime


import os
import yaml
import librosa
import soundfile as sf
import pyloudnorm as pyln
import numpy as np
from .utils.audio_utils import remove_dc_offset

def preprocess_audio(input_path: str, output_path: str, config_path: str):
    # Load config
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)

    # Load audio
    samples, sr = librosa.load(
        input_path,
        sr=cfg["target_sample_rate"],
        mono=(cfg["channels"] == "mono")
    )

    # DC offset removal
    if cfg["dc_offset_removal"]:
        samples = remove_dc_offset(samples)

    # Loudness normalization
    meter = pyln.Meter(cfg["target_sample_rate"])
    loudness = meter.integrated_loudness(samples)
    samples = pyln.normalize.loudness(
        samples, loudness, cfg["loudness_target_lufs"]
    )

    # Silence trimming
    if cfg["trim_silence"]:
        samples, _ = librosa.effects.trim(
            samples,
            top_db=abs(cfg["silence_threshold_db"])
        )

    # Simple denoise placeholder
    if cfg["denoise"]:
        samples = librosa.effects.preemphasis(samples)

    # Save processed audio
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sf.write(output_path, samples, cfg["target_sample_rate"])

    return {
        "output_path": output_path,
        "duration_sec": len(samples) / cfg["target_sample_rate"],
        "loudness_target": cfg["loudness_target_lufs"]
    }

"""
# IMPORTANT: disable numba JIT BEFORE importing librosa
import os
os.environ["NUMBA_DISABLE_JIT"] = "1"

import yaml
import librosa
import soundfile as sf
import pyloudnorm as pyln
import numpy as np
from .utils.audio_utils import remove_dc_offset

MIN_AUDIO_DURATION_SEC = 0.3  # safety guard

def preprocess_audio(input_path: str, output_path: str, config_path: str):

    # -----------------------------
    # Load config
    # -----------------------------
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)

    # -----------------------------
    # Load audio
    # -----------------------------
    samples, sr = librosa.load(
        input_path,
        sr=cfg["target_sample_rate"],
        mono=(cfg["channels"] == "mono")
    )

    # -----------------------------
    # DC offset removal
    # -----------------------------
    if cfg["dc_offset_removal"]:
        samples = remove_dc_offset(samples)

    # -----------------------------
    # Silence trimming (lead & trail)
    # -----------------------------
    if cfg["trim_silence"]:
        samples, _ = librosa.effects.trim(
            samples,
            top_db=abs(cfg["silence_threshold_db"])
        )

    # Guard: empty or too short audio
    duration_sec = len(samples) / sr
    if duration_sec < MIN_AUDIO_DURATION_SEC:
        raise ValueError(
            f"Audio too short after trimming: {input_path}"
        )

    # -----------------------------
    # Noise handling (placeholder)
    # -----------------------------
    if cfg["denoise"]:
        # NOTE: This is NOT true denoising.
        # It is spectral emphasis for feature conditioning.
        samples = librosa.effects.preemphasis(samples)

    # -----------------------------
    # Loudness normalization (FINAL STEP)
    # -----------------------------
    meter = pyln.Meter(sr)
    loudness = meter.integrated_loudness(samples)

    samples = pyln.normalize.loudness(
        samples,
        loudness,
        cfg["loudness_target_lufs"]
    )

    # -----------------------------
    # Save processed audio
    # -----------------------------
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sf.write(output_path, samples, sr)

    return {
        "output_path": output_path,
        "duration_sec": round(duration_sec, 3),
        "target_lufs": cfg["loudness_target_lufs"]
    }
"""
