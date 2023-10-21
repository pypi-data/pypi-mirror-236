[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [MediaPipe-Selfie-Segmentation: Segments the person from background in a selfie image and realtime background segmentation in video conferencing.](https://tetra.ai/model-zoo/mediapipe_selfie)

Light-weight model that segments a person from the background in square or landscape selfie and video conference imagery. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of MediaPipe-Selfie-Segmentation found [here](https://github.com/google/mediapipe/tree/master/mediapipe/modules/selfie_segmentation).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/mediapipe_selfie


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[mediapipe_selfie]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.mediapipe_selfie.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate MediaPipe-Selfie-Segmentation for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate MediaPipe-Selfie-Segmentation for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.mediapipe_selfie.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using MediaPipe-Selfie-Segmentation in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of MediaPipe-Selfie-Segmentation can be found [here](https://github.com/google/mediapipe/blob/master/LICENSE).


## References
* [Image segmentation guide](https://developers.google.com/mediapipe/solutions/vision/image_segmenter/)
* [Source Model Implementation](https://github.com/google/mediapipe/tree/master/mediapipe/modules/selfie_segmentation)
