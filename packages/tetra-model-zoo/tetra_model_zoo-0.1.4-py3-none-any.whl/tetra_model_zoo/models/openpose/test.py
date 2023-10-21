import numpy as np

from tetra_model_zoo.models.openpose.app import OpenPoseApp
from tetra_model_zoo.models.openpose.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    OpenPose,
)
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image
from tetra_model_zoo.utils.testing import skip_clone_repo_check

IMAGE_ADDRESS = get_model_asset_url(MODEL_ID, MODEL_ASSET_VERSION, "openpose_demo.png")
OUTPUT_IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "openpose_output.png"
)


@skip_clone_repo_check
def test_openpose_app():
    image = load_image(IMAGE_ADDRESS, MODEL_ID)
    output_image = load_image(OUTPUT_IMAGE_ADDRESS, MODEL_ID)
    app = OpenPoseApp(OpenPose.from_pretrained())
    app_output_image = app.estimate_pose(image)
    np.testing.assert_allclose(
        np.asarray(app_output_image, dtype=np.float32) / 255,
        np.asarray(output_image, dtype=np.float32) / 255,
        rtol=0.02,
        atol=0.2,
    )
