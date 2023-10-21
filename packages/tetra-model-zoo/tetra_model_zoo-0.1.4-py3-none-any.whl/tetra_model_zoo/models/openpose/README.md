[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [OpenPose: Human pose estimation.](https://tetra.ai/model-zoo/openpose)

OpenPose is a machine learning model that estimates body and hand pose in an image and returns location and confidence for each of 19 joints. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of OpenPose found [here](https://github.com/CMU-Perceptual-Computing-Lab/openpose).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/openpose


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[openpose]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.openpose.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate OpenPose for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate OpenPose for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.openpose.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using OpenPose in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of OpenPose can be found [here](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/LICENSE).


## References
* [OpenPose: Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields](https://arxiv.org/abs/1812.08008)
* [Source Model Implementation](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
