from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.mobilenet_v3_large.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    MobileNetV3Large,
)


def main():
    imagenet_demo(MobileNetV3Large, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
