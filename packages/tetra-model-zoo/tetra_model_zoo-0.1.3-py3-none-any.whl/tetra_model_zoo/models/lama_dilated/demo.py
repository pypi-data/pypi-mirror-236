from tetra_model_zoo.models._shared.repaint.demo import repaint_demo
from tetra_model_zoo.models.lama_dilated.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    LamaDilated,
)
from tetra_model_zoo.models.lama_dilated.test import IMAGE_ADDRESS, MASK_ADDRESS


def main():
    repaint_demo(LamaDilated, MODEL_ID, DEFAULT_WEIGHTS, IMAGE_ADDRESS, MASK_ADDRESS)


if __name__ == "__main__":
    main()
