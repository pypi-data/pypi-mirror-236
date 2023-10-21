from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
)
from tetra_model_zoo.models.mobilenet_v3_large.model import MODEL_ID, MobileNetV3Large


def test_numerical():
    run_imagenet_classifier_test(MobileNetV3Large.from_pretrained(), MODEL_ID)
