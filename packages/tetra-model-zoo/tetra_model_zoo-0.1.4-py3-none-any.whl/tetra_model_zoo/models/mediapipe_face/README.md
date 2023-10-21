[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [MediaPipe-Face-Detection: Understand and process facial data in real-time video and image streams.](https://tetra.ai/model-zoo/mediapipe_face)

The MediaPipe Face Landmark Detector is a machine learning pipeline that predicts bounding boxes and pose skeletons of faces in an image. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of MediaPipe-Face-Detection found [here](https://github.com/zmurez/MediaPipePyTorch/).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/mediapipe_face


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[mediapipe_face]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.mediapipe_face.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate MediaPipe-Face-Detection for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate MediaPipe-Face-Detection for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.mediapipe_face.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using MediaPipe-Face-Detection in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of MediaPipe-Face-Detection can be found [here](https://github.com/zmurez/MediaPipePyTorch/blob/master/LICENSE).


## References
* [BlazeFace: Sub-millisecond Neural Face Detection on Mobile GPUs](https://arxiv.org/abs/1907.05047)
* [Source Model Implementation](https://github.com/zmurez/MediaPipePyTorch/)
