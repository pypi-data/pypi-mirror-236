"""Base pre/post-processors."""

from typing import Any

from scihence.ai.models._utils import check_fitted, set_fitted


class BaseProcessor:

    def __init__(self, *, process_outputs: bool = False) -> None:
        self.fitted = False
        self.process_outputs = process_outputs

    @set_fitted
    def fit(self, *args, **kwargs) -> None:
        raise NotImplementedError("Processor has no fit function.")

    @check_fitted
    def preprocess(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Processor has no preprocess function.")

    @check_fitted
    def postprocess(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Processor has no postprocess function.")

    @check_fitted
    def inv_postprocess(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Processor has no inv_postprocess function.")


def identity(*args, **kwargs):
    if (len(args) == 1) and (len(kwargs) == 0):
        return args[0]
    if (len(args) == 0) and (len(kwargs) == 1):
        return next(iter(kwargs.values()))
    return *args, *kwargs.values()


class IdentityProcessor(BaseProcessor):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fitted = True
        self.postprocess = self.inv_postprocess = self.preprocess

    @set_fitted
    def fit(self, *args, **kwargs) -> None:
        pass

    @check_fitted
    def preprocess(self, *args, **kwargs) -> Any:
        return identity(*args, **kwargs)
