from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
)
from tetra_model_zoo.models.resnext50.model import MODEL_ID, ResNeXt50


def test_numerical():
    run_imagenet_classifier_test(ResNeXt50.from_pretrained(), MODEL_ID)
