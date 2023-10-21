from tetra_model_zoo.models._shared.repaint.demo import repaint_demo
from tetra_model_zoo.models.aotgan.model import AOTGAN, DEFAULT_WEIGHTS, MODEL_ID
from tetra_model_zoo.models.aotgan.test import IMAGE_ADDRESS, MASK_ADDRESS


def main():
    repaint_demo(AOTGAN, MODEL_ID, DEFAULT_WEIGHTS, IMAGE_ADDRESS, MASK_ADDRESS)


if __name__ == "__main__":
    main()
