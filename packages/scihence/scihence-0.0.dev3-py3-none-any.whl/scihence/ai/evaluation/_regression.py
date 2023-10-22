"""Classification machine learning model evaluation."""
from typing import Any

import matplotlib.pyplot as plt
import mlflow
import pandas as pd
import seaborn as sns
from plotly.figure_factory import create_table
from scipy.stats import pearsonr

from scihence.ai._io import DaitaFraime
from scihence.utils._math import set_sig_figs


def regression_model_evaluation(
    model: Any,
    X: DaitaFraime,
    Y: DaitaFraime,
    mlflow_logging: bool = False,
    build_plots: bool = True,
) -> dict[str, Any]:
    """Evaluate the regression model generically.

    Args:
        model: Regression model.
        X: Test input data.
        Y: Test target data.
        mlflow_logging: Whether to log outputs to MLflow. Defaults to :code:`False`.
        build_plots: Whether to build the plots, often set to false if there are too many outputs
            and in this case it will not display them, but will still calculate and return them.
            Defaults to :code:`True`.

    Returns:
        Information about the evaluation methods.
    """
    info = {}
    errors = (predictions := model.predict(X)) - Y

    info["error_histograms"] = build_error_histograms(
        errors, mlflow_logging, build_plots
    )
    info["bland_altman_correlations"] = build_bland_altman_plots(
        predictions, Y, errors, mlflow_logging, build_plots
    )
    info["target_prediction_correlations"] = build_target_prediction_scatters(
        predictions, Y, mlflow_logging, build_plots
    )
    return info


def build_error_histograms(
    errors: DaitaFraime, mlflow_logging: bool = False, build_plots: bool = True
) -> pd.DataFrame:
    """Build a plot of histograms of the error for each model output.

    Args:
        errors: Regression model errors.
        mlflow_logging: Whether to log outputs to MLflow. Defaults to :code:`False`.
        build_plots: Whether to build the plots, often set to false if there are too many outputs
            and in this case it will not display them, but will still calculate and return them.
            Defaults to :code:`True`.

    Returns:
        The means and standard deviations of each output's errors.
    """
    if build_plots:
        fig, axes = plt.subplots(1, 1, figsize=(10, 4), tight_layout=True)
        errors.plot.hist(histtype="step", lw=2, ax=axes)
        axes.set(
            title="Histogram of Prediction Errors",
            xlabel="Prediction error",
            ylabel="Number of examples",
        )
        if mlflow_logging:
            mlflow.log_figure(fig, "error-histograms.svg")
            plt.close()

    errors = DaitaFraime.concat(
        [errors.mean(axis=0), errors.std(axis=0).rename(columns={0: 1})],
        axis=1,
    )
    errors.columns = pd.Index(["Mean", "Standard deviation"], name="Aggregation")

    if mlflow_logging:
        table = create_table(errors._dataframe, index=True, index_title=errors.index.name)
        mlflow.log_figure(table, "error-aggregations.html")
    return errors


def build_bland_altman_plots(
    predictions: DaitaFraime,
    Y: DaitaFraime,
    errors: DaitaFraime,
    mlflow_logging: bool = False,
    build_plots: bool = True,
) -> pd.DataFrame:
    """Build scatter plots correlating the error with the targets/predictions.

    Args:
        predictions: Regression model predictions.
        Y: Regression model targets.
        errors: Regression model errors.
        mlflow_logging: Whether to log outputs to MLflow. Defaults to :code:`False`.
        build_plots: Whether to build the plots, often set to false if there are too many outputs
            and in this case it will not display them, but will still calculate and return them.
            Defaults to :code:`True`.

    Returns:
        The correlations of target vs error and prediction vs error and their p-values for each
        output.
    """
    info = pd.DataFrame(
        index=pd.MultiIndex.from_product(
            [["prediction", "target"], ["r", "p-value"]], names=["Label", "Statistic"]
        ),
        columns=pd.Index(errors.columns, name="Output"),
    )

    for output in errors:
        if build_plots:
            fig, axes = plt.subplots(1, 1, figsize=(10, 4), tight_layout=True)

        for x, label in zip((Y, predictions), ("Target", "Prediction")):
            corr = pearsonr(x[output].to_series(), errors[output].to_series())
            info[output][label.lower()]["r"] = corr.statistic
            info[output][label.lower()]["p-value"] = corr.pvalue

            if build_plots:
                plot_label = (
                    rf"{label}, $\it{{r}}$: {set_sig_figs(info[output][label.lower()]['r'], 3)}, "
                    f"p-value: {set_sig_figs(info[output][label.lower()]['p-value'], 3)}"
                )
                sns.regplot(
                    x=x[output], y=errors[output], ci=None, label=plot_label, ax=axes
                )
                if label == "Target":
                    sns.regplot(
                        x=x[output],
                        y=errors[output] * 0,
                        ci=None,
                        label=r"Perfect regressor, $\mathit{r}$: 0",
                        color=plt.rcParams["axes.labelcolor"],
                        scatter_kws={"alpha": 0.25},
                        line_kws={"alpha": 0.25},
                        ax=axes,
                    )
            for statistic in ["r", "p-value"]:
                mlflow.log_param(
                    f"{label} vs error correlation - {output} - {statistic}",
                    info[output][label.lower()][statistic],
                )

        if build_plots:
            axes.set(
                title=f"Bland-Altman plot: {output}",
                xlabel="Target or prediction",
                ylabel="Error = prediction - target",
            )
            axes.legend()
            if mlflow_logging:
                mlflow.log_figure(fig, f"bland-altman/{output}.svg")
                plt.close()
    return info


def build_target_prediction_scatters(
    predictions: DaitaFraime,
    Y: DaitaFraime,
    mlflow_logging: bool = False,
    build_plots: bool = True,
) -> pd.DataFrame:
    """Build scatter plots correlating the predictions with the targets.

    Args:
        predictions: Regression model predictions.
        Y: Regression model targets.
        mlflow_logging: Whether to log outputs to MLflow. Defaults to :code:`False`.
        build_plots: Whether to build the plots, often set to false if there are too many outputs
            and in this case it will not display them, but will still calculate and return them.
            Defaults to :code:`True`.

    Returns:
        The correlations between targets and predictions and their p-values for each output.
    """
    info: dict[str, Any] = {}
    for output in Y:
        if build_plots:
            fig, axes = plt.subplots(1, 1, figsize=(10, 4), tight_layout=True)

        info[output], corr = {}, pearsonr(Y[output].to_series(), predictions[output].to_series())
        info[output]["r"], info[output]["p-value"] = corr.statistic, corr.pvalue
        if build_plots:
            plot_label = (
                rf"Model, $\it{{r}}$: {set_sig_figs(info[output]['r'], 3)}, p-value: "
                f"{set_sig_figs(info[output]['p-value'], 3)}"
            )
            sns.regplot(
                x=Y[output], y=predictions[output], ci=None, label=plot_label, ax=axes
            )
            sns.regplot(
                x=Y[output],
                y=Y[output],
                ci=None,
                label=r"Perfect regressor, $\mathit{r}$: 1",
                color=plt.rcParams["axes.labelcolor"],
                scatter_kws={"alpha": 0.25},
                line_kws={"alpha": 0.25},
                ax=axes,
            )
            axes.set(
                title=f"Target vs prediction scatter: {output}",
                xlabel="Target",
                ylabel="Prediction",
            )
            axes.legend()
            if mlflow_logging:
                mlflow.log_figure(fig, f"target-prediction-scatter/{output}.svg")
                plt.close()

        if mlflow_logging:
            for statistic in ["r", "p-value"]:
                mlflow.log_param(
                    f"Target vs prediction correlation - {output} - {statistic}",
                    info[output][statistic],
                )

    return info
