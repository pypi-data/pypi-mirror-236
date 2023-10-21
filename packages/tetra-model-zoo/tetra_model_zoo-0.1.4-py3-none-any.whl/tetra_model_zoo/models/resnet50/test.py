from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
)
from tetra_model_zoo.models.resnet50.model import MODEL_ID, ResNet50


def test_numerical():
    run_imagenet_classifier_test(
        ResNet50.from_pretrained(), MODEL_ID, probability_threshold=0.45
    )
