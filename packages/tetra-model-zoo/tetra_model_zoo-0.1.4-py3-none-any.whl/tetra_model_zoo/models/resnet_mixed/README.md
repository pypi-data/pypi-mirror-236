[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [ResNet-Mixed-Convolution: Sports and human action recognition in videos.](https://tetra.ai/model-zoo/resnet_mixed)

ResNet Mixed Convolutions is a network with a mixture of 2D and 3D convolutions used for video understanding. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of ResNet-Mixed-Convolution found [here](https://github.com/pytorch/vision/blob/main/torchvision/models/video/resnet.py).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/resnet_mixed


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[resnet_mixed]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.resnet_mixed.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate ResNet-Mixed-Convolution for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate ResNet-Mixed-Convolution for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.resnet_mixed.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using ResNet-Mixed-Convolution in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of ResNet-Mixed-Convolution can be found [here](https://github.com/pytorch/vision/blob/main/LICENSE).


## References
* [A Closer Look at Spatiotemporal Convolutions for Action Recognition](https://arxiv.org/abs/1711.11248)
* [Source Model Implementation](https://github.com/pytorch/vision/blob/main/torchvision/models/video/resnet.py)
