[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [Densenet-121: Imagenet classifier and general purpose backbone.](https://tetra.ai/model-zoo/densenet121)

Densenet is a machine learning model that can classify images from the Imagenet dataset. It can also be used as a backbone in building more complex models for specific use cases. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of Densenet-121 found [here](https://github.com/pytorch/vision/blob/main/torchvision/models/densenet.py).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/densenet121


## Example & Usage

Run the demo:
```bash
python -m tetra_model_zoo.models.densenet121.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate Densenet-121 for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate Densenet-121 for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.densenet121.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using Densenet-121 in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of Densenet-121 can be found [here](https://github.com/pytorch/vision/blob/main/LICENSE).


## References
* [Densely Connected Convolutional Networks](https://arxiv.org/abs/1608.06993)
* [Source Model Implementation](https://github.com/pytorch/vision/blob/main/torchvision/models/densenet.py)
