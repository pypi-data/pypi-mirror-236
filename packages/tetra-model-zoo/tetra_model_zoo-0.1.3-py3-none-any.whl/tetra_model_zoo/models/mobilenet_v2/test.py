from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
)
from tetra_model_zoo.models.mobilenet_v2.model import MODEL_ID, MobileNetV2


def test_numerical():
    run_imagenet_classifier_test(
        MobileNetV2.from_pretrained(), MODEL_ID, probability_threshold=0.39
    )
