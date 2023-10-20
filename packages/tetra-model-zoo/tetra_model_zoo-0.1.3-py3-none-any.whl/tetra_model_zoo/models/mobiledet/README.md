[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [MobileDet: Accelerated Detection backbone.](https://tetra.ai/model-zoo/mobiledet)

MobileDet are discovered using Neural Architecture Search(NAS) which places regular convolutions in certain way as compared to using inverted bottleneck layers(widely used in detection architectures). We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of MobileDet found [here](https://github.com/tetraai/mobiledet-pytorch).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/mobiledet


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[mobiledet]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.mobiledet.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate MobileDet for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate MobileDet for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.mobiledet.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using MobileDet in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of MobileDet can be found [here](This model's original implementation does not provide a LICENSE.).


## References
* [MobileDets: Searching for Object Detection Architectures for Mobile Accelerators](https://arxiv.org/abs/2004.14525v3)
* [Source Model Implementation](https://github.com/tetraai/mobiledet-pytorch)
