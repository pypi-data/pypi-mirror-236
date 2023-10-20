from tetra_model_zoo.models._shared.video_classifier.demo import (
    kinetics_classifier_demo,
)
from tetra_model_zoo.models.resnet_2plus1d.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    ResNet2Plus1D,
)
from tetra_model_zoo.models.resnet_2plus1d.test import INPUT_VIDEO_PATH


def main():
    kinetics_classifier_demo(
        model_type=ResNet2Plus1D,
        model_id=MODEL_ID,
        default_weights=DEFAULT_WEIGHTS,
        default_video=INPUT_VIDEO_PATH,
    )


if __name__ == "__main__":
    main()
