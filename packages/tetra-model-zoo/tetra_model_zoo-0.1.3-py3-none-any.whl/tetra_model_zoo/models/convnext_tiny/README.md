[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [ConvNext-Tiny: Imagenet classifier and general purpose backbone.](https://tetra.ai/model-zoo/convnext_tiny)

ConvNextTiny is a machine learning model that can classify images from the Imagenet dataset. It can also be used as a backbone in building more complex models for specific use cases. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of ConvNext-Tiny found [here](https://github.com/pytorch/vision/blob/main/torchvision/models/convnext.py).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/convnext_tiny


## Example & Usage

Run the demo:
```bash
python -m tetra_model_zoo.models.convnext_tiny.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate ConvNext-Tiny for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate ConvNext-Tiny for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.convnext_tiny.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using ConvNext-Tiny in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of ConvNext-Tiny can be found [here](https://github.com/pytorch/vision/blob/main/LICENSE).


## References
* [A ConvNet for the 2020s](https://arxiv.org/abs/2201.03545)
* [Source Model Implementation](https://github.com/pytorch/vision/blob/main/torchvision/models/convnext.py)
