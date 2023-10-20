import numpy as np

from tetra_model_zoo.models.esrgan.app import ESRGANApp
from tetra_model_zoo.models.esrgan.model import ESRGAN, MODEL_ASSET_VERSION, MODEL_ID
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image
from tetra_model_zoo.utils.testing import skip_clone_repo_check

IMAGE_ADDRESS = get_model_asset_url(MODEL_ID, MODEL_ASSET_VERSION, "esrgan_demo.jpg")
OUTPUT_IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "esrgan_demo_output.png"
)


@skip_clone_repo_check
def test_esrgan_app():
    image = load_image(IMAGE_ADDRESS, MODEL_ID)
    output_image = load_image(OUTPUT_IMAGE_ADDRESS, MODEL_ID)
    app = ESRGANApp(ESRGAN.from_pretrained())
    app_output_image = app.upscale_image(image)
    np.testing.assert_allclose(
        np.asarray(app_output_image, dtype=np.float32) / 255,
        np.asarray(output_image, dtype=np.float32) / 255,
        rtol=0.02,
        atol=0.2,
    )
