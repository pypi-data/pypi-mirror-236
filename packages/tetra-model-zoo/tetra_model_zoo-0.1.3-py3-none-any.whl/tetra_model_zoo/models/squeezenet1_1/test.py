from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
)
from tetra_model_zoo.models.squeezenet1_1.model import MODEL_ID, SqueezeNet


def test_numerical():
    run_imagenet_classifier_test(SqueezeNet.from_pretrained(), MODEL_ID)
