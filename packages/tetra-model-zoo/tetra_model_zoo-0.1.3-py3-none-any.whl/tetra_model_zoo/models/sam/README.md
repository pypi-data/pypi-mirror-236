[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [Segment-Anything-Model: Generate high quality segmentation mask with light-weight decoder on device.](https://tetra.ai/model-zoo/sam)

SegmentAnything is a Transformer based model for image segmentation.
This model follows encoder-decoder architecture:
  - Large and heavy image encoder to generate image embeddings
  - Light-weight decoder to work on image embedding for point and mask based segmentation

This model is a great example of using cloud and edge together where large model runs over the cloud and light weight model runs on the edge and performs multiple segmentations locally.
We present both,
  - Encoder (suitable for cloud deployment)
  - Decoder (suitable for low latency mobile/edge application).
 We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of Segment-Anything-Model found [here](https://github.com/tetraai/segment-anything).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/sam


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[sam]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.sam.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate Segment-Anything-Model for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate Segment-Anything-Model for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.sam.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using Segment-Anything-Model in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of Segment-Anything-Model can be found [here](https://github.com/facebookresearch/segment-anything/blob/main/LICENSE).


## References
* [Segment Anything](https://arxiv.org/abs/2304.02643)
* [Source Model Implementation](https://github.com/tetraai/segment-anything)
