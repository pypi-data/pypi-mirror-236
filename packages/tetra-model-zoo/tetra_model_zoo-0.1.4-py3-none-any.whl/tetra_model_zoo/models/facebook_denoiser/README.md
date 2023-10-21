[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [Facebook Denoiser: Real-time speech denoising optimized for mobile and edge.](https://tetra.ai/model-zoo/facebook_denoiser)

Facebook Denoiser is a machine learning model that can denoise & isolate voices in sound clips. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of Facebook Denoiser found [here](https://github.com/facebookresearch/denoiser).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/facebook_denoiser


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[facebook_denoiser]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.facebook_denoiser.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate Facebook Denoiser for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate Facebook Denoiser for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.facebook_denoiser.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using Facebook Denoiser in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of Facebook Denoiser can be found [here](https://github.com/facebookresearch/denoiser/blob/main/LICENSE).


## References
* [Real Time Speech Enhancement in the Waveform Domain](https://arxiv.org/abs/2006.12847)
* [Source Model Implementation](https://github.com/facebookresearch/denoiser)
