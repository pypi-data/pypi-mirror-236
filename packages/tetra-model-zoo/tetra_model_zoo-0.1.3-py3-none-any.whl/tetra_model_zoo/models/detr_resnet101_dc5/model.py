from __future__ import annotations

from tetra_model_zoo.models._shared.detr.model import DETR

MODEL_ID = __name__.split(".")[-2]
DEFAULT_WEIGHTS = "facebook/detr-resnet-101-dc5"
MODEL_ASSET_VERSION = 1


class DETRResNet101DC5(DETR):
    """Exportable DETR model, end-to-end."""

    @staticmethod
    def from_pretrained(ckpt_name: str = DEFAULT_WEIGHTS):
        return DETR.from_pretrained(ckpt_name)
