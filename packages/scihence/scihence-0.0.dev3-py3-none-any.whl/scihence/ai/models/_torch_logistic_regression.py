"""PyTorch logistic regression model."""
from collections import OrderedDict

from torch import Tensor, nn

from scihence.ai._io import DaitaFraime
from scihence.ai.models._torch import BaseTorchClassificationModel, Linear3D, pre_post_process


class TorchLogisticRegression(BaseTorchClassificationModel):

    def __init__(self, n_features: int, n_classes: int = 2, n_outputs: int = 1, **kwargs) -> None:
        super().__init__(**kwargs)
        self.layers = nn.Sequential(
            OrderedDict(
                [("Dense", Linear3D(n_features, n_outputs, n_classes)), ("Sigmoid", nn.Sigmoid())]
            )
        )

    @pre_post_process
    def forward(self, X: DaitaFraime) -> Tensor:
        return self.layers(X.to_torch())
