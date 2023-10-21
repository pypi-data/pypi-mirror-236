[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [Yolo-v7: Real-time object detection optimized for mobile and edge.](https://tetra.ai/model-zoo/yolov7)

YoloV7 is a machine learning model that predicts bounding boxes and classes of objects in an image. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of Yolo-v7 found [here](https://github.com/WongKinYiu/yolov7/).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/yolov7


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[yolov7]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.yolov7.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate Yolo-v7 for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate Yolo-v7 for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.yolov7.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using Yolo-v7 in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of Yolo-v7 can be found [here](https://github.com/WongKinYiu/yolov7/blob/main/LICENSE.md).


## References
* [YOLOv7: Trainable bag-of-freebies sets new state-of-the-art for real-time object detectors](https://arxiv.org/abs/2207.02696)
* [Source Model Implementation](https://github.com/WongKinYiu/yolov7/)
