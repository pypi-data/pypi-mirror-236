"""XGBoost model setup for supervised pipelines."""
from typing import Any

import mlflow
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier, XGBRegressor

from scihence.ai._io import DaitaFraime
from scihence.ai.models._utils import (
    ModelObjective,
    ScihenceClassifier,
    ScihenceRegressor,
    decode_classes_,
    encode_classes_,
    fit_classes_,
)


class ScihenceXGBClassifier(XGBClassifier):
    """Scihence's XGBoost classifier.

    Wraps the `xgboost.XGBClassifier <https://xgboost.readthedocs.io/en/stable/python/python_api.htm
    l#xgboost.XGBClassifier>`_ to ensure that it aligns with Scihence's pipeline API.
    """

    def __init__(self, **kwargs) -> None:
        """Construct an instance.

        Args:
            **kwargs: Keyword arguments for the `xgboost.XGBClassifier <https://xgboost.readthedocs.
                io/en/stable/python/python_api.html#xgboost.XGBClassifier>`_.
        """
        super().__init__(**kwargs)

    @fit_classes_
    @encode_classes_
    def fit(self, *args, **kwargs):
        return super().fit(*args, **kwargs)

    @decode_classes_(numpy=True)
    def predict(self, *args, **kwargs):
        return super().predict(*args, **kwargs)


def init_fit_xgboost(
    X: DaitaFraime,
    Y: DaitaFraime,
    objective: ModelObjective,
    hyperparam: dict[str, Any],
    fold: tuple[np.ndarray, np.ndarray],
    **kwargs,  # noqa: ARG001
) -> tuple[Pipeline, dict]:
    """Initialize and fit Scihence's XGBoost model.

    Args:
        X: Input data.
        Y: Target data.
        objective: Objective of the learning problem, from {"binary", "multiclass",
            "mulitlabel-indicator", "multiclass-multioutput", "continuous",
            "continuous-multioutput"}.
        hyperparam: Hyperparameter specification.
        fold: Fold specification of indices to use as train and test set.
        **kwargs: Additional keyword arguments.

    Raises:
        ValueError: If the objective is not a classification objective.

    Returns:
        Fitted XGBoost model, and a dictionary that will in future versions be populated with
        information about the fitting procedure.
    """
    class_kwargs = hyperparam.get("class_kwargs", {})
    if (classification := (objective in ModelObjective.filter("classification"))):
        xgboost = ScihenceXGBClassifier(**class_kwargs)
    elif objective in ModelObjective.filter("regression"):
        xgboost = XGBRegressor(**class_kwargs)
    else:
        raise ValueError(
            f"Unsupported objective: {objective}. Only supports objectives in {ModelObjective}."
        )
    preprocessor = hyperparam.get("preprocessor", StandardScaler(with_mean=False, with_std=False))
    model = Pipeline([("Preprocessor", preprocessor), ("XGBoost", xgboost)])
    model = (ScihenceClassifier if classification else ScihenceRegressor)(model)
    return model.fit(X.loc[fold[0]], Y.loc[fold[0]]), {}


def interpret_xgboost(model: Pipeline, *args, **kwargs) -> dict[str, pd.Series]:  # noqa: ARG001
    """Interpret the XGBClassifier model by finding feature importances.

    Interpret the XGBClassifier model by finding feature importances as the maximum absolute values
    of the weights.

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
    xgbs = [estimators[i].named_steps["XGBoost"] for i in range(len(estimators))]
    # when multiple estimators, take absolute value of each estimator's importances to get an
    # importance of each feature for each estimator, then take the mean across all the estimators
    feature_importances = np.mean([np.abs(xgb.feature_importances_) for xgb in xgbs], axis=0)
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
