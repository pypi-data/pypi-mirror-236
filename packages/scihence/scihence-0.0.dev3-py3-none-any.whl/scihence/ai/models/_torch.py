"""Base PyTorch models."""
from collections.abc import Callable
from copy import deepcopy
from typing import Any

import mlflow
import numpy as np
import pandas as pd
import torch
from sklearn.utils import shuffle
from torch import Tensor, nn
from torch.optim import AdamW

from scihence.ai._data import get_batches
from scihence.ai._io import DaitaFraime
from scihence.ai.experiment_tracking._mlflow import mlflow_log_nested_dict
from scihence.ai.models._utils import (
    check_fitted,
    decode_classes,
    encode_classes_,
    fit_classes_,
    fit_output_columns,
    set_fitted,
)
from scihence.ai.models.processors._base import IdentityProcessor
from scihence.utils._functools import wraps_without_annotations


def pre_post_process(f: Callable) -> Callable:
    def preprocess_f_postprocess(
        self, X: Tensor | list[Tensor], *args, **kwargs
    ) -> Tensor | list[Tensor]:
        X = self.preprocess(X)
        X = f(self, X, *args, **kwargs)
        return self.postprocess(X)

    return preprocess_f_postprocess


def coerce_output(f: Callable) -> Callable:
    @wraps_without_annotations(f)
    def f_then_coerce_output(self, *args, **kwargs):
        X = kwargs.get("X", args[0])
        self.eval()
        with torch.no_grad():
            output = f(self, *args, **kwargs)
        if isinstance(output, list):
            index_tuples = sum(
                [
                    [(seq_idx, item_idx) for item_idx, _ in enumerate(output[i])]
                    for i, seq_idx in enumerate(X.index.get_level_values(0).unique())
                ],
                [],
            )
            index = pd.MultiIndex.from_tuples(index_tuples, names=(X.index.names[0], "item"))
            output = DaitaFraime.from_torch(output, index=index)
        elif isinstance(output, Tensor):
            output = DaitaFraime.from_torch(output, index=X.index.get_level_values(0).unique())
        if f.__name__ == "predict_proba":
            output.columns = pd.MultiIndex.from_product(
                (self.output_columns, pd.Index(self.classes_, name="class"))
            )
            return output
        output.columns = self.output_columns
        if hasattr(self, "classes_"):
            return decode_classes(output, self.class_encoder)
        return output

    return f_then_coerce_output


class BaseTorchModel(nn.Module):

    def __init__(
        self, objective: str, processor=IdentityProcessor(), *args, **kwargs   # noqa: ARG002
    ) -> None:
        super().__init__()
        self.objective = objective
        self.fitted, self.output_columns = False, None
        self._sequential_to_non_sequential = False
        self.processor = processor

    def preprocess(self, X: DaitaFraime) -> DaitaFraime:
        return self.processor.preprocess(X)

    def postprocess(self, Y: DaitaFraime) -> DaitaFraime:
        return self.processor.postprocess(Y)

    @pre_post_process
    def forward(self, X: Tensor | list[Tensor], *args, **kwargs) -> Tensor | list[Tensor]:
        raise NotImplementedError

    @check_fitted
    @coerce_output
    def predict(self, X: DaitaFraime, *args, **kwargs) -> Tensor:
        raise NotImplementedError

    @encode_classes_
    def loss(self, X: DaitaFraime, Y: DaitaFraime, *args, **kwargs) -> Tensor:
        raise NotImplementedError

    @set_fitted
    @fit_output_columns
    def fit(
        self,
        X: DaitaFraime,
        Y: DaitaFraime,
        index_valid: pd.Index | None = None,
        optimizer: dict = {},
        max_epochs: int = 100,
        batch_size: int = 0,
        stop_criteria: Callable[[dict[str, Any]], bool] | None = None,
        track_loss: bool = False,
        save_best_model: bool = False,
        *args,  # noqa: ARG002
        **kwargs,  # noqa: ARG002
    ) -> dict:
        info = {
            "batch_size": batch_size,
            "epoch": 0,
            "max_epochs": max_epochs,
            "optimizer": optimizer,
            "save_best_model": save_best_model,
            "stop_criteria": stop_criteria,
        }
        stop_criteria = stop_criteria if stop_criteria else (lambda _: False)
        optimizer = optimizer.get("class", AdamW)(
            self.parameters(), **optimizer.get("class_kwargs", {})
        )
        validating = index_valid is not None

        with mlflow.start_run(nested=True, run_name=f"Fitting {self.__class__.__name__}"):
            mlflow_log_nested_dict(info)

            self.processor.fit(X, Y=Y, groups=None)

            # this preserves the order of a second index level if sequential
            index = X.index.get_level_values(0).unique()
            index_train = index[~index.isin(index_valid)] if validating else index
            batches_train = get_batches(len(index_train), batch_size, shuffle=True)
            batches_train = [index_train[batch] for batch in batches_train]
            if validating:
                batches_valid = get_batches(len(index_valid), batch_size, shuffle=True)
                batches_valid = [index_valid[batch] for batch in batches_valid]
            else:
                batches_valid = None

            if track_loss:
                info.update({"best_loss": np.inf, "train_loss": []})
                if validating:
                    info["valid_loss"] = []
                self._update_fit_tracking_state(info, X, Y, batches_train, batches_valid)

            for info["epoch"] in range(1, max_epochs + 1):
                self.train()
                for batch in shuffle(batches_train):
                    optimizer.zero_grad()
                    self.loss(X.loc[batch], Y.loc[batch]).backward()
                    optimizer.step()
                if track_loss:
                    self._update_fit_tracking_state(info, X, Y, batches_train, batches_valid)
                if stop_criteria(info):
                    break

            if track_loss:
                mlflow.log_params({k: info[k] for k in ["best_loss", "best_epoch"]})
                if save_best_model:
                    self.load_state_dict(info["best_state_dict"])
        return info

    def _update_fit_tracking_state(
        self,
        info: dict[str, Any],
        X: DaitaFraime,
        Y: DaitaFraime,
        batches_train: list[pd.Index],
        batches_valid: list[pd.Index] | None,
    ) -> None:
        for name, batches in zip(("train", "valid"), (batches_train, batches_valid)):
            if (name == "valid") and (batches_valid is None):
                continue
            info[loss_name:=f"{name}_loss"].append(loss := self.loss(X, Y, batches))
            mlflow.log_metric(loss_name, loss, info["epoch"])

        if loss < info["best_loss"]:
            info.update({"best_epoch": info["epoch"], "best_loss": loss})
            if info["save_best_model"]:
                info["best_state_dict"] = deepcopy(self.state_dict())


mse_loss = nn.MSELoss()

class BaseTorchRegressionModel(BaseTorchModel):

    @check_fitted
    @coerce_output
    def predict(self, *args, **kwargs) -> Tensor:
        return self.forward(*args, **kwargs)

    def loss(self, X: DaitaFraime, Y: DaitaFraime) -> Tensor:
        X = self.forward(X)
        X = torch.cat(X) if isinstance(X, list) else X
        Y = Y.to_torch()
        Y = torch.cat(Y) if isinstance(Y, list)else Y
        return mse_loss(X, Y)


softmax = nn.Softmax(dim=-1)
cross_entropy_loss = nn.CrossEntropyLoss()


class BaseTorchClassificationModel(BaseTorchModel):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.classes_ = None

    @fit_classes_
    def fit(self, *args, **kwargs) -> Any:
        return super().fit(*args, **kwargs)

    @pre_post_process
    def forward(self, X: DaitaFraime, *args, **kwargs) -> Tensor | list[Tensor]:
        # OUTPUT LOGITS
        raise NotImplementedError

    def forward_proba(self, X: DaitaFraime, *args, **kwargs) -> Tensor:
        X = self.forward(X, *args, **kwargs)
        if isinstance(X, list):
            return [softmax(x) for x in X]
        return softmax(X)

    @check_fitted
    @coerce_output
    def predict_proba(self, X: DaitaFraime, *args, **kwargs) -> np.ndarray:
        with torch.no_grad():
            return self.forward_proba(X, *args, **kwargs)

    @check_fitted
    @coerce_output
    def predict(self, X: Tensor | list[Tensor], *args, **kwargs) -> Tensor:
        with torch.no_grad():
            probabilities = self.forward_proba(X, *args, **kwargs)
        if isinstance(probabilities, list):
            return [probability.argmax(axis=-1) for probability in probabilities]
        return probabilities.argmax(axis=-1)

    @encode_classes_
    def loss(self, X: DaitaFraime, Y: DaitaFraime) -> Tensor:
        logits = self.forward(X)
        if isinstance(logits, list):
            logits = torch.cat([logit.transpose(1, 2) for logit in logits])
        else:
            logits = logits.transpose(1, 2)
        Y = Y.to_torch()
        if isinstance(Y, list):
            Y = torch.cat([y.to(int) for y in Y])
        else:
            Y = Y.to(int)
        return cross_entropy_loss(logits, Y)



class Linear3D(nn.Module):

    training: bool = True
    """Whether the module is in training mode, by default it is True."""

    def __init__(self, n_features: int, n_outputs: int, n_classes: int) -> None:
        """Initialise an instance."""
        super().__init__()
        self.weight = nn.Parameter(torch.randn(n_features, n_outputs, n_classes))
        self.bias = nn.Parameter(torch.randn(n_outputs))

    def forward(self, x: Tensor) -> Tensor:
        x = torch.einsum("...j,jkl->...kl", x, self.weight)
        return x + self.bias.reshape(*([1] * (x.ndim - 2)), -1, 1)
