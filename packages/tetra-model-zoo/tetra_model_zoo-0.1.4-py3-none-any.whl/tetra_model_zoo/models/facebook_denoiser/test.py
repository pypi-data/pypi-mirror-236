import torch
import torchaudio

from tetra_model_zoo.models.facebook_denoiser.app import FacebookDenoiserApp
from tetra_model_zoo.models.facebook_denoiser.model import (
    ASSET_VERSION,
    MODEL_ID,
    FacebookDenoiser,
)
from tetra_model_zoo.utils.asset_loaders import download_data, get_model_asset_url

EXAMPLE_RECORDING = get_model_asset_url(
    MODEL_ID, ASSET_VERSION, "icsi_meeting_recording.wav"
)
ENHANCED_EXAMPLE_RECORDING = get_model_asset_url(
    MODEL_ID, ASSET_VERSION, "icsi_meeting_recording_enhanced.wav"
)


def test_sample_app():
    app = FacebookDenoiserApp(FacebookDenoiser.from_pretrained())
    try:
        out = app.predict([download_data(EXAMPLE_RECORDING, MODEL_ID)])[0][:, 0]
    except RuntimeError as e:
        if "Couldn't find appropriate backend to handle uri" not in str(e):
            raise e
        print(
            "You're missing either FFMPEG on Linux (apt-get install ffmpeg) or PySoundFile on Windows (pip install PySoundFile)"
        )
        return
    expected, _ = torchaudio.load(download_data(ENHANCED_EXAMPLE_RECORDING, MODEL_ID))
    torch.testing.assert_allclose(out, expected)
