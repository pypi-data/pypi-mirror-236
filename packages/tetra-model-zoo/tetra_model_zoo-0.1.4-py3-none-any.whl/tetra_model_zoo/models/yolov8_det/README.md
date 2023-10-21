[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [Yolo-v8-Detection: Real-time object detection optimized for mobile and edge.](https://tetra.ai/model-zoo/yolov8_det)

YoloV8 is a machine learning model that predicts bounding boxes and classes of objects in an image. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of Yolo-v8-Detection found [here](https://github.com/ultralytics/ultralytics/tree/main/ultralytics/models/yolo/detect).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/yolov8_det


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[yolov8_det]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.yolov8_det.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate Yolo-v8-Detection for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate Yolo-v8-Detection for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.yolov8_det.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using Yolo-v8-Detection in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of Yolo-v8-Detection can be found [here](https://github.com/meituan/YOLOv8/blob/47625514e7480706a46ff3c0cd0252907ac12f22/LICENSE).


## References
* [Real-Time Flying Object Detection with YOLOv8](https://arxiv.org/abs/2305.09972)
* [Source Model Implementation](https://github.com/ultralytics/ultralytics/tree/main/ultralytics/models/yolo/detect)
