import os
from .phase_A_audio_preprocessing import preprocess_audio

RAW_AUDIO_DIR = r"D:\new_p_voice_ai_v3\Data_Base\Raw_Audios"
PROCESSED_AUDIO_DIR = r"D:\new_p_voice_ai_v3\data_pipeline\artifacts\audio_processed"
CONFIG_PATH = r"D:\new_p_voice_ai_v3\data_pipeline\configs\audio_preprocess_config.yaml"

SUPPORTED_EXT = (".wav", ".mp3", ".m4a", ".aac")

for file in os.listdir(RAW_AUDIO_DIR):
    if file.lower().endswith(SUPPORTED_EXT):
        input_path = os.path.join(RAW_AUDIO_DIR, file)
        output_path = os.path.join(
            PROCESSED_AUDIO_DIR,
            os.path.splitext(file)[0] + ".wav"
        )

        meta = preprocess_audio(
            input_path=input_path,
            output_path=output_path,
            config_path=CONFIG_PATH
        )

        print(f"Processed: {file} → {meta['output_path']}")

# python -m data_pipeline.run_phase_A