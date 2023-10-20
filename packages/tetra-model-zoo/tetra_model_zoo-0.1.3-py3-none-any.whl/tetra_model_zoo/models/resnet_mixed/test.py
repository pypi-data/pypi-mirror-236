from tetra_model_zoo.models._shared.video_classifier.app import (
    KineticsClassifierApp,
    recognize_action_kinetics_400,
)
from tetra_model_zoo.models.resnet_mixed.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    ResNetMixed,
)
from tetra_model_zoo.utils.asset_loaders import download_data, get_model_asset_url

INPUT_VIDEO_PATH = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "surfing_cutback.mp4"
)


def test_numerical():
    kinetics_app = KineticsClassifierApp(model=ResNetMixed.from_pretrained())
    dst_path = download_data(INPUT_VIDEO_PATH, MODEL_ID)
    prediction = kinetics_app.predict(path=dst_path)
    assert "surfing water" in recognize_action_kinetics_400(prediction)
