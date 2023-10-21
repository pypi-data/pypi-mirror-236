[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [Optimized-Clip: Multi-modal model that learns the correspondence between natural language and images.](https://tetra.ai/model-zoo/optimized_clip)

CLIP (Contrastive Language-Image Pre-Training) is a neural network trained on a variety of (image, text) pairs. It can be instructed in natural language to predict the most relevant text snippet, given an image. This version of clip has been optimized using modules provided by [ANE Transformers](https://github.com/apple/ml-ane-transformers) repository provided by Apple. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of Optimized-Clip found [here](https://github.com/apple/ml-ane-transformers).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/optimized_clip


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[optimized_clip]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.optimized_clip.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate Optimized-Clip for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate Optimized-Clip for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.optimized_clip.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using Optimized-Clip in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of Optimized-Clip can be found [here](https://github.com/apple/ml-ane-transformers/blob/main/LICENSE.md).


## References
* [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020)
* [Source Model Implementation](https://github.com/apple/ml-ane-transformers)
