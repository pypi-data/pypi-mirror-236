[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [EfficientNet-B0: Imagenet classifier and general purpose backbone.](https://tetra.ai/model-zoo/efficientnet_b0)

EfficientNetB0 is a machine learning model that can classify images from the Imagenet dataset. It can also be used as a backbone in building more complex models for specific use cases. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of EfficientNet-B0 found [here](https://github.com/pytorch/vision/blob/main/torchvision/models/efficientnet.py).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/efficientnet_b0


## Example & Usage

Run the demo:
```bash
python -m tetra_model_zoo.models.efficientnet_b0.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate EfficientNet-B0 for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate EfficientNet-B0 for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.efficientnet_b0.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using EfficientNet-B0 in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of EfficientNet-B0 can be found [here](https://github.com/pytorch/vision/blob/main/LICENSE).


## References
* [EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks](https://arxiv.org/abs/1905.11946)
* [Source Model Implementation](https://github.com/pytorch/vision/blob/main/torchvision/models/efficientnet.py)
