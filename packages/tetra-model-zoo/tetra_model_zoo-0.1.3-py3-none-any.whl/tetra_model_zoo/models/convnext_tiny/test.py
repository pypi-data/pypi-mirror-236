from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
)
from tetra_model_zoo.models.convnext_tiny.model import MODEL_ID, ConvNextTiny


def test_numerical():
    run_imagenet_classifier_test(ConvNextTiny.from_pretrained(), MODEL_ID)
