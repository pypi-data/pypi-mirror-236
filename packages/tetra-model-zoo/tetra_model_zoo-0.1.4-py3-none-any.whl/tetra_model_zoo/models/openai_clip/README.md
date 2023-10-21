[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [OpenAI-Clip: Open Source version of CLIP model.](https://tetra.ai/model-zoo/openai_clip)

CLIP (Contrastive Language-Image Pre-Training) is a neural network trained on a variety of (image, text) pairs. It can be instructed in natural language to predict the most relevant text snippet, given an image. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of OpenAI-Clip found [here](https://github.com/openai/CLIP/).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/openai_clip


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[openai_clip]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.openai_clip.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate OpenAI-Clip for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate OpenAI-Clip for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.openai_clip.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using OpenAI-Clip in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of OpenAI-Clip can be found [here](https://github.com/openai/CLIP/blob/main/LICENSE).


## References
* [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020)
* [Source Model Implementation](https://github.com/openai/CLIP/)
