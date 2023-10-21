from __future__ import annotations

from typing import Any, List

import torch

import tetra_hub as hub
from tetra_model_zoo.models.mobiledet.model import MODEL_ID, MobileDet
from tetra_model_zoo.utils.args import base_export_parser
from tetra_model_zoo.utils.hub import download_hub_models


def trace(model: MobileDet, input_shape: List[int] = [1, 3, 640, 640]) -> Any:
    """
    Convert MobileDet backbone to a pytorch trace. Traces can be saved & loaded from disk.
    Returns: Trace Object
    """
    return torch.jit.trace(model, [torch.ones(input_shape)])


def main():
    # Export parameters
    parser = base_export_parser()

    args = parser.parse_args()

    # Instantiate the model
    model = MobileDet.from_pretrained()

    # Trace the model.
    traced_model = trace(model)

    # Select the device(s) you'd like to optimize for.
    devices = [hub.Device(x) for x in args.devices]

    # Submit the traced models for conversion & profiling.
    jobs = hub.submit_profile_job(
        name=MODEL_ID,
        model=traced_model,
        input_shapes=model.get_input_spec(),
        device=devices,
    )

    # Download the optimized asset!
    download_hub_models(jobs)


if __name__ == "__main__":
    main()
