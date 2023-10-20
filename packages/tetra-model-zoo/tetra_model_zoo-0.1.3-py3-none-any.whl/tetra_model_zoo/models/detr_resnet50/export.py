from __future__ import annotations

from typing import Any, List

import torch

import tetra_hub as hub
from tetra_model_zoo.models.detr_resnet50.model import DEFAULT_WEIGHTS, DETRResNet50
from tetra_model_zoo.utils.args import vision_export_parser
from tetra_model_zoo.utils.hub import download_hub_models


def trace(model: DETRResNet50, image_shape: List[int], mask_shape: List[int]) -> Any:
    """
    Convert DETR to a pytorch trace. Traces can be saved & loaded from disk.
    Returns: Trace Object
    """
    return torch.jit.trace(
        model, [torch.rand((image_shape)), torch.rand((mask_shape))], strict=False
    )


def main():
    # Export parameters
    parser = vision_export_parser(
        default_x=480, default_y=480, dim_constraint="Must be divisble by 32."
    )
    parser.add_argument(
        "--weights",
        type=str,
        default=DEFAULT_WEIGHTS,
    )
    parser.add_argument("--c", type=int, default=3, help="Number of image channels.")

    args = parser.parse_args()

    # Instantiate the model & a sample input.
    detr_model = DETRResNet50.from_pretrained(args.weights)

    # Trace the model.
    traced_detr = trace(
        detr_model, [args.b, args.c, args.y, args.x], [args.b, args.y, args.x]
    )
    # Select the device(s) you'd like to optimize for.
    devices = [hub.Device(x) for x in args.devices]

    # # Submit the traced models for conversion & profiling.
    jobs = hub.submit_profile_job(
        name="detr",
        model=traced_detr,
        input_shapes=detr_model.get_input_spec((args.y, args.x), args.b, args.c),
        device=devices,
        options="--enable_mlpackage",
    )

    # Download the optimized assets!
    download_hub_models(jobs)


if __name__ == "__main__":
    main()
