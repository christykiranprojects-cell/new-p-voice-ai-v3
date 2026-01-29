import os
from data_pipeline.phase_B_transcription import transcribe_audio


PROCESSED_AUDIO_DIR = (
    r"D:\new_p_voice_ai_v3\data_pipeline\artifacts\audio_processed"
)

TRANSCRIPT_DIR = (
    r"D:\new_p_voice_ai_v3\data_pipeline\artifacts\transcripts_raw"
)


def run_phase_B(model):
    """
    Phase B runner.
    Model must be injected by Execution Controller.
    """

    if model is None:
        raise RuntimeError("Model not provided to run_phase_B")

    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

    for file in sorted(os.listdir(PROCESSED_AUDIO_DIR)):
        if file.lower().endswith(".wav"):
            audio_path = os.path.join(PROCESSED_AUDIO_DIR, file)

            output_csv = os.path.join(
                TRANSCRIPT_DIR,
                f"transcription_{os.path.splitext(file)[0]}.csv"
            )

            transcribe_audio(
                model=model,
                audio_path=audio_path,
                output_csv=output_csv
            )

            print(f"Transcribed: {file}")
