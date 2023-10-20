[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [DDRNet23-Slim: Segment images or video by class in real-time on device.](https://tetra.ai/model-zoo/ddrnet23_slim)

DDRNet23Slim is a machine learning model that segments an image into semantic classes, specifically designed for road-based scenes. It is designed for the application of self-driving cars. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of DDRNet23-Slim found [here](https://github.com/chenjun2hao/DDRNet.pytorch).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/ddrnet23_slim


## Example & Usage

Run the demo:
```bash
python -m tetra_model_zoo.models.ddrnet23_slim.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate DDRNet23-Slim for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate DDRNet23-Slim for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.ddrnet23_slim.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using DDRNet23-Slim in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of DDRNet23-Slim can be found [here](https://github.com/chenjun2hao/DDRNet.pytorch/blob/main/LICENSE).


## References
* [Deep Dual-resolution Networks for Real-time and Accurate Semantic Segmentation of Road Scenes](https://arxiv.org/abs/2101.06085)
* [Source Model Implementation](https://github.com/chenjun2hao/DDRNet.pytorch)
