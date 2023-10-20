[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [Real-ESRGAN-x4plus: Upscale images and remove image noise.](https://tetra.ai/model-zoo/real_esrgan_x4plus)

Real-ESRGAN is a machine learning model that upscales an image with no loss in quality. The implementation is a derivative of the Real-ESRGAN-x4plus architecture, a larger and more powerful version compared to the Real-ESRGAN-general-x4v3 architecture. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of Real-ESRGAN-x4plus found [here](https://github.com/xinntao/Real-ESRGAN).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/real_esrgan_x4plus


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[real_esrgan_x4plus]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.real_esrgan_x4plus.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate Real-ESRGAN-x4plus for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate Real-ESRGAN-x4plus for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.real_esrgan_x4plus.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using Real-ESRGAN-x4plus in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of Real-ESRGAN-x4plus can be found [here](https://github.com/xinntao/Real-ESRGAN/blob/master/LICENSE).


## References
* [Real-ESRGAN: Training Real-World Blind Super-Resolution with Pure Synthetic Data](https://arxiv.org/abs/2107.10833)
* [Source Model Implementation](https://github.com/xinntao/Real-ESRGAN)
