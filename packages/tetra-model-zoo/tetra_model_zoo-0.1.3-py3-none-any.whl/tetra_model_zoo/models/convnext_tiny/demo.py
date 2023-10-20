from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.convnext_tiny.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    ConvNextTiny,
)


def main():
    imagenet_demo(ConvNextTiny, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
