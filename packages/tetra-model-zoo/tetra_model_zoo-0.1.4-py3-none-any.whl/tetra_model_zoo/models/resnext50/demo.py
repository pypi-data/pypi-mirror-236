from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.resnext50.model import DEFAULT_WEIGHTS, MODEL_ID, ResNeXt50


def main():
    imagenet_demo(ResNeXt50, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
