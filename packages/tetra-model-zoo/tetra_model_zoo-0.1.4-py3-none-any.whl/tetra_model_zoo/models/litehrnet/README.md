[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [LiteHRNet: Human pose estimation.](https://tetra.ai/model-zoo/litehrnet)

LiteHRNet is a machine learning model that detects human pose and returns a location and confidence for each of 17 joints. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of LiteHRNet found [here](https://github.com/HRNet/Lite-HRNet).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/litehrnet


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[litehrnet]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.litehrnet.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate LiteHRNet for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate LiteHRNet for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.litehrnet.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using LiteHRNet in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of LiteHRNet can be found [here](https://github.com/HRNet/Lite-HRNet/blob/hrnet/LICENSE).


## References
* [Lite-HRNet: A Lightweight High-Resolution Network](https://arxiv.org/abs/2104.06403)
* [Source Model Implementation](https://github.com/HRNet/Lite-HRNet)
