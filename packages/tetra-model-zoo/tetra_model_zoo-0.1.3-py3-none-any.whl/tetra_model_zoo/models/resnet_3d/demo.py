from tetra_model_zoo.models._shared.video_classifier.demo import (
    kinetics_classifier_demo,
)
from tetra_model_zoo.models.resnet_3d.model import DEFAULT_WEIGHTS, MODEL_ID, ResNet3D
from tetra_model_zoo.models.resnet_3d.test import INPUT_VIDEO_PATH


def main():
    kinetics_classifier_demo(
        model_type=ResNet3D,
        model_id=MODEL_ID,
        default_weights=DEFAULT_WEIGHTS,
        default_video=INPUT_VIDEO_PATH,
    )


if __name__ == "__main__":
    main()
