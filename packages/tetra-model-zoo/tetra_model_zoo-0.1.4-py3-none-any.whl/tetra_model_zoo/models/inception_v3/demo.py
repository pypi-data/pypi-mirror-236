from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.inception_v3.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    InceptionNetV3,
)


def main():
    imagenet_demo(InceptionNetV3, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
