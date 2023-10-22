"""ML model utilities."""
import enum
from collections.abc import Callable
from typing import Any, Self

import numpy as np
import pandas as pd
from sklearn.multioutput import MultiOutputClassifier, MultiOutputRegressor
from sklearn.preprocessing import LabelEncoder

from scihence.ai._io import DaitaFraime
from scihence.utils._functools import wraps_without_annotations


def set_fitted(fit: Callable) -> Callable:
    @wraps_without_annotations(fit)
    def fit_and_set_fitted(self, *args, **kwargs) -> Any:
        output = fit(self, *args, **kwargs)
        self.fitted = True
        return output
    return fit_and_set_fitted


def check_fitted(f: Callable) -> Callable:
    @wraps_without_annotations(f)
    def check_fitted_then_f(self, *args, **kwargs) -> Any:
        if self.fitted:
            return f(self, *args, **kwargs)
        raise NotImplementedError("Requires fitting first.")
    return check_fitted_then_f


def fit_output_columns(fit: Callable) -> Callable:
    @wraps_without_annotations(fit)
    def save_output_format_and_fit(
        self, X: DaitaFraime, Y: DaitaFraime, *args, **kwargs
    ) -> Callable:
        self.output_columns = Y.columns
        return fit(self, X, Y, *args, **kwargs)
    return save_output_format_and_fit


def fit_classes_(f: Callable) -> Callable:
    """Decorate the :meth:`fit` method to assign classes with optionally string labels.

    Args:
        f: Fit method to decorate.

    Returns:
        Decorated fit method.
    """
    @wraps_without_annotations(f)
    def fit_classes_and_fit(
        self, X: DaitaFraime | np.ndarray, Y: DaitaFraime, *args, **kwargs
    ) -> Any:
        """Encode the string labels of the classifier as integers.

        Encode the string classes of the classifier to integers, pass the encodings through the
        :func:`fit` method and then set the :code:`classes_` variable back to the optionally string
        classes.

        Args:
            self: Instance of the model.
            X: Input data.
            Y: Target data.
            *args: Positional arguments supplied to the :meth:`fit` method.
            **kwargs: Keyword arguments supplied to the :meth:`fit` method.

        Returns:
            Outputs of the original :meth:`fit` method.
        """
        if isinstance(Y, np.ndarray):
            Y = DaitaFraime.from_numpy(Y.reshape(-1, 1) if Y.ndim == 1 else Y)
        self.class_encoder = LabelEncoder().fit(Y._dataframe.stack())
        self.classes_ = self.class_encoder.classes_
        output = f(self, X, Y, *args, **kwargs)
        self.classes_ = self.class_encoder.classes_
        return output

    return fit_classes_and_fit


def encode_classes(Y: DaitaFraime, class_encoder: LabelEncoder) -> DaitaFraime:
    Y, state = Y.save_state_and_stack()
    Y = class_encoder.transform(Y)
    return DaitaFraime.from_stacked(Y, state)


def encode_classes_(f: Callable) -> Callable:
    @wraps_without_annotations(f)
    def encode_classes_and_predict(self, X: DaitaFraime, Y: DaitaFraime, *args, **kwargs) -> Any:
        Y = encode_classes(Y, self.class_encoder)
        return f(self, X, Y, *args, **kwargs)
    return encode_classes_and_predict


def decode_classes(
    predictions: DaitaFraime, class_encoder: LabelEncoder, numpy: bool = False
) -> DaitaFraime:
    if numpy:
        one_d = predictions.ndim == 1
        predictions = DaitaFraime.from_numpy(predictions.reshape(-1, 1) if one_d else predictions)
    predictions, state = predictions.save_state_and_stack()
    predictions = class_encoder.inverse_transform(predictions)
    predictions = DaitaFraime.from_stacked(predictions, state)
    if numpy:
        predictions = predictions.to_numpy()
        if one_d:
            return predictions.reshape(-1)
    return predictions


def decode_classes_(numpy: bool = False):

    def decode_classes_decorator(f: Callable) -> Callable:
        """Decorate a :meth:`predict` method to output the class labels as initially input.

        Args:
            f: Prediction method.

        Returns:
            Decorated prediction method.
        """
        @wraps_without_annotations(f)
        def predict_and_decode_classes(self, *args, **kwargs) -> np.ndarray:
            """Predict then convert the classes into the same format as initially input.

            Args:
                self: Instance of the model.
                *args: Positional arguments supplied to the :meth:`predict` method.
                **kwargs: Keyword arguments supplied to the :meth:`predict` method..

            Returns:
                Formatted prediction.
            """
            return decode_classes(f(self, *args, **kwargs), self.class_encoder, numpy=numpy)
        return predict_and_decode_classes
    return decode_classes_decorator


@enum.unique
class ModelObjective(enum.Enum):

    def _generate_next_value_(name: str, *args, **kwargs) -> str:  # noqa: ARG002
        return name.replace("_", "-").lower()

    BINARY = enum.auto(), [0, 2, 4]
    MULTICLASS = enum.auto(), [0, 2, 5]
    MULTILABEL_INDICATOR = enum.auto(), [0, 3, 4]
    MULTICLASS_MULTIOUTPUT = enum.auto(), [0, 3, 5]
    CONTINUOUS = enum.auto(), [1, 2]
    CONTINUOUS_MULTIOUTPUT = enum.auto(), [1, 3]

    def __new__(cls, value, *args, **kwargs) -> Self:  # noqa: ARG003
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, _, tags: list[int]) -> Self:
        self.tags = tags

    @classmethod
    @property
    def tags(cls) -> dict[str, int]:
        return {
            "classification": 0,
            "regression": 1,
            "single-output": 2,
            "multioutput": 3,
            "binary-class": 4,
            "multiclass": 5,
        }

    @classmethod
    def filter(cls, *tags):
        """Filter the possible model objectives to get only those that have all the tags provided.

        Args:
            *tags: Tags.

        Returns:
            List of objectives that have all of the tags provided.
        """
        output = []
        for objective in cls:
            for tag in tags:
                if cls.tags[tag] not in objective.tags:
                    break
            else:
                output.append(objective.value)
        return output


def set_missing_classes_to_0_prob(
    prob: DaitaFraime | np.ndarray,
    predicted_classes: np.ndarray,
    all_classes: np.ndarray,
) -> np.ndarray:
    """Standardize a single output of a Scikit-learn classifier.

    Standardize so that it contains all of the output classes seen across all outputs.

    Args:
        prob: An instance of :meth:`predict_proba` for one output.
        predicted_classes: Classes that are predicted and in :code:`prob`.
        all_classes: All the output classes of that model that should be predicted.

    Returns:
        Standardized single output for :meth:`predict_proba`.
    """
    formatted_prob = np.zeros((len(prob), len(all_classes)))
    formatted_prob[:, np.where(np.isin(all_classes, predicted_classes))[0]] = prob
    if isinstance(prob, np.ndarray):
        return formatted_prob
    elif isinstance(prob, DaitaFraime):
        return DaitaFraime.from_numpy(
            formatted_prob, index=prob.index, columns=pd.Index(all_classes, name=prob.columns.name)
        )
    raise TypeError()


class ScihenceClassifier(MultiOutputClassifier):

    @set_fitted
    @fit_output_columns
    def fit(self, X, Y, *args, **kwargs):
        output = super().fit(X, Y, *args, **kwargs)
        self.all_classes_ = np.unique(np.hstack(self.classes_))
        return output

    @check_fitted
    def predict(self, X, *args, **kwargs):
        prediction = super().predict(X, *args, **kwargs)
        return DaitaFraime.from_numpy(data=prediction, index=X.index, columns=self.output_columns)

    @check_fitted
    def predict_proba(self, X, *args, **kwargs):
        probs = super().predict_proba(X, *args, **kwargs)
        formatted_probs = np.empty((n_outputs := len(probs), len(X), len(self.all_classes_)))
        for i, prob in enumerate(probs):
            formatted_probs[i] = set_missing_classes_to_0_prob(
                prob, self.classes_[i] if n_outputs > 1 else self.classes_, self.all_classes_
            )
        return DaitaFraime.from_numpy(
            formatted_probs.swapaxes(0, 1), index=X.index, columns=pd.MultiIndex.from_product(
                (self.output_columns, pd.Index(self.all_classes_, name="class"))
            )
        )


class ScihenceRegressor(MultiOutputRegressor):

    @set_fitted
    @fit_output_columns
    def fit(self, *args, **kwargs):
        return super().fit(*args, **kwargs)

    @check_fitted
    def predict(self, X: DaitaFraime, *args, **kwargs):
        prediction = super().predict(X, *args, **kwargs)
        return DaitaFraime.from_numpy(data=prediction, index=X.index, columns=self.output_columns)
