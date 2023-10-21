from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.densenet121.model import DEFAULT_WEIGHTS, MODEL_ID, DenseNet


def main():
    imagenet_demo(DenseNet, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
