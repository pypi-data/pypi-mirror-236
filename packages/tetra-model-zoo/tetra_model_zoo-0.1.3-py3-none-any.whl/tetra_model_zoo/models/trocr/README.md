[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [TrOCR: Real-time optical character recognition.](https://tetra.ai/model-zoo/trocr)

TrOCR is a transformer model that converts single-lines of writing in images to text output. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of TrOCR found [here](https://huggingface.co/microsoft/trocr-small-stage1).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/trocr


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[trocr]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.trocr.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate TrOCR for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate TrOCR for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.trocr.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using TrOCR in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of TrOCR can be found [here](https://github.com/microsoft/unilm/blob/master/LICENSE).


## References
* [TrOCR: Transformer-based Optical Character Recognition with Pre-trained Models](https://arxiv.org/abs/2109.10282)
* [Source Model Implementation](https://huggingface.co/microsoft/trocr-small-stage1)
