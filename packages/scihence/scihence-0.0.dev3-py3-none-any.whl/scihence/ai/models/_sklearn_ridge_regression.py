"""Scikit-learn ridge regression model objects for supervised pipelines."""
from typing import Any

import mlflow
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.linear_model import Ridge
from sklearn.multioutput import MultiOutputRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from scihence.ai._io import DaitaFraime
from scihence.ai.models._utils import ScihenceRegressor


def init_fit_sklearn_ridge_regression(
    X: DaitaFraime,
    Y: DaitaFraime,
    hyperparam: dict[str, Any],
    fold: tuple[np.ndarray, np.ndarray],
    **kwargs,  # noqa: ARG001
) -> tuple[Ridge | MultiOutputRegressor, dict]:
    """Initialize and fit a scikit-learn ridge regression model.

    Args:
        X: Input data.
        Y: Target data.
        objective: Objective of the learning problem, from {"continuous", "continuous-multioutput"}.
        hyperparam: Hyperparameter specification.
        fold: Fold specification of indices to use as train and test set.
        **kwargs: Additional keyword arguments.

    Raises:
        ValueError: If the objective is not a regression objective.

    Returns:
        Fitted ridge regression model, and a dictionary that will in future versions be populated
        with information about the fitting procedure.
    """
    ridge = Ridge(**hyperparam.get("class_kwargs", {}))
    preprocessor = hyperparam.get("preprocessor", StandardScaler(with_mean=False, with_std=False))
    model = Pipeline([("Preprocessor", preprocessor), ("RidgeRegression", ridge)])
    model = ScihenceRegressor(model)
    return model.fit(X.loc[fold[0]], Y.loc[fold[0]]), {}


def interpret_sklearn_ridge_regression(
    model: Pipeline, *args, **kwargs  # noqa: ARG001
) -> dict[str, pd.Series]:
    """Interpret the ridge regression model by finding feature importances.

    Interpret the ridge regression model by finding feature importances as the maximum absolute
    values of the weights.

    Todo:
        * Is it worth getting feature importances for each output in the mulitoutput cases? This
          would involve creating a feature importance bar chart for each output.

    Args:
        model: Ridge regression model.
        objective: Objective of the learning problem, from {"continuous", "continuous-multioutput"}.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Feature importances.
    """
    estimators = model.estimators_
    rrs = [estimators[i].named_steps["RidgeRegression"] for i in range(len(estimators))]

    # when multiple estimators, take absolute value of each estimator's weight matrix then mean over
    # the rows (since scikit-learn RidgeRegression uses X.W^T) to get an importance of each feature
    # for each estimator, then take the mean across all the estimators
    feature_importances = np.mean([np.abs(rr.coef_) for rr in rrs], axis=0)
    feature_importances *= 100 / feature_importances.sum()

    # Get the indices of the feature importance in descending order
    feature_importance_idxs = np.argsort(feature_importances)[::-1]
    feature_importances = pd.Series(
        feature_importances[feature_importance_idxs],
        index=model.feature_names_in_[feature_importance_idxs].astype(str),
        name="Relative importance / %",
    )
    feature_importances.index.name = "Feature"
    fig = px.bar(
        feature_importances,
        x=feature_importances.index,
        y="Relative importance / %",
        title="Feature importances",
    )
    fig.update_xaxes(tickangle=45)
    mlflow.log_figure(fig, "feature_importances.html")
    return {"feature_importances": feature_importances}
