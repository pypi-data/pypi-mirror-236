from __future__ import annotations

from typing import Any

import torch
import torchvision.models as tv_models

from tetra_model_zoo.models._shared.video_classifier.model import KineticsClassifier

MODEL_ID = __name__.split(".")[-2]
MODEL_ASSET_VERSION = 1
DEFAULT_WEIGHTS = tv_models.video.R2Plus1D_18_Weights.DEFAULT


class ResNet2Plus1D(KineticsClassifier):
    @staticmethod
    def from_pretrained(
        weights: Any = DEFAULT_WEIGHTS,
    ) -> torch.nn.Module:
        net = tv_models.video.r2plus1d_18(weights)
        return ResNet2Plus1D(net)
