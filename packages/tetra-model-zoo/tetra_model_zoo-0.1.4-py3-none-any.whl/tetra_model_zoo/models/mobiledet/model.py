from __future__ import annotations

import torch

from tetra_model_zoo.utils.asset_loaders import SourceAsRoot
from tetra_model_zoo.utils.input_spec import InputSpec

MOBILEDET_SOURCE_REPOSITORY = "https://github.com/tetraai/mobiledet-pytorch"
MOBILEDET_SOURCE_REPO_COMMIT = "f0df9b534b03c1c11bf5292676b4e80cc8df6d4f"
MODEL_ID = __name__.split(".")[-2]
DEFAULT_WEIGHTS = "dsp"


class MobileDet(torch.nn.Module):
    """Exportable MobileDet backbone"""

    def __init__(
        self,
        model: torch.nn.Module,
    ) -> None:
        super().__init__()
        self.model = model

    @staticmethod
    def from_pretrained(
        backbone_type: str = DEFAULT_WEIGHTS,
    ) -> MobileDet:
        """Load RealESRGAN from a weightfile created by the source RealESRGAN repository."""

        # Load PyTorch model from disk
        model = _load_mobiledet_source_model_from_backbone(backbone_type)

        return MobileDet(model)

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        """
        Run RealESRGAN on `image`, and produce an upscaled image

        Parameters:
            image: Pixel values pre-processed for GAN consumption.
                   Range: float[0, 1]
                   3-channel Color Space: RGB

        Returns:
            image: Pixel values
                   Range: float[0, 1]
                   3-channel Color Space: RGB
        """
        return self.model(input)

    def get_input_spec(
        self,
        image_size: tuple[int, int] | int = 640,
        batch_size: int = 1,
        num_channels: int = 3,
    ) -> InputSpec:
        # Get the input specification ordered (name -> (shape, type)) pairs for this model.
        #
        # This can be used with the tetra_hub python API to declare
        # the model input specification upon submitting a profile job.
        if isinstance(image_size, int):
            image_size = (image_size, image_size)
        return {"image": ((batch_size, num_channels, *image_size), "float32")}


def _load_mobiledet_source_model_from_backbone(
    backbone_type: str,
) -> torch.nn.Module:
    with SourceAsRoot(
        MOBILEDET_SOURCE_REPOSITORY, MOBILEDET_SOURCE_REPO_COMMIT, MODEL_ID
    ):
        from mobiledet_dsp import MobileDetDSP
        from mobiledet_gpu import MobileDetGPU
        from mobiledet_tpu import MobileDetTPU

        if backbone_type == "dsp":
            model = MobileDetDSP()
        elif backbone_type == "gpu":
            model = MobileDetGPU()
        elif backbone_type == "tpu":
            model = MobileDetTPU()
        else:
            raise ValueError(
                f"Incorrect backbone_type({backbone_type}) specificed."
                " Provide one of 'dsp', 'gpu' or 'tpu'."
            )

        model.eval()
        return model
