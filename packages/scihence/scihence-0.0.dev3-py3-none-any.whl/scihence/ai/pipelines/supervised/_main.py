"""Main supervised pipeline module."""

import logging
from collections.abc import Callable
from typing import Any, Literal

import mlflow
import numpy as np
import pandas as pd
import torch
from sklearn.model_selection._split import _BaseKFold

from scihence.ai._io import DaitaFraime
from scihence.ai.evaluation._classification import classification_model_evaluation
from scihence.ai.evaluation._regression import regression_model_evaluation
from scihence.ai.evaluation._scoring_functions import get_scoring_function
from scihence.ai.experiment_tracking._mlflow import mlflow_log_nested_dict, set_mlflow_experiment
from scihence.ai.models._generic import init_fit_generic_model
from scihence.ai.models._sklearn_logistic_regression import (
    init_fit_sklearn_logistic_regression,
    interpret_sklearn_logistic_regression,
)
from scihence.ai.models._sklearn_ridge_regression import (
    init_fit_sklearn_ridge_regression,
    interpret_sklearn_ridge_regression,
)
from scihence.ai.models._utils import ModelObjective
from scihence.ai.models._xgboost import init_fit_xgboost, interpret_xgboost
from scihence.utils._dict import get_dict_without_keys
from scihence.utils._reproduce import set_random_seed

from ._check import check_supervised_pipeline_inputs
from ._split import supervised_train_valid_test_split

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

N_OUTPUT_MODERATION_LIMIT = 10


def supervised_pipeline(
    X: DaitaFraime,
    Y: DaitaFraime,
    objective: ModelObjective,
    valid: int | float | _BaseKFold = 0,
    test: int | float | pd.Index = 0,
    remove_train_groups_from_test_when_idxs: bool = False,
    instance_tags: DaitaFraime | None = None,
    feature_tags: pd.DataFrame | None = None,
    mlflow_kwargs: dict[str, str] = {},
    random_seed: int = 0,
    generic: dict[str, Any] = {},
    sklearn_logistic_regression: dict[str, Any] = {},
    sklearn_ridge_regression: dict[str, Any] = {},
    xgboost: dict[str, Any] = {},
) -> dict[str, Any]:
    r"""Supervised learning pipeline, for classification or regression.

    Args:
        X: Model input data.
        Y: Model target data.
        objective: Objective of the learning problem, from {"binary", "multiclass",
            "mulitlabel-indicator", "multiclass-multioutput", "continuous", "continuous-multioutput"
            }.
        valid: How to build the cross-validation set. Can be an integer to specify the number to use
            , can be a float to specify a proportion to use, or can be a `cross validation
            class that inherits from _BaseKFold <https://github.com/scikit-learn/scikit-learn/blob/9
            aaed498795f68e5956ea762fef9c440ca9eb239/sklearn/model_selection/_split.py#L285>`_.
            Defaults to :code:`0`.
        test: How to build the testing set. Can be an integer to specify the number to use, can be a
            float to specify a proportion to use, or can be a sequence of integers to specfy the
            indices of inputs to use as the test set. Defaults to :code:`0`.
        remove_train_groups_from_test_when_idxs: When specifying the test set by its specific
            indices, it may have some examples of training groups within the test set. By setting
            this to :code:`True`, the training groups (if specified by their numerical indices) will
            be removed from the test set. Defaults to :code:`False`.
        instance_tags: Tags associated with each instance. Defaults to :code:`None`.
        feature_tags: Tags associated with each feature. Defaults to :code:`None`.
        mlflow_kwargs: Dictionary of keyword arguments for the encompassing MLflow run of this
            pipeline. Should include an :code:`experiment_name` or :code:`experiment_id`, and then
            any other keyword arguments to `mlflow.start_run() <https://mlflow.org/docs/latest/pytho
            n_api/mlflow.html#mlflow.start_run>`_. If the experiment is not specified, it will send
            the run to whichever experiment
            :func:`scihence.ai.experiment_tracking.set_mlflow_experiment` would. Defaults to
            :code:`{}`.
        random_seed: The random seed to pass to the :func:`scihence.utils.set_random_seed` function.
            Defaults to :code:`0`.
        generic: Any generic model that conforms to specifications. PyTorch objects are built-in
            that allow for the convenient creation of these models.
        sklearn_logistic_regression: Scikit-learn logistic regression specification. The form of
            this dictionary is explained and outlined in
            :ref:`Specifying model arguments <ref-specifying-model-arguments>`, where the more
            specific parameters of the :code:`hyperparam` list should resemble:

                .. code-block:: python

                    "hyperparams"=[
                        {"preprocessor": ..., "class_kwargs": {...}, ...},
                        {"preprocessor": ..., "class_kwargs": {...}, ...},
                        ...,
                    ]

            using the keyword arguments:

                * :code:`preprocessor` (:code:`Any`): An instance to preprocess ML input data using
                  the same API as `scikit-learn preprocessing scaler classes <https://scikit-learn.o
                  rg/stable/modules/classes.html#module-sklearn.preprocessing>`_. Defaults to an
                  identity scaler.
                * :code:`class_kwargs` (:code:`dict[str, Any]`): Keyword arguments to be passed to
                  an `sklearn.linear_model.LogisticRegression() <https://scikit-learn.org/stable/mod
                  ules/generated/sklearn.linear_model.LogisticRegression.html>`_ class.

            Defaults to :code:`{}`.
        sklearn_ridge_regression: Scikit-learn ridge regression specification. The form of this
            dictionary is explained and outlined in
            :ref:`Specifying model arguments <ref-specifying-model-arguments>`, where the more
            specific parameters of the :code:`hyperparam` list should resemble:

                .. code-block:: python

                    "hyperparams"=[
                        {"preprocessor": ..., "class_kwargs": {...}, ...},
                        {"preprocessor": ..., "class_kwargs": {...}, ...},
                        ...,
                    ]

            using the keyword arguments:

                * :code:`preprocessor` (:code:`Any`): An instance to preprocess ML input data using
                  the same API as `scikit-learn preprocessing scaler classes <https://scikit-learn.o
                  rg/stable/modules/classes.html#module-sklearn.preprocessing>`_. Defaults to an
                  identity scaler.
                * :code:`class_kwargs` (:code:`dict[str, Any]`): Keyword arguments to be passed to
                  an `sklearn.linear_model.Ridge() <https://scikit-learn.org/stable/modules/generate
                  d/sklearn.linear_model.Ridge.html>`_ class.

            Defaults to :code:`{}`.
        xgboost: XGBoost specification. The form of this dictionary is explained and outlined in
            :ref:`Specifying model arguments <ref-specifying-model-arguments>`, where the more
            specific parameters of the :code:`hyperparam` list should resemble:

                .. code-block:: python

                    "hyperparams"=[
                        {"preprocessor": ..., "class_kwargs": {...}, ...},
                        {"preprocessor": ..., "class_kwargs": {...}, ...},
                        ...,
                    ]

            using the keyword arguments:

                * :code:`preprocessor` (:code:`Any`): An instance to preprocess ML input data using
                  the same API as `scikit-learn preprocessing scaler classes <https://scikit-learn.o
                  rg/stable/modules/classes.html#module-sklearn.preprocessing>`_. Defaults to an
                  identity scaler.
                * :code:`class_kwargs` (:code:`dict[str, Any]`): Keyword arguments to be passed to
                  an `xgboost.XGBModel() <https://github.com/dmlc/xgboost/blob/08ce495b5de973033160e
                  7c7b650abf59346a984/python-package/xgboost/sklearn.py#L616>`_ class.

            Defaults to :code:`{}`.

    Returns:
        Information about the pipeline run.

    .. _ref-specifying-model-arguments:

    .. admonition:: Specifying model arguments

        If a model argument (e.g. :code:`sklearn_logistic_regression`) is left as 'Falsy', e.g. its
        default, :code:`{}`, it will not be run. All models to be run should have their arguments
        specified using the structure:

            .. code-block:: python

                model_argument={
                    "hyperparams": [
                        {"final_model_use_hyperparam_search_epochs": ..., "n_inits": ..., ...},
                        {"final_model_use_hyperparam_search_epochs": ..., "n_inits": ..., ...},
                        ...,
                    ]
                    "build_final_model": ...,
                    "greater_score_better": ...,
                    "scoring_function": ...,
                }

        These have the following meanings:

            * :code:`hyperparams` (:code:`list[dict[str, Any]]`): List of dictionaries of
              hyperparameters. The specific form of these can be found above in the documentation
              for the model in question. Some general arguments to this can include:

                * :code:`final_model_use_hyperparam_search_epochs` (:code:`bool`): Whether the
                  number of epochs to train for should be calculated from the results of the
                  hyperparameter search. Currently implemented to take the median of the best epoch
                  from the best initialization of each fold. Note that this will only work for
                  PyTorch models. Defaults to :code:`False`.
                * :code:`n_inits` (:code:`int`): The number of different initialisations to use for
                  a mode training routine. The routine with the best score is carried forward.
                  Defaults to :code:`1`.

            * :code:`build_final_model` (:code:`bool`): Whether to build a final model using the
              best hyperparameter specification and the combined training and validation dataset.
              Defaults to :code:`True`.
            * :code:`greater_score_better` (:code:`bool`): Whether a greater `scoring_function` is
              better. This only needs to be declared if a custom (non-string) scoring function is
              specified. Defaults to :code:`None`.
            * :func:`scoring_function` (:code:`Callable[[Any, pd.DataFrame], pd.Series] | str`):
              Scoring function to use to compare different initialisations / folds /
              hyperparameters. Must have the same signature as the scoring functions in
              :mod:`scihence.ai.evaluation`, i.e. the :code:`model` is the first argument, :code:`X`
              is the second, and :code:`Y` is the third. If :code:`"auto"`, will choose will choose
              F1 score if a classification objective or will choose MAE if a regression objective.
              Defaults to :code:`"auto"`.

    .. admonition:: Pipeline flow of a single model.

        The following figures outline the flow of the pipeline. With respect to the scenarios in
        which the hyperparameter search and final model fitting are run for a model:

            * Validating and :math:`>` 1 hyperparameter: This is the most rigorous kind of pipeline
              run. It will search through all hyperparameters, choose the best and then fit a final
              model with the best hyperparameter.
            * Validating and 1 hyperparameter: The assumption here is that you may like to casually
              see the see how this 1 hyperparameter specification works, so the hyperparameter
              search is run and you can see the training and validation loss plots, etc. The final
              model will then be built using all the training and validation data.
            * Not validating and :math:`>` 1 hyperparameter: The hyperparameter search will be run
              and the best (according to the training score) one will be chosen. However, since
              there is no extra validation data to use to train a final model, the final model is
              taken to be the one output by the hyperparameter search.
            * Not validating and 1 hyperparameter: The hyperparameter search will not be run but the
              final model will be built. This is because training the single model specification in
              the search is equivalent to building one final model, as there is no extra information
              potentially coming from seeing a validation score or validation loss plot. Thus, we
              jump to building the final model.
            * The final model build will not be run in any of the scenarios above if
              :code:`build_final_model` if :code:`False`.

        .. csv-table:: Cases in which the (hyperparameter search | final model) is run.
            :header: "Validating", "1 hyperparameter", ":math:`>` 1 hyperparameter"
            :align: center
            :width: 100%

            False, "No | Yes", "Yes | No"
            True, "Yes | Yes", "Yes | Yes"

    Examples:
        stuff

    .. admonition:: Including new models

        If you are using a new type of model for which the pipeline does not already have an
        in-built plugin and the :code:`generic` argument is not sufficient for the purposes of the
        work that you are doing (perhaps you need some extra information about the explanatory power
        of the model or some example outputs), then you may add a new model plugin. The procedure
        for producing a new model plugin consists of the following steps:

        * Create a new, informative keyword argument as input to the
          :func:`scihence.ai.pipelines.supervised.supervised_pipeline` function.
        * Write an :func:`init_fit_model_func` (e.g.
          :func:`scihence.ai.models.init_fit_sklearn_logistic_regression`).
        * Write an :func:`interpret_model` function (e.g.
          :func:`scihence.ai.models.interpret_sklearn_logistic_regression`).
        * Include the code to run the new model through the
          :func:`scihence.ai.pipelines.supervised._main.supervised_single_model_pipeline` within
          :func:`scihence.ai.pipelines.supervised.supervised_pipeline`.
        * Write tests for the new model functionality.
        * Include this new argument in the docstring of
          :func:`scihence.ai.pipelines.supervised.supervised_pipeline`.

    Todo:
        * Python logging to the MLflow run.
        * Implement groups for features in scikit-learn model preprocessors.
        * Add support for saving models to the model registry.
        * Make scikit-learn models return information about fitting procedure within a
          :code:`fit_output`.
        * Sort issues that could occur in mlflow logging in all cases where there are a combination
          of too many labels and too many outputs
        * Maybe violinplots instead of the current confidence plots - maybe using a swarmplot too:
          `example <https://datavizpyr.com/how-to-make-violinpot-with-data-points-in-seaborn/>`_.
        * Make PR curves, ROC curves, and confidence plots plot even in the case that
          there are some example outputs in :code:`Y_test` that are not in the output space and vice
          versa.
        * Make groups works for multiple-instance tags in sequential inputs.
        * Dataclasses for pipeline results.
    """
    logger.info("Running supervised pipeline.")
    set_mlflow_experiment(
        experiment_name=mlflow_kwargs.get("experiment_name"),
        experiment_id=mlflow_kwargs.get("experiment_id"),
    )
    set_random_seed(random_seed)
    info = {"random_seed": random_seed, "objective": objective}

    logger.info("Checking data format.")
    check_supervised_pipeline_inputs(X, Y, objective, instance_tags, feature_tags)

    logger.info("Splitting data.")
    (
        X_train,
        X_test,
        Y_train,
        Y_test,
        instance_tags_train,
        instance_tags_test,
        info["index_train"],
        info["index_test"],
        info["folds"],
        info["validating"],
        info["testing"],
    ) = supervised_train_valid_test_split(
        X,
        Y,
        info["objective"],
        valid,
        test,
        remove_train_groups_from_test_when_idxs,
        instance_tags,
    )

    pipeline_kwargs = {
        "X_train": X_train,
        "Y_train": Y_train,
        "X_test": X_test,
        "Y_test": Y_test,
        "objective": objective,
        "folds": info["folds"],
        "validating": info["validating"],
        "testing": info["testing"],
        "instance_tags_train": instance_tags_train,
        "instance_tags_test": instance_tags_test,
        "feature_tags": feature_tags,
    }

    with mlflow.start_run(**get_dict_without_keys(mlflow_kwargs, ["experiment_name"]), nested=True):
        for k in ["objective", "random_seed", "testing", "validating"]:
            mlflow.log_param(k, info[k])

        if generic:
            with mlflow.start_run(run_name="Generic models", nested=True):
                logger.info("Generic models.")
                info["generic"] = single_model_pipeline(
                    init_fit_model_func=init_fit_generic_model,
                    interpret_model_func=None,
                    **(pipeline_kwargs | generic),
                )

        if sklearn_logistic_regression:
            with mlflow.start_run(run_name="Scikit-learn logistic regression", nested=True):
                logger.info("Scikit-learn logistic regression.")
                info["sklearn_logistic_regression"] = single_model_pipeline(
                    init_fit_model_func=init_fit_sklearn_logistic_regression,
                    interpret_model_func=interpret_sklearn_logistic_regression,
                    **(pipeline_kwargs | sklearn_logistic_regression),
                )

        if sklearn_ridge_regression:
            with mlflow.start_run(run_name="Scikit-learn ridge regression", nested=True):
                logger.info("Scikit-learn ridge regression.")
                info["sklearn_ridge_regression"] = single_model_pipeline(
                    init_fit_model_func=init_fit_sklearn_ridge_regression,
                    interpret_model_func=interpret_sklearn_ridge_regression,
                    **(pipeline_kwargs | sklearn_ridge_regression),
                )

        if xgboost:
            with mlflow.start_run(run_name="XGBoost", nested=True):
                logger.info("XGBoost.")
                info["xgboost"] = single_model_pipeline(
                    init_fit_model_func=init_fit_xgboost,
                    interpret_model_func=interpret_xgboost,
                    **(pipeline_kwargs | xgboost),
                )

    return info


def single_model_pipeline(
    X_train: DaitaFraime,
    Y_train: DaitaFraime,
    X_test: DaitaFraime,
    Y_test: DaitaFraime,
    objective: ModelObjective,
    folds: list[tuple[pd.Index, pd.Index]],
    hyperparams: list[dict],
    init_fit_model_func: Callable,
    scoring_function: Callable[[Any, pd.DataFrame], pd.Series] | str = "auto",
    greater_score_better: bool | None = None,
    validating: bool = False,
    testing: bool = False,
    instance_tags_train: DaitaFraime | None = None,
    instance_tags_test: DaitaFraime | None = None,
    feature_tags: pd.DataFrame | None = None,
    build_final_model: bool = True,
    interpret_model_func: Callable | None = None,
) -> dict[str, Any]:
    """Supervised learning pipeline for a single model.

    Args:
        X_train: Model training input data.
        Y_train: Model training target data.
        X_test: Model testing input data.
        Y_test: Model testing target data.
        objective: Objective of the learning problem, from {"binary", "multiclass",
            "mulitlabel-indicator", "multiclass-multioutput", "continuous", "continuous-multioutput"
            }.
        folds: Fold specification of indices to use as training and testing sets, where each element
            in the list is a different fold defined as a tuple with the first element a numpy array
            of the indices in the training set, and the second element a numpy array of the indices
            in the tesing set.
        hyperparams: All hyperparameter specifications.
        init_fit_model_func: Function to initialise and fit a model.
        scoring_function: The inputted scoring function, as a string or function. If specified as
            "auto", will choose F1 if a classification objective or will choose MAE if a regression
            objective. If specified as a string, can be any of {"accuracy", "f1", "mae", "mape",
            "mse"} (will automatically be converted to lower case). If a function, the callable must
            have signature :code:`(model, X, Y, *args, **kwargs)`. Defaults to :code:`"auto"`.
        greater_score_better: Whether a greater score is better. Only required if
            :func:`scoring_function` is not specified as a string. Defualts to :code:`None`.
        validating: Whether a validation set exists. Defaults to :code:`False`.
        testing: Whether a test set exists. Defaults to :code:`False`.
        instance_tags_train: Tags associated with each training instance. When :code:`X` is
            sequential, this only counts as one instance (for now). Defaults to :code:`None`.
        instance_tags_test: Tags associated with each testing instance. When :code:`X` is sequential
            , this only counts as one instance (for now). Defaults to :code:`None`.
        feature_tags: Tags associated with each feature. Defaults to :code:`None`.
        build_final_model: Whether to build the final model on all training and validation data,
            however will still only build it if validating or :code:`len(hyperparams) == 1`.
            Defaults to :code:`True`.
        interpret_model_func: Function to do interpretation of the model. Defaults to :code:`None`.

    Returns:
        Information about the pipeline run.
    """
    scoring_function, new_score_better = get_scoring_function(
        scoring_function, greater_score_better, objective
    )
    info = {
        "scoring_data": "valid" if validating else "train", "scoring_function": scoring_function
    }

    if (n_hyperparams := len(hyperparams)) > 1 or validating:
        info[f"{info['scoring_data']}_score"] = np.inf * (
            1 - 2 * new_score_better(new=np.inf, old=-np.inf)
        )
        info["hyperparams"] = {}

        for idx, hyperparam in enumerate(hyperparams):
            logger.info(f"Hyperparameter: {idx}.")
            with mlflow.start_run(run_name=f"Hyperparameter: {idx}", nested=True):
                info["hyperparams"][idx] = single_hyperparam_pipeline(
                    X=X_train,
                    Y=Y_train,
                    objective=objective,
                    folds=folds,
                    hyperparam=get_dict_without_keys(
                        hyperparam, ["final_model_use_hyperparam_search_epochs"]
                    ),
                    init_fit_model_func=init_fit_model_func,
                    scoring_function=scoring_function,
                    scoring_data=info["scoring_data"],
                    new_score_better=new_score_better,
                    instance_tags=instance_tags_train,
                    feature_tags=feature_tags,
                )
            if new_score_better(
                new=info["hyperparams"][idx][f"{info['scoring_data']}_score"],
                old=info[f"{info['scoring_data']}_score"],
            ):
                info["best_hyperparam"] = idx
                info["model"] = info["hyperparams"][idx]["model"]
                info["train_score"] = info["hyperparams"][idx]["train_score"]
                if validating:
                    info["valid_score"] = info["hyperparams"][idx]["valid_score"]

            # delete the best model by that hyperparameter so store many models unnecessarily
            del info["hyperparams"][idx]["model"]

        mlflow_params_to_log = ["train_score", "scoring_function", "scoring_data"]
        mlflow_params_to_log += ["valid_score"] if validating else []
        for param in mlflow_params_to_log:
            mlflow.log_param(param, info[param])
    else:
        info["best_hyperparam"] = 0

    mlflow.log_param("best_hyperparam", best_hyperparam := info["best_hyperparam"])

    if (n_hyperparams == 1 or validating) and build_final_model:
        logger.info("Building model with best hyperparameters on training and validation data.")
        with mlflow.start_run(run_name="Final model", nested=True):
            hyperparam = get_best_final_hyperparam(hyperparams, info, best_hyperparam)
            info["final_model_build"] = single_fold_pipeline(
                X=X_train,
                Y=Y_train,
                objective=objective,
                hyperparam=get_dict_without_keys(
                    hyperparam, ["final_model_use_hyperparam_search_epochs"]
                ),
                init_fit_model_func=init_fit_model_func,
                scoring_function=scoring_function,
                scoring_data="train",
                new_score_better=new_score_better,
                fold=None,
                instance_tags=instance_tags_train,
                feature_tags=feature_tags,
            )
            info["model"] = info["final_model_build"].pop("model")
            mlflow_log_nested_dict(hyperparam)

    if testing:
        logger.info("Evaluating final model on test set.")
        info["test_score"] = scoring_function(info["model"], X_test, Y_test)

        # if there are too many outputs, average them - otherwise higher chance of too many
        # parameters for mlflow
        if (Y_test.n_fields == 1) or (Y_test.n_fields > N_OUTPUT_MODERATION_LIMIT):
            mlflow.log_param("test_score", info["test_score"].mean())
        else:
            for output, score in info["test_score"].to_series().items():
                mlflow.log_param(f"test_score - {output}", score)

        if objective in ModelObjective.filter("classification"):
            info["evaluation"] = classification_model_evaluation(
                model=info["model"],
                X=X_test,
                Y=Y_test,
                mlflow_logging=True,
                build_plots=Y_test.n_fields <= N_OUTPUT_MODERATION_LIMIT,
            )
        elif objective in ModelObjective.filter("regression"):
            info["evaluation"] = regression_model_evaluation(
                model=info["model"],
                X=X_test,
                Y=Y_test,
                mlflow_logging=True,
                build_plots=Y_test.n_fields <= N_OUTPUT_MODERATION_LIMIT,
            )

    if interpret_model_func is not None:
        logger.info("Interpreting final model.")
        info["interpretation"] = interpret_model_func(
            model=info["model"],
            X_train=X_train,
            Y_train=Y_train,
            X_test=X_test,
            Y_test=Y_test,
            objective=objective,
            instance_tags_train=instance_tags_train,
            instance_tags_test=instance_tags_test,
            feature_tags=feature_tags,
        )
    return info


def get_best_final_hyperparam(
    hyperparams: dict[str, Any], info: dict[str, Any], best_hyperparam: int
) -> dict[str, Any]:
    """Construct the best hyperparameter for the final model build.

    Args:
        hyperparams: All hyperparameter specifications.
        info: Information about the model pipeline.
        best_hyperparam: Best hyperparemeter index.

    Raises:
        ValueError: If using the number of epochs from the hyperparemeter search but the search was
            not executed.

    Returns:
        Hyperparameter for the final model build.
    """
    hyperparam = hyperparams[best_hyperparam]
    if use_hyperparam_search_epochs := hyperparam.get(
        "final_model_use_hyperparam_search_epochs"
    ):
        if "hyperparams" not in info:
            raise ValueError(
                "It has been specified that the number of epochs to be used should be the number "
                "found from the hyperparameter search, however the hyperparameter search was not "
                "executed. Set the number of hyperparemeters to be > 1 or include a validation set "
                "to run the hyperparameter search."
            )
        # no stopping criteria or will stop based on training loss, not based on best number of
        # epochs found from before based on validation loss
        hyperparam["fit_kwargs"]["stop_criteria"] = None
        # save_best_model needs to be False or will save one with lowest (not necessarily last)
        # training loss
        hyperparam["fit_kwargs"]["save_best_model"] = False
        hyperparam["fit_kwargs"]["max_epochs"] = get_agg_epochs_for_hyperparam(
            info["hyperparams"][best_hyperparam]
        )
    mlflow.log_param("use_hyperparam_search_epochs", use_hyperparam_search_epochs)
    return hyperparam


def get_agg_epochs_for_hyperparam(hyperparam_fit_dict: dict) -> int:
    """Get an aggregation of the number of epochs used when training a hyperparameter.

    Aggregates if multiple initialisations and folds were used. Computes the median of the epochs
    used for the model resulting from the best initialisation for each fold. It will use the
    :code:`best_epoch` from each fitting procedure if :code:`log_loss` was :code:`True` (i.e. it
    tracked the losses during training), or just :code:`epochs` (i.e. the final number of epochs
    trained for) if not.

    Args:
        hyperparam_fit_dict: Hyperparameter dictionary.

    Returns:
        An aggregation of the number of epochs used for a hyperparameter.
    """
    epochs_for_folds = []
    for fold in hyperparam_fit_dict["folds"].values():
        fit_output = fold["inits"][fold["best_init"]]["fit_output"]
        epochs_for_fold = fit_output.get("best_epoch") or fit_output.get("epochs")
        epochs_for_folds.append(epochs_for_fold)
    return int(np.median(epochs_for_folds))


def single_hyperparam_pipeline(
    X: DaitaFraime,
    Y: DaitaFraime,
    objective: ModelObjective,
    folds: list[tuple[np.ndarray, np.ndarray]],
    hyperparam: dict[str, Any],
    init_fit_model_func: Callable,
    scoring_function: Callable[[Any, pd.DataFrame], pd.Series],
    scoring_data: Literal["train", "valid"],
    new_score_better: Callable[[float, float], bool],
    instance_tags: DaitaFraime | None = None,
    feature_tags: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """Supervised learning pipeline for a single hyperparameter.

    Args:
        X: Model input data.
        Y: Model target data.
        objective: Objective of the learning problem, from {"binary", "multiclass",
            "mulitlabel-indicator", "multiclass-multioutput", "continuous", "continuous-multioutput"
            }.
        folds: Fold specification of indices to use as training and testing sets, where each element
            in the list is a different fold defined as a tuple with the first element a numpy array
            of the indices in the training set, and the second element a numpy array of the indices
            in the tesing set.
        hyperparam: Hyperparameter specification.
        init_fit_model_func: Function to initialise and fit a model.
        scoring_function: Scoring function, the callable must have signature `(model, X, Y, *args,
            **kwargs)`.
        scoring_data: The data to use for scoring data. Should be :code:`"valid"` if validating, and
            :code:`"train"` if not.
        new_score_better: Function to take in a new score, and compare it to a current best to
            determine which is better.
        instance_tags: Tags associated with each instance. Defaults to :code:`None`.
        feature_tags: Tags associated with each feature. Defaults to :code:`None`.

    Returns:
        Information about the pipeline run.
    """
    info = {
        "train_score": 0,
        "best_fold_score": np.inf * (1 - 2 * new_score_better(new=np.inf, old=-np.inf)),
        "folds": {},
    }
    if scoring_data == "valid":
        info["valid_score"] = 0

    for idx, fold in enumerate(folds):
        logger.info(f"Fold: {idx}.")
        with mlflow.start_run(run_name=f"Fold: {idx}", nested=True):
            info["folds"][idx] = single_fold_pipeline(
                X=X,
                Y=Y,
                objective=objective,
                hyperparam=hyperparam,
                init_fit_model_func=init_fit_model_func,
                scoring_function=scoring_function,
                scoring_data=scoring_data,
                new_score_better=new_score_better,
                fold=fold,
                instance_tags=instance_tags,
                feature_tags=feature_tags,
            )
        if new_score_better(
            new=info["folds"][idx][f"{scoring_data}_score"], old=info["best_fold_score"]
        ):
            info["best_fold"] = idx
            info["best_fold_score"] = info["folds"][idx][f"{scoring_data}_score"]
            info["model"] = info["folds"][idx]["model"]

        # delete the best model by that fold as we do not want to store many models unnecessarily
        del info["folds"][idx]["model"]

        info["train_score"] += info["folds"][idx]["train_score"]
        if scoring_data == "valid":
            info["valid_score"] += info["folds"][idx]["valid_score"]

    info["train_score"] /= len(folds)
    if scoring_data == "valid":
        info["valid_score"] /= len(folds)

    mlflow_params_to_log = ["best_fold", "best_fold_score", "train_score"]
    mlflow_params_to_log += ["valid_score"] if scoring_data == "valid" else []
    for param in mlflow_params_to_log:
        mlflow.log_param(param, info[param])
    mlflow_log_nested_dict(hyperparam)
    return info


def single_fold_pipeline(
    X: DaitaFraime,
    Y: DaitaFraime,
    objective: ModelObjective,
    hyperparam: dict[str, Any],
    init_fit_model_func: Callable,
    scoring_function: Callable[[Any, pd.DataFrame], pd.Series],
    scoring_data: Literal["train", "valid"],
    new_score_better: Callable[[float, float], bool],
    fold: tuple[np.ndarray, np.ndarray] | None,
    instance_tags: DaitaFraime | None = None,
    feature_tags: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """Supervised learning pipeline for a single fold.

    Args:
        X: Model input data.
        Y: Model target data.
        objective: Objective of the learning problem, from {"binary", "multiclass",
            "mulitlabel-indicator", "multiclass-multioutput", "continuous", "continuous-multioutput"
            }.
        hyperparam: Hyperparameter specification.
        init_fit_model_func: Function to initialise and fit a model.
        scoring_function: Scoring function, the callable must have signature `(model, X, Y, *args,
            **kwargs)`.
        scoring_data: The data to use for scoring data. Should be :code:`"valid"` if validating, and
            :code:`"train"` if not.
        new_score_better: Function to take in a new score, and compare it to a current best to
            determine which is better.
        fold: Fold specification of indices to use as train and test set. If None, uses all data as
            the training set.
        instance_tags: Tags associated with each instance. Defaults to :code:`None`.
        feature_tags: Tags associated with each feature. Defaults to :code:`None`.

    Returns:
        Information about the pipeline run.
    """
    if fold is None:
        index_train = Y.index.get_level_values(0).unique()
        fold = (index_train, index_train[:0])
    # set initial score to -np.inf if greater score is better or np.inf if lesser score is better
    info = {
        f"{scoring_data}_score": np.inf * (1 - 2 * new_score_better(new=np.inf, old=-np.inf)),
        "inits": {},
    }

    for idx in range(hyperparam.get("n_inits", 1)):
        logger.info(f"Initialization: {idx}.")
        with mlflow.start_run(run_name=f"Initialization: {idx}", nested=True):
            info["inits"][idx] = single_init_pipeline(
                X=X,
                Y=Y,
                objective=objective,
                hyperparam=get_dict_without_keys(hyperparam, ["n_inits"]),
                init_fit_model_func=init_fit_model_func,
                scoring_function=scoring_function,
                scoring_data=scoring_data,
                fold=fold,
                instance_tags=instance_tags,
                feature_tags=feature_tags,
            )
        # update the best scores
        if new_score_better(
            new=info["inits"][idx][f"{scoring_data}_score"], old=info[f"{scoring_data}_score"]
        ):
            info["best_init"] = idx
            info["model"] = info["inits"][idx]["model"]
            info["train_score"] = info["inits"][idx]["train_score"]
            if scoring_data == "valid":
                info["valid_score"] = info["inits"][idx]["valid_score"]

        # do not save the model from the initialization unless it was the best so far
        del info["inits"][idx]["model"]

    mlflow_params_to_log = ["best_init", "train_score"]
    mlflow_params_to_log += ["valid_score"] if scoring_data == "valid" else []
    for param in mlflow_params_to_log:
        mlflow.log_param(param, info[param])
    return info


def single_init_pipeline(
    X: DaitaFraime,
    Y: DaitaFraime,
    objective: ModelObjective,
    hyperparam: dict[str, Any],
    init_fit_model_func: Callable,
    scoring_function: Callable[[Any, pd.DataFrame], pd.Series],
    scoring_data: Literal["train", "valid"],
    fold: tuple[np.ndarray, np.ndarray],
    instance_tags: DaitaFraime | None = None,
    feature_tags: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """Supervised pipeline for a single model intialization.

    Args:
        X: Model input data.
        Y: Model target data.
        objective: Objective of the learning problem, from {"binary", "multiclass",
            "mulitlabel-indicator", "multiclass-multioutput", "continuous", "continuous-multioutput"
            }.
        hyperparam: Hyperparameter specification.
        init_fit_model_func: Function to initialise and fit a model.
        scoring_function: Scoring function, the callable must have signature `(model, X, Y, *args,
            **kwargs)`.
        scoring_data: The data to use for scoring data. Should be `"valid"` if validating, and
            `"train"` if not.
        fold: Fold specification of indices to use as train and test set.
        instance_tags: Tags associated with each instance. Defaults to :code:`None`.
        feature_tags: Tags associated with each feature. Defaults to :code:`None`.

    Returns:
        Information about the pipeline run.
    """
    info = {}
    info["model"], info["fit_output"] = init_fit_model_func(
        X=X,
        Y=Y,
        objective=objective,
        hyperparam=hyperparam,
        fold=fold,
        instance_tags=instance_tags,
        feature_tags=feature_tags,
    )
    # if the model.fit function output is a dictionary, then it is storing extra information about
    # the fitting process so keep it. If not then it may contain a copy of the modelc(since this is
    # what is returned by scikit-learn fitters).
    info["fit_output"] = info["fit_output"] if isinstance(info["fit_output"], dict) else {}

    # calculate scores
    with torch.no_grad():
        for i, data_name in enumerate(["train", "valid"]):
            info[f"{data_name}_score"] = scoring_function(
                info["model"], X.loc[fold[i]], Y.loc[fold[i]]
            ).mean().squeeze()
            mlflow.log_param(f"{data_name}_score", info[f"{data_name}_score"])
            if scoring_data == "train":
                break
    return info
