from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.googlenet.model import DEFAULT_WEIGHTS, MODEL_ID, GoogLeNet


def main():
    imagenet_demo(GoogLeNet, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
