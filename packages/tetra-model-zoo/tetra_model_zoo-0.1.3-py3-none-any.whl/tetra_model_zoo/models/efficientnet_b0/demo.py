from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.efficientnet_b0.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    EfficientNetB0,
)


def main():
    imagenet_demo(EfficientNetB0, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
