from tetra_model_zoo.models._shared.detr.app import DETRApp
from tetra_model_zoo.models.detr_resnet101.model import (
    DEFAULT_WEIGHTS,
    MODEL_ASSET_VERSION,
    MODEL_ID,
    DETRResNet101,
)
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image

IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "detr_test_image.jpg"
)


def test_task():
    net = DETRResNet101.from_pretrained(DEFAULT_WEIGHTS)
    img = load_image(IMAGE_ADDRESS, MODEL_ID)
    _, _, label, _ = DETRApp(net).predict(img, DEFAULT_WEIGHTS)
    assert set(list(label.numpy())) == {75, 63, 17}
