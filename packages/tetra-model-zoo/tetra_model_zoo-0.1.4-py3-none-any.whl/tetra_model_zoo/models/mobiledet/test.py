import numpy as np
import torch

from tetra_model_zoo.models.mobiledet.app import MobileDetApp
from tetra_model_zoo.models.mobiledet.model import (
    MobileDet,
    _load_mobiledet_source_model_from_backbone,
)
from tetra_model_zoo.utils.testing import skip_clone_repo_check

SEED_VAL = 10


@skip_clone_repo_check
def test_mobiledet_app():
    torch.manual_seed(SEED_VAL)
    model = MobileDet.from_pretrained()

    torch.manual_seed(SEED_VAL)
    input_shape = model.get_input_spec()["image"][0]
    input_data = torch.randn(input_shape)

    app = MobileDetApp(model)
    observed_outputs = app.predict(input_data)

    torch.manual_seed(SEED_VAL)
    model = _load_mobiledet_source_model_from_backbone("dsp")
    expected_outputs = model(input_data)
    for obs, exp in zip(observed_outputs, expected_outputs):
        np.testing.assert_allclose(
            np.asarray(obs.detach().numpy(), dtype=np.float32),
            np.asarray(exp.detach().numpy(), dtype=np.float32),
            rtol=0.02,
            atol=1.5,
        )
