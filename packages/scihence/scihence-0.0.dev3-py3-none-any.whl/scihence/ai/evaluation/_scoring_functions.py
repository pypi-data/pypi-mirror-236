"""Scoring functions."""
from collections.abc import Callable
from typing import Any, Literal

import pandas as pd
from sklearn.metrics import fbeta_score

from scihence.ai._io import DaitaFraime
from scihence.ai.models._utils import ModelObjective


def get_new_score_better_func(greater_score_better: bool) -> Callable[[float, float], bool]:
    """Get a function that will return whether a new score is better than an older one.

    Args:
        greater_score_better: Whether a new score being greater than an old one is better.

    Returns:
        Function that will take in an old score and a new score and output whether the new one is
        better.

    Examples:
        Greater score is better:

        >>> new_score_better = get_new_score_better_func(greater_score_better=True)
        >>> new_score_better(new=1, old=0)
        True
        >>> new_score_better(new=1, old=1)
        False

        Lesser score is better:

        >>> new_score_better = get_new_score_better_func(greater_score_better=False)
        >>> new_score_better(new=0, old=1)
        True
        >>> new_score_better(new=1, old=1)
        False
    """

    def new_score_better(new: float, old: float) -> bool:
        """Determine whether a new score is better than an old one.

        Args:
            new: New score.
            old: Old score.

        Returns:
            True if the new score is better else False.
        """
        if greater_score_better:
            return new > old
        return new < old

    return new_score_better


def get_scoring_function(
    scoring_function: Callable | str,
    greater_score_better: bool | None = None,
    objective: ModelObjective | None = None,
) -> tuple[Callable, Callable[[float, float], bool]]:
    """Get the scoring function as a callable function.

    If a callable is passed, it will leave it untouched, with the exception of wrapping it to allow
    it to handle variale length inputs.

    Args:
        scoring_function: The inputted scoring function, as a string or function. If specified as
            "auto", will choose F1 if a classification objective or will choose MAE if a regression
            objective. If specified as a string, can be any of {"accuracy", "f1", "mae", "mape",
            "mse"} (will automatically be converted to lower case). If a function, the callable must
            have signature :code:`(model, X, Y, *args, **kwargs)`.
        greater_score_better: Whether a greater score is better. Only required if
            :func:`scoring_function` is not specified as a string. Defualts to None.
        objective: Objective of the learning problem, from {"binary", "multiclass",
            "mulitlabel-indicator", "multiclass-multioutput", "continuous", "continuous-multioutput"
            }. Only required if :func:`scoring_function` is :code:`auto`. Defaults to :code:`None`.

    Raises:
        ValueError: If :code:`scoring_function == "auto"` but :code:`greater_score_better` is not
            specified.
        ValueError: If unsupported scoring function string input.

    Returns:
        Scoring function, and :code:`new_score_better` function.
    """
    if not isinstance(scoring_function, str):
        if greater_score_better is None:
            raise ValueError(
                "scoring_function defined as a callable but greater_score_better is 'auto'."
            )
        return scoring_function, get_new_score_better_func(greater_score_better)

    scoring_function = scoring_function.lower()

    def greater_score_better_error_message():
        """Raise an error if :func:`scoring_function` disagrees with :code:`greater_score_better`.

        Raises:
            ValueError: Describes how the :func:`scoring_function` does not align with
            :code:`greater_score_better`.
        """
        raise ValueError(
            f"{scoring_function} scoring function is at odds with greater_score_better = "
            f"{greater_score_better}."
        )

    if scoring_function == "auto":
        if objective is None:
            raise ValueError("Model objective must be given if scoring_function is not specified.")
        if objective in ModelObjective.filter("classification"):
            return f_beta_score, get_new_score_better_func(greater_score_better=True)
        elif objective in ModelObjective.filter("regression"):
            return mean_absolute_error, get_new_score_better_func(greater_score_better=False)

    elif scoring_function == "accuracy":
        if greater_score_better is False:
            greater_score_better_error_message()
        return accuracy, get_new_score_better_func(greater_score_better=True)

    elif scoring_function == "f1":
        if greater_score_better is False:
            greater_score_better_error_message()
        return f_beta_score, get_new_score_better_func(greater_score_better=True)

    elif scoring_function == "mae":
        if greater_score_better:
            greater_score_better_error_message()
        return mean_absolute_error, get_new_score_better_func(greater_score_better=False)

    elif scoring_function == "mape":
        if greater_score_better:
            greater_score_better_error_message()
        return mean_absolute_percentage_error, get_new_score_better_func(greater_score_better=False)

    elif scoring_function == "mse":
        if greater_score_better:
            greater_score_better_error_message()
        return mean_squared_error, get_new_score_better_func(greater_score_better=False)

    raise ValueError("Unsupported scoring function.")


def accuracy(model: Any, X: DaitaFraime, Y: DaitaFraime) -> DaitaFraime:
    """Get the accuracy for each output of a classification model for given inputs and targets.

    Args:
        model: Classification ML model.
        X: Input data.
        Y: Target data.

    Returns:
        Accuracy score(s).
    """
    return (model.predict(X) == Y).mean(axis=0)


def mean_absolute_error(model: Any, X: DaitaFraime, Y: DaitaFraime) -> DaitaFraime:
    """Get the mean absolute error for each output of a regression model.

    Args:
        model: Classification ML model.
        X: Input data.
        Y: Target data.

    Returns:
        Mean absolute error score(s).
    """
    return (model.predict(X) - Y).abs().mean(axis=0)


def mean_absolute_percentage_error(
    model: Any, X: DaitaFraime, Y: DaitaFraime, eps: float = 1e-8
) -> DaitaFraime:
    """Get the mean absolute percentage error for each output of a regression model.

    Args:
        model: Classification ML model.
        X: Input data.
        Y: Target data.
        eps: The small addition to add to the denominator to ensure no division by 0. Defaults to
            :code:`1e-8`.

    Returns:
        Mean absolute percentage error score(s).
    """
    return ((model.predict(X) - Y).abs() / (Y.abs() + eps)).mean(axis=0)


def mean_squared_error(model: Any, X: DaitaFraime, Y: DaitaFraime) -> pd.Series:
    """Get the mean squared error for each output of a regression model.

    Args:
        model: Classification ML model.
        X: Input data.
        Y: Target data.

    Returns:
        Mean squared error score(s).
    """
    return ((model.predict(X) - Y) ** 2).mean(axis=0)


def f_beta_score(
    model: Any,
    X: DaitaFraime,
    Y: DaitaFraime,
    beta: float = 1,
    average: Literal["micro", "macro", "weighted"] | None = "micro",
    **kwargs,
) -> pd.Series:
    r"""Get the :math:`F_{\beta}` score for each output of a classification model.

    Args:
        model: Classification ML model.
        X: Input data.
        Y: Target data.
        beta: The beta parameter that specifies how much weighting to the give to the recall, as
            mentioned in :func:`sklearn.metrics.fbeta_score`. Defaults to :code:`1`.
        average: The type of average to take over the classes in a multiclass output, as required by
            :func:`sklearn.metrics.fbeta_score`. Defaults to :code:`"micro"`.
        **kwargs: Keyword arguments to :func:`sklearn.metrics.fbeta_score`.

    Returns:
        :math:`F_{\beta}` score(s).
    """
    predictions = model.predict(X)
    score = pd.Series(index=Y.columns, name="f_beta_score", dtype=float)
    for output in score.index:
        score[output] = fbeta_score(
            Y[output], predictions[output], beta=beta, average=average, **kwargs
        )
    return DaitaFraime.from_pandas(
        score, index=Y.columns, columns=pd.Index(["f_beta"], name="score")
    )
