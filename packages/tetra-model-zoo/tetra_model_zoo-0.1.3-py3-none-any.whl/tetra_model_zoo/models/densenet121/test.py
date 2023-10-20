from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
)
from tetra_model_zoo.models.densenet121.model import MODEL_ID, DenseNet


def test_numerical():
    run_imagenet_classifier_test(DenseNet.from_pretrained(), MODEL_ID)
