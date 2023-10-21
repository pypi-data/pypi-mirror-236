[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [Yolo-v6: Real-time object detection optimized for mobile and edge.](https://tetra.ai/model-zoo/yolov6)

YoloV6 is a machine learning model that predicts bounding boxes and classes of objects in an image. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of Yolo-v6 found [here](https://github.com/meituan/YOLOv6/).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/yolov6


## Example & Usage

Run the demo:
```bash
python -m tetra_model_zoo.models.yolov6.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate Yolo-v6 for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate Yolo-v6 for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.yolov6.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using Yolo-v6 in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of Yolo-v6 can be found [here](https://github.com/meituan/YOLOv6/blob/47625514e7480706a46ff3c0cd0252907ac12f22/LICENSE).


## References
* [YOLOv6: A Single-Stage Object Detection Framework for Industrial Applications](https://arxiv.org/abs/2209.02976)
* [Source Model Implementation](https://github.com/meituan/YOLOv6/)
