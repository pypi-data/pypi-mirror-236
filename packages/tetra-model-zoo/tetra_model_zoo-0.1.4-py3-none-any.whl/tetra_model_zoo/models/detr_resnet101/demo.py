from tetra_model_zoo.models._shared.detr.demo import detr_demo
from tetra_model_zoo.models.detr_resnet101.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    DETRResNet101,
)
from tetra_model_zoo.models.detr_resnet101.test import IMAGE_ADDRESS

#
# Run DETR app end-to-end on a sample image.
# The demo will display the predicted mask in a window.
#
#
if __name__ == "__main__":
    detr_demo(
        DETRResNet101,
        MODEL_ID,
        DEFAULT_WEIGHTS,
        IMAGE_ADDRESS,
    )
