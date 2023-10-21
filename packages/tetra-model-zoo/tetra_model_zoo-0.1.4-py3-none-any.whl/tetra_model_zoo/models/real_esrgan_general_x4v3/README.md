[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [Real-ESRGAN-General-x4v3: Upscale images and remove image noise.](https://tetra.ai/model-zoo/real_esrgan_general_x4v3)

Real-ESRGAN is a machine learning model that upscales an image with no loss in quality. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of Real-ESRGAN-General-x4v3 found [here](https://github.com/xinntao/Real-ESRGAN/tree/master).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/real_esrgan_general_x4v3


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[real_esrgan_general_x4v3]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.real_esrgan_general_x4v3.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate Real-ESRGAN-General-x4v3 for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate Real-ESRGAN-General-x4v3 for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.real_esrgan_general_x4v3.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using Real-ESRGAN-General-x4v3 in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of Real-ESRGAN-General-x4v3 can be found [here](https://github.com/xinntao/Real-ESRGAN/blob/master/LICENSE).


## References
* [Real-ESRGAN: Training Real-World Blind Super-Resolution with Pure Synthetic Data](https://arxiv.org/abs/2107.10833)
* [Source Model Implementation](https://github.com/xinntao/Real-ESRGAN/tree/master)
