from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.vit.model import DEFAULT_WEIGHTS, MODEL_ID, VIT


def main():
    imagenet_demo(VIT, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
