from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
)
from tetra_model_zoo.models.googlenet.model import MODEL_ID, GoogLeNet


def test_numerical():
    run_imagenet_classifier_test(GoogLeNet.from_pretrained(), MODEL_ID)
