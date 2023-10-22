"""PyTorch linear regression model."""
from collections import OrderedDict

from torch import Tensor, nn

from scihence.ai._io import DaitaFraime
from scihence.ai.models._torch import BaseTorchRegressionModel, pre_post_process


class TorchLinearRegression(BaseTorchRegressionModel):

    def __init__(self, n_features: int, n_outputs: int = 1, **kwargs) -> None:
        super().__init__(**kwargs)
        self.layers = nn.Sequential(OrderedDict([("Dense", nn.Linear(n_features, n_outputs))]))

    @pre_post_process
    def forward(self, X: DaitaFraime) -> Tensor:
        return self.layers(X.to_torch())
