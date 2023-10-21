from tetra_model_zoo.models._shared.detr.demo import detr_demo
from tetra_model_zoo.models.detr_resnet50.test import IMAGE_ADDRESS
from tetra_model_zoo.models.detr_resnet101_dc5.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    DETRResNet101DC5,
)

#
# Run DETR app end-to-end on a sample image.
# The demo will display the predicted mask in a window.
#
#
if __name__ == "__main__":
    detr_demo(
        DETRResNet101DC5,
        MODEL_ID,
        DEFAULT_WEIGHTS,
        IMAGE_ADDRESS,
    )
