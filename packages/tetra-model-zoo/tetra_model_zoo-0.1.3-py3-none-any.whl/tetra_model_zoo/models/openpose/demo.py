import argparse

from tetra_model_zoo.models.openpose.app import OpenPoseApp
from tetra_model_zoo.models.openpose.model import MODEL_ID, OpenPose
from tetra_model_zoo.models.openpose.test import IMAGE_ADDRESS
from tetra_model_zoo.utils.asset_loaders import load_image


#
# Run OpenPose end-to-end on a sample image.
# The demo will display the input image with circles drawn over the estimated joint positions.
#
def main():
    # Demo parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image",
        type=str,
        default=IMAGE_ADDRESS,
        help="image file path or URL.",
    )

    args = parser.parse_args()

    # Load image & model
    app = OpenPoseApp(OpenPose.from_pretrained())
    image = load_image(args.image, MODEL_ID)
    pred_images = app.estimate_pose(image)
    pred_images.show()


if __name__ == "__main__":
    main()
