from __future__ import annotations

from typing import Callable

import torch

from tetra_model_zoo.utils.image_processing import app_to_net_image_inputs


class MobileDetApp:
    """
    This class consists of light-weight "app code" that is required to perform end to end inference with MobileDet backbone.

    The app uses 1 model:
        * MobileDet

    For a given image input, the app will:
        * Run inference
        * returns backbone outputs
    """

    def __init__(self, model: Callable[[torch.Tensor], torch.Tensor]):
        self.model = model

    def predict(self, input_image):
        """
        Upscale provided images

        Parameters:
            input_image
                PIL image(s)
                or
                numpy array (N H W C x uint8) or (H W C x uint8) -- both RGB channel layout
                or
                pyTorch tensor (N C H W x fp32, value range is [0, 1]), RGB channel layout

        Returns:
                tuple(torch.Tensor) of size 5
                    Return tuple of tensor outputs of each block
        """
        _, NCHW_fp32_torch_frames = app_to_net_image_inputs(input_image)
        return self.model(NCHW_fp32_torch_frames)
