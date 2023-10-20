from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
)
from tetra_model_zoo.models.wideresnet50.model import MODEL_ID, WideResNet50


def test_numerical():
    run_imagenet_classifier_test(WideResNet50.from_pretrained(), MODEL_ID)
