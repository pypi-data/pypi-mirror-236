[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [DETR-RestNet50-DC5: Transformer based object detector with ResNet50 backbone (dilated C5 stage).](https://tetra.ai/model-zoo/detr_resnet50_dc5)

DETR is a machine learning model that can detect objects (trained on COCO dataset). We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of DETR-RestNet50-DC5 found [here](https://github.com/facebookresearch/detr).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/detr_resnet50_dc5


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[detr_resnet50_dc5]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.detr_resnet50_dc5.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate DETR-RestNet50-DC5 for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate DETR-RestNet50-DC5 for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.detr_resnet50_dc5.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using DETR-RestNet50-DC5 in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of DETR-RestNet50-DC5 can be found [here](https://github.com/facebookresearch/detr/blob/main/LICENSE).


## References
* [End-to-End Object Detection with Transformers](https://arxiv.org/abs/2005.12872)
* [Source Model Implementation](https://github.com/facebookresearch/detr)
