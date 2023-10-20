from __future__ import annotations

from typing import Any

import torch

import tetra_hub as hub
from tetra_model_zoo.models.facebook_denoiser.model import (
    DEFAULT_SEQUENCE_LENGTH,
    DNS_48_URL,
    HIDDEN_LAYER_COUNT,
    MODEL_ID,
    FacebookDenoiser,
)
from tetra_model_zoo.utils.args import base_export_parser
from tetra_model_zoo.utils.hub import download_hub_models


def trace(model: FacebookDenoiser, sequence_length) -> Any:
    """
    Convert fb_dns to a pytorch trace. Traces can be saved & loaded from disk.
    Returns: Trace Object
    """
    input_shape = model.get_input_spec(sequence_length)["noisy"][0]
    return torch.jit.trace(model, [torch.ones(input_shape)])


def main():
    # Export parameters
    parser = base_export_parser()
    parser.add_argument(
        "--checkpoint",
        type=str,
        default=DNS_48_URL,
        help="URL or path to the checkpoint to load for the Facebook denoiser.",
    )
    parser.add_argument(
        "--hidden_layer_count",
        type=int,
        default=HIDDEN_LAYER_COUNT,
        help="Count of hidden layers in model",
    )
    parser.add_argument(
        "--sequence_length",
        type=int,
        default=DEFAULT_SEQUENCE_LENGTH,
        help="The audio sequence length for which the model should be compiled. "
        "This is typically (audio sample length) * (audio length in seconds).",
    )
    args = parser.parse_args()

    # Load Denoiser model
    source_model = FacebookDenoiser.from_pretrained(
        args.checkpoint, args.hidden_layer_count
    )

    # Trace the model.
    traced_model = trace(source_model, args.sequence_length)

    # Select the device you'd like to optimize for.
    devices = [hub.Device(device) for device in args.devices]

    # Submit the traced models for conversion & profiling.
    device_jobs = hub.submit_profile_job(
        name=MODEL_ID,
        model=traced_model,
        input_shapes=source_model.get_input_spec(),
        device=devices,
        options="",
    )

    # Download the optimized assets!
    download_hub_models(device_jobs)


if __name__ == "__main__":
    main()
