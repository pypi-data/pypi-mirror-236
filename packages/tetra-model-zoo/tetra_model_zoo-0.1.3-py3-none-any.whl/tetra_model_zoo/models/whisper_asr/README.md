[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [Whisper-Base: Translate speech to text, in real time.](https://tetra.ai/model-zoo/whisper_asr)

Whisper is a state of art speech recognition model from OpenAI. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of Whisper-Base found [here](https://github.com/openai/whisper/tree/main).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/whisper_asr


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[whisper_asr]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.whisper_asr.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate Whisper-Base for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate Whisper-Base for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.whisper_asr.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using Whisper-Base in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of Whisper-Base can be found [here](This model's original implementation does not provide a LICENSE.).


## References
* [Robust Speech Recognition via Large-Scale Weak Supervision](https://cdn.openai.com/papers/whisper.pdf)
* [Source Model Implementation](https://github.com/openai/whisper/tree/main)
