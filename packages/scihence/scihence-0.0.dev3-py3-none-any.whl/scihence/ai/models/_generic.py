"""Generic model tools for the supervised pipelines."""
from copy import deepcopy
from typing import Any

import numpy as np

from scihence.ai._io import DaitaFraime
from scihence.ai.models._torch import BaseTorchModel
from scihence.ai.models._utils import ModelObjective


def init_fit_generic_model(
    X: DaitaFraime,
    Y: DaitaFraime,
    objective: ModelObjective,
    hyperparam: dict[str, Any],
    fold: tuple[np.ndarray, np.ndarray],
    **kwargs,  # noqa: ARG001
) -> tuple[Any, dict]:
    class_kwargs = hyperparam.get("class_kwargs", {})
    class_kwargs["objective"] = class_kwargs.get("objective", objective)
    model = hyperparam["class"](**class_kwargs)

    fit_kwargs = deepcopy(hyperparam.get("fit_kwargs", {}))
    if len(fold[1]) > 0 and isinstance(model, BaseTorchModel):
        fit_kwargs["index_valid"] = fold[1]

    fit_output = model.fit(X, Y, **fit_kwargs)
    return model, fit_output
