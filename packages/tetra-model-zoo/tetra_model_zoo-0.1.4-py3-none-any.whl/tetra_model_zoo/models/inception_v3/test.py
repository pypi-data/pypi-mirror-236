from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
)
from tetra_model_zoo.models.inception_v3.model import MODEL_ID, InceptionNetV3


def test_numerical():
    run_imagenet_classifier_test(InceptionNetV3.from_pretrained(), MODEL_ID)
