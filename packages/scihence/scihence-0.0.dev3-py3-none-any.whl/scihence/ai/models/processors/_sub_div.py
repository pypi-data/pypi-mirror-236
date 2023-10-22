"""Subtraction then division pre/post processor."""

from collections.abc import Callable

import numpy as np
import torch
from torch import Tensor, tensor

from scihence.ai._io import DaitaFraime
from scihence.ai.models._utils import check_fitted, set_fitted
from scihence.ai.models.processors._base import BaseProcessor


def postprocess_sequential(f: Callable) -> Callable:

    def standardise_process_sequentialise(self, x: Tensor | list[Tensor]) -> Tensor | list[Tensor]:
        if sequential := DaitaFraime.is_coercible(x, sequential=True, from_type="torch"):
            seq_lens = [len(seq) for seq in x]
            x = torch.cat(x)
        x = f(self, x)
        if sequential:
            return np.split(x, np.cumsum(seq_lens)[:-1])
        return x

    return standardise_process_sequentialise


class SubtractDivideProcessor(BaseProcessor):

    supported_kinds: tuple[str, str] = ("standard", "minmax")
    """Kinds of :class:`SubtractDivideProcessor` that are supported."""

    def __init__(self, kind: str = "standard", eps: float = 1e-8, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kind not in self.supported_kinds:
            raise ValueError(
                f"SubtractDivideProcessor kind={kind} not supported, must be one of "
                f"{self.supported_kinds}."
            )
        self.kind = kind
        self.eps = eps
        self.X_sub, self.X_div = None, None
        if self.process_outputs:
            self.Y_sub, self.Y_div = None, None

    @set_fitted
    def fit(self, X: DaitaFraime, Y: DaitaFraime | None = None, groups: list | None = None) -> None:
        self.groups = np.arange(n_features := X.shape[1]) if groups is None else groups
        unique_groups = np.unique(self.groups)

        self.X_sub = np.empty((1, n_features))
        self.X_div = np.empty_like(self.X_sub)

        for group in unique_groups:
            cols_of_group = X.columns[idxs_of_group := (self.groups == group)]
            if self.kind == "standard":
                self.X_sub[:, idxs_of_group] = X[cols_of_group].mean()
                self.X_div[:, idxs_of_group] = X[cols_of_group].std(ddof=0)
            elif self.kind == "minmax":
                self.X_sub[:, idxs_of_group] = X[cols_of_group].min()
                self.X_div[:, idxs_of_group] = X[cols_of_group].max() - self.X_sub[:, idxs_of_group]

        if self.process_outputs:
            kwargs = {"axis": 0, "keepdims": True}
            if self.kind == "standard":
                self.Y_sub = Y.values.mean(**kwargs)
                self.Y_div = Y.values.std(**kwargs)
            elif self.kind == "minmax":
                self.Y_sub = Y.values.min(**kwargs)
                self.Y_div = Y.values.max(**kwargs) - self.Y_sub


    @check_fitted
    def preprocess(self, X: DaitaFraime) -> DaitaFraime:
        return (X - self.X_sub) / (self.X_div + self.eps)

    @check_fitted
    @postprocess_sequential
    def postprocess(self, Y: Tensor | list[Tensor]) -> Tensor | list[Tensor]:
        if self.process_outputs:
            dtyp = torch.get_default_dtype()
            return Y * (tensor(self.Y_div, dtype=dtyp) + self.eps) + tensor(self.Y_sub, dtype=dtyp)
        return Y
