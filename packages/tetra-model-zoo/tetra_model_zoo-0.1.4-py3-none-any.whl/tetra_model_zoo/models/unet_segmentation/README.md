[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [Unet-Segmentation: Real-time segmentation optimized for mobile and edge.](https://tetra.ai/model-zoo/unet_segmentation)

UNet is a machine learning model that produces a segmentation mask for an image. The most basic use case will label each pixel in the image as being in the foreground or the background. More advanced usage will assign a class label to each pixel. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of Unet-Segmentation found [here](https://github.com/milesial/Pytorch-UNet).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/unet_segmentation


## Example & Usage

Run the demo:
```bash
python -m tetra_model_zoo.models.unet_segmentation.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate Unet-Segmentation for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate Unet-Segmentation for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.unet_segmentation.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using Unet-Segmentation in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of Unet-Segmentation can be found [here](https://github.com/milesial/Pytorch-UNet/blob/master/LICENSE).


## References
* [U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)
* [Source Model Implementation](https://github.com/milesial/Pytorch-UNet)
