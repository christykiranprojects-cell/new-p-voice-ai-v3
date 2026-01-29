import csv
import os
from datetime import datetime


def transcribe_audio(model, audio_path, output_csv):
    """
    Phase B — Transcription (Data Plane)
    Model is injected by Execution Controller (changes_1).
    """

    if model is None:
        raise RuntimeError("No model provided to Phase B transcription")

    result = model.transcribe(audio_path, verbose=False)

    run_id = datetime.now().strftime("run_%Y%m%d_%H%M%S")
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "file_name",
            "segment_id",
            "start_time_sec",
            "end_time_sec",
            "duration_sec",
            "raw_transcript",
            "language",
            "audio_path",
            "run_id"
        ])

        for i, seg in enumerate(result.get("segments", [])):
            writer.writerow([
                os.path.basename(audio_path),
                i,
                seg["start"],
                seg["end"],
                seg["end"] - seg["start"],
                seg["text"].strip(),
                result.get("language"),
                audio_path,
                run_id
            ])
