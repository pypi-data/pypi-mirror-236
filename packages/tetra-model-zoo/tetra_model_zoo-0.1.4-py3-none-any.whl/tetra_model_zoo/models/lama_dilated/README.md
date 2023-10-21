[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [LaMa-Dilated: High resolution image in-painting on-device.](https://tetra.ai/model-zoo/lama_dilated)

LaMa-Dilated is a machine learning model that allows to erase and in-paint part of given input image. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of LaMa-Dilated found [here](https://github.com/advimman/lama).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/lama_dilated


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[lama_dilated]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.lama_dilated.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate LaMa-Dilated for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate LaMa-Dilated for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.lama_dilated.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using LaMa-Dilated in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of LaMa-Dilated can be found [here](https://github.com/advimman/lama/blob/main/LICENSE).


## References
* [Resolution-robust Large Mask Inpainting with Fourier Convolutions](https://arxiv.org/abs/2109.07161)
* [Source Model Implementation](https://github.com/advimman/lama)
