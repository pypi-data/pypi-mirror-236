from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.resnext101.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    ResNeXt101,
)


def main():
    imagenet_demo(ResNeXt101, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
