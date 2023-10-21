from __future__ import annotations

import tetra_hub as hub
from tetra_model_zoo.models.resnet_mixed.model import MODEL_ID, ResNet_2plus1D
from tetra_model_zoo.utils.args import base_export_parser
from tetra_model_zoo.utils.hub import download_hub_models


def main():
    # Export parameters
    parser = base_export_parser()
    args = parser.parse_args()

    # Instantiate the model
    model = ResNet_2plus1D.from_pretrained()

    # Select the device(s) you'd like to optimize for.
    devices = [hub.Device(x) for x in args.devices]

    # Submit the traced models for conversion & profiling.
    jobs = hub.submit_profile_job(
        name=MODEL_ID,
        model=model,
        input_shapes=model.get_input_spec(),
        device=devices,
    )

    # Download the optimized asset!
    download_hub_models(jobs)


if __name__ == "__main__":
    main()
