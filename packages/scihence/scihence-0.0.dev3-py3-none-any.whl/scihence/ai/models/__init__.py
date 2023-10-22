"""Model objects for AI."""
from . import processors
from ._sequential_torch import (
    TorchRNNSequenceClassifier,
    TorchRNNSequenceRegressor,
    TorchRNNSequenceToSequenceClassifier,
    TorchRNNSequenceToSequenceRegressor,
)
from ._sklearn_logistic_regression import (
    init_fit_sklearn_logistic_regression,
    interpret_sklearn_logistic_regression,
)
from ._sklearn_ridge_regression import (
    init_fit_sklearn_ridge_regression,
    interpret_sklearn_ridge_regression,
)
from ._torch import (
    BaseTorchClassificationModel,
    BaseTorchModel,
    BaseTorchRegressionModel,
    Linear3D,
    coerce_output,
    pre_post_process,
)
from ._torch_linear_regression import TorchLinearRegression
from ._torch_logistic_regression import TorchLogisticRegression
from ._utils import (
    ModelObjective,
    check_fitted,
    decode_classes,
    encode_classes,
    set_fitted,
)
from ._xgboost import ScihenceXGBClassifier, init_fit_xgboost, interpret_xgboost

__all__ = [
    "BaseTorchClassificationModel",
    "BaseTorchModel",
    "BaseTorchRegressionModel",
    "check_fitted",
    "coerce_output",
    "decode_classes",
    "encode_classes",
    "format_sklearn_api_model_outputs",
    "init_fit_sklearn_logistic_regression",
    "init_fit_sklearn_ridge_regression",
    "init_fit_xgboost",
    "interpret_sklearn_logistic_regression",
    "interpret_sklearn_ridge_regression",
    "interpret_xgboost",
    "Linear3D",
    "ModelObjective",
    "pre_post_process",
    "processors",
    "ScihenceXGBClassifier",
    "set_fitted",
    "torch",
    "TorchLinearRegression",
    "TorchLogisticRegression",
    "TorchRNNSequenceClassifier",
    "TorchRNNSequenceRegressor",
    "TorchRNNSequenceToSequenceClassifier",
    "TorchRNNSequenceToSequenceRegressor",
]
