[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [RegNet: Imagenet classifier and general purpose backbone.](https://tetra.ai/model-zoo/regnet)

RegNet is a machine learning model that can classify images from the Imagenet dataset. It can also be used as a backbone in building more complex models for specific use cases. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of RegNet found [here](https://github.com/pytorch/vision/blob/main/torchvision/models/regnet.py).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/regnet


## Example & Usage

Run the demo:
```bash
python -m tetra_model_zoo.models.regnet.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate RegNet for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate RegNet for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.regnet.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using RegNet in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of RegNet can be found [here](https://github.com/pytorch/vision/blob/main/LICENSE).


## References
* [Revisiting Weakly Supervised Pre-Training of Visual Perception Models](https://arxiv.org/abs/2201.08371)
* [Source Model Implementation](https://github.com/pytorch/vision/blob/main/torchvision/models/regnet.py)
