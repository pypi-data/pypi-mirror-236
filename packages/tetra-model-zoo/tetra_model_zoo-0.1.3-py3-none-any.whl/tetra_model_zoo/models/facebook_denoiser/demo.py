import argparse
import os
from typing import List

from tetra_model_zoo.models.facebook_denoiser.app import FacebookDenoiserApp
from tetra_model_zoo.models.facebook_denoiser.model import (
    DNS_48_URL,
    HIDDEN_LAYER_COUNT,
    MODEL_ID,
    SAMPLE_RATE,
    FacebookDenoiser,
)
from tetra_model_zoo.models.whisper_asr.test import TEST_AUDIO_PATH
from tetra_model_zoo.utils.asset_loaders import download_data


def main():
    """
    Run facebook denoiser on a sample audio (`.wav`) file.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--audio",
        nargs="+",
        default=[TEST_AUDIO_PATH],
        help="WAV file paths or URLs",
    )
    parser.add_argument(
        "--checkpoint",
        type=str,
        default=DNS_48_URL,
        help="Path to model checkpoint",
    )
    parser.add_argument(
        "--hidden_layer_count",
        type=int,
        default=HIDDEN_LAYER_COUNT,
        help="Count of hidden layers in model",
    )
    parser.add_argument(
        "--sample_rate",
        type=int,
        default=SAMPLE_RATE,
        help="Audio sample rate the model was trained on",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=os.getcwd(),
        help="output directory (where output WAV should be written)",
    )
    args = parser.parse_args()

    # Load Model
    source_model = FacebookDenoiser.from_pretrained(
        args.checkpoint, args.hidden_layer_count
    )
    app = FacebookDenoiserApp(source_model, args.sample_rate)

    # Download data
    audio: List[str] = args.audio
    for idx, file in enumerate(audio):
        if file.startswith("http"):
            audio[idx] = download_data(file, MODEL_ID)

    # Dump output from app
    output = app.denoise_audio(audio, args.output_dir)
    print("Wrote files:")
    for path in output:
        print(str(path))


if __name__ == "__main__":
    main()
