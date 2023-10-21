import argparse
from typing import Callable

import torch
from PIL import Image

from tetra_model_zoo.models._shared.detr.app import DETRApp
from tetra_model_zoo.utils.asset_loaders import load_image


#
# Run DETR app end-to-end on a sample image.
# The demo will display the predicted mask in a window.
#
#
def detr_demo(
    model: Callable[..., Callable[[torch.Tensor, torch.Tensor], torch.Tensor]],
    model_id: str,
    default_weights: str,
    default_image: str,
):
    # Demo parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--weights", type=str, default=default_weights, help="Model weights"
    )
    parser.add_argument(
        "--image",
        type=str,
        default=default_image,
        help="test image file path or URL",
    )
    args = parser.parse_args()

    # Load image & model
    model = model.from_pretrained(args.weights)

    # Run app to scores, labels and boxes
    img = load_image(args.image, model_id)
    app = DETRApp(model)
    pred_images = app.predict(img, default_weights)

    # Show the predicted boxes, scores and class names on the image.
    Image.fromarray(pred_images[0]).show()
