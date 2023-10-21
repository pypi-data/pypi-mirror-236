[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [AOT-GAN: High resolution image in-painting on-device.](https://tetra.ai/model-zoo/aotgan)

AOT-GAN is a machine learning model that allows to erase and in-paint part of given input image. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of AOT-GAN found [here](https://github.com/researchmm/AOT-GAN-for-Inpainting).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/aotgan


## Example & Usage

Run the demo:
```bash
python -m tetra_model_zoo.models.aotgan.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate AOT-GAN for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate AOT-GAN for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.aotgan.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using AOT-GAN in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of AOT-GAN can be found [here](This model's original implementation does not provide a LICENSE.).


## References
* [Aggregated Contextual Transformations for High-Resolution Image Inpainting](https://arxiv.org/abs/2104.01431)
* [Source Model Implementation](https://github.com/researchmm/AOT-GAN-for-Inpainting)
