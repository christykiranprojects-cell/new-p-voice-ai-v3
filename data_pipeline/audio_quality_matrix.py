import os
import numpy as np
import librosa
import pyloudnorm as pyln


def analyze_audio_quality(audio_path: str) -> dict:
    """
    READ-ONLY analysis of audio.
    Multi-format safe via librosa + FFmpeg.
    Does NOT modify audio.
    """

    y, sr = librosa.load(audio_path, sr=None, mono=False)

    if y.size == 0:
        raise ValueError("Empty audio file")

    # Channel count
    channels = 1 if y.ndim == 1 else y.shape[0]

    # Convert to mono for analysis consistency
    if y.ndim > 1:
        y = np.mean(y, axis=0)

    duration_sec = len(y) / sr
    dc_offset = float(np.mean(y))

    intervals = librosa.effects.split(y, top_db=30)
    non_silent = sum((end - start) for start, end in intervals)
    silence_ratio = 1.0 - (non_silent / len(y)) if len(y) > 0 else 1.0

    meter = pyln.Meter(sr)
    integrated_lufs = meter.integrated_loudness(y)

    window_size = int(0.4 * sr)
    hop_size = int(0.1 * sr)

    momentary_values = []

    for start in range(0, len(y) - window_size, hop_size):
        window = y[start:start + window_size]
        try:
            momentary_values.append(
                meter.integrated_loudness(window)
            )
        except Exception:
            continue

    momentary_max = (
        float(max(momentary_values))
        if momentary_values else float("nan")
    )

    return {
        "file": os.path.basename(audio_path),
        "format": os.path.splitext(audio_path)[1].lower(),
        "sample_rate": sr,
        "channels": channels,
        "duration_sec": round(duration_sec, 2),
        "integrated_lufs": round(integrated_lufs, 2),
        "momentary_max_lufs": round(momentary_max, 2),
        "residual_dc_offset": round(dc_offset, 7),
        "silence_ratio": round(silence_ratio, 4),
    }
