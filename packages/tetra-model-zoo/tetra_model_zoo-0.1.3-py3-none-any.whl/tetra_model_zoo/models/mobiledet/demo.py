from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    TEST_IMAGENET_IMAGE,
)
from tetra_model_zoo.models.mobiledet import MODEL_ID, App, Model
from tetra_model_zoo.utils.asset_loaders import load_image


def main():
    image = load_image(TEST_IMAGENET_IMAGE, MODEL_ID)
    app = App(Model.from_pretrained())
    app.predict(image)


if __name__ == "__main__":
    main()
