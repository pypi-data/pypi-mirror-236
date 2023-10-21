from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
)
from tetra_model_zoo.models.vit.model import MODEL_ID, VIT


def test_numerical():
    run_imagenet_classifier_test(VIT.from_pretrained(), MODEL_ID)
