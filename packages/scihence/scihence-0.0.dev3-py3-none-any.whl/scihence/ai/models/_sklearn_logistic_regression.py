"""Scikit-learn logistic regression model objects for supervised pipelines."""
from typing import Any

import mlflow
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from scihence.ai._io import DaitaFraime
from scihence.ai.models._utils import ScihenceClassifier


def init_fit_sklearn_logistic_regression(
    X: DaitaFraime,
    Y: DaitaFraime,
    hyperparam: dict[str, Any],
    fold: tuple[np.ndarray, np.ndarray],
    **kwargs,  # noqa: ARG001
) -> tuple[LogisticRegression | MultiOutputClassifier, dict]:
    """Initialize and fit a scikit-learn logistic regression model.

    Args:
        X: Input data.
        Y: Target data.
        objective: Objective of the learning problem, from {"binary", "multiclass",
            "mulitlabel-indicator", "multiclass-multioutput"}.
        hyperparam: Hyperparameter specification.
        fold: Fold specification of indices to use as train and test set.
        **kwargs: Additional keyword arguments.

    Raises:
        ValueError: If the objective is not a classification objective.

    Returns:
        Fitted logistic regression model, and a dictionary that will in future versions be populated
        with information about the fitting procedure.
    """
    lr = LogisticRegression(**hyperparam.get("class_kwargs", {}))
    preprocessor = hyperparam.get("preprocessor", StandardScaler(with_mean=False, with_std=False))
    model = Pipeline([("Preprocessor", preprocessor), ("LogisticRegression", lr)])
    model = ScihenceClassifier(model)
    return model.fit(X.loc[fold[0]], Y.loc[fold[0]]), {}


def interpret_sklearn_logistic_regression(
    model: Pipeline, *args, **kwargs  # noqa: ARG001
) -> dict[str, pd.Series]:
    """Interpret the logistic regression model by finding feature importances.

    Interpret the logistic regression model by finding feature importances as the maximum absolute
    values of the weights.

    Todo:
        * Is it worth getting feature importances for each output in the mulitoutput cases? This
          would involve creating a feature importance bar chart for each output.

    Args:
        model: Logistic regression model.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Feature importances.
    """
    estimators = model.estimators_
    lrs = [estimators[i].named_steps["LogisticRegression"] for i in range(len(estimators))]
    # when multiple estimators, take absolute value of each estimator's weight matrix then mean over
    # the rows (since scikit-learn LogisticRegression uses X.W^T) to get an importance of each
    # feature for each estimator, then take the mean across all the estimators
    feature_importances = np.mean([np.abs(lr.coef_).mean(axis=0) for lr in lrs], axis=0)
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
