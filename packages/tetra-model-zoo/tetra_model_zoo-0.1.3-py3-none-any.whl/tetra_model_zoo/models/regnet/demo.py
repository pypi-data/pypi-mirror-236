from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.regnet.model import DEFAULT_WEIGHTS, MODEL_ID, RegNet


def main():
    imagenet_demo(RegNet, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
