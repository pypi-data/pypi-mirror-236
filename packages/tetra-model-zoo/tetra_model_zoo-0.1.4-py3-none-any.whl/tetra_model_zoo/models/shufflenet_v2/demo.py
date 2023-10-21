from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.shufflenet_v2.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    ShufflenetV2,
)


def main():
    imagenet_demo(ShufflenetV2, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
