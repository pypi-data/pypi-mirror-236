[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [MediaPipe-Pose-Estimation: Detect and track human body poses in real-time images and video streams.](https://tetra.ai/model-zoo/mediapipe_pose)

The MediaPipe Pose Landmark Detector is a machine learning pipeline that predicts bounding boxes and pose skeletons of poses in an image. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of MediaPipe-Pose-Estimation found [here](https://github.com/zmurez/MediaPipePyTorch/).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/mediapipe_pose


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[mediapipe_pose]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.mediapipe_pose.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate MediaPipe-Pose-Estimation for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate MediaPipe-Pose-Estimation for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.mediapipe_pose.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using MediaPipe-Pose-Estimation in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of MediaPipe-Pose-Estimation can be found [here](https://github.com/zmurez/MediaPipePyTorch/blob/master/LICENSE).


## References
* [BlazePose: On-device Real-time Body Pose tracking](https://arxiv.org/abs/2006.10204)
* [Source Model Implementation](https://github.com/zmurez/MediaPipePyTorch/)
