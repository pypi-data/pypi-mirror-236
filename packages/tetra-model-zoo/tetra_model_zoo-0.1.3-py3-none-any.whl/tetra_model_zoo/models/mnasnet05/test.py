from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
)
from tetra_model_zoo.models.mnasnet05.model import MODEL_ID, MNASNet05


def test_numerical():
    run_imagenet_classifier_test(
        MNASNet05.from_pretrained(), MODEL_ID, probability_threshold=0.69
    )
