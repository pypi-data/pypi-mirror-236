from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
)
from tetra_model_zoo.models.efficientnet_b0.model import MODEL_ID, EfficientNetB0


def test_numerical():
    run_imagenet_classifier_test(EfficientNetB0.from_pretrained(), MODEL_ID)
