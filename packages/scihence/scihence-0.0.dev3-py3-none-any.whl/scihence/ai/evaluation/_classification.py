"""Classification machine learning model evaluation."""

import logging
from typing import Any

import matplotlib.pyplot as plt
import mlflow
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import MaxNLocator
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    PrecisionRecallDisplay,
    RocCurveDisplay,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)

import scihence.visualize as vis
from scihence.ai._io import DaitaFraime
from scihence.ai.models._utils import set_missing_classes_to_0_prob
from scihence.utils._math import robust_divide

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def classification_model_evaluation(
    model: Any,
    X: DaitaFraime,
    Y: DaitaFraime,
    mlflow_logging: bool = False,
    build_plots: bool = True,
) -> dict[str, Any]:
    """Evaluate the classification model generically.

    Todo:
        * Return variation of confidences for each output and each class.

    Args:
        model: Classification model.
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
    info["confusion-matrices"], info["metrics"] = build_confusion_matrices(
        model.predict(X), Y, mlflow_logging, build_plots
    )
    if not hasattr(model, "predict_proba"):
        return info

    confidences = model.predict_proba(X)

    info["avg-precision"] = build_precision_recall_curves(
        confidences, Y, mlflow_logging, build_plots
    )
    info["roc-auc"] = build_roc_curves(confidences, Y, mlflow_logging, build_plots)

    if build_plots:
        build_confidence_plots(confidences, Y, mlflow_logging)
    return info


def build_confusion_matrices(
    predictions: DaitaFraime,
    Y: DaitaFraime,
    mlflow_logging: bool = False,
    build_plots: bool = True,
) -> tuple[dict[str, pd.DataFrame], dict[str, dict]]:
    """Build confusion matrices and calculate metrics.

    Build a confusion matrix for each output of the classification model (for example there will be
    one output in the event of a multiclass objective). Also calculate some common metrics that
    relate to the confusion matrix, e.g. F1 score.

    Args:
        predictions: Predictions from the classification model.
        Y: Targets.
        mlflow_logging: Whether to log outputs to MLflow. Defaults to :code:`False`.
        build_plots: Whether to build the plots, often set to false if there are too many outputs
            and in this case it will not display them, but will still calculate and return them as a
            DataFrame. Defaults to :code:`True`.

    Returns:
        The confusion matrices, and the evaluation metrics.
    """
    cm, metrics = {}, {}
    for output_name in Y:
        cm[output_name], metrics[output_name] = build_confusion_matrix(
            predictions=predictions[output_name],
            labels=Y[output_name],
            output_name=output_name,
            mlflow_logging=mlflow_logging,
            build_plot=build_plots,
        )
    return cm, metrics


def build_confusion_matrix(
    predictions: pd.Series,
    labels: pd.Series,
    output_name: str,
    mlflow_logging: bool = False,
    build_plot: bool = False,
) -> tuple[pd.DataFrame, dict]:
    """Build a confusion matrix for an output of the classification model.

    Args:
        predictions: Predictions of a classification model for an output.
        labels: Targets for an output.
        output_name: The name of the output.
        mlflow_logging: Whether to log outputs to MLflow. Defaults to :code:`False`.
        build_plot: Whether to build the plots, often set to false if there are too many outputs
            and in this case it will not display them, but will still calculate and return them as a
            DataFrame. Defaults to :code:`False`.

    Returns:
        The confusion matrix as a DataFrame, and the dictionary of metrics, including that for each
        class and some averages.
    """
    cm = confusion_matrix(labels, predictions)
    metrics = {
        "accuracy": {},
        "f1": {},
        "npv": {},
        "ppv": {},
        "sensitivity": {},
        "specificity": {},
    }

    # list all the possible output labels, here produced from a set union as there could be cases
    # where the labels have examples that the predicions do not and vice versa (if for example the
    # test set did not contain some rare output labels that were seen during training)
    all_labels = np.unique(list(set(labels.values.flatten()) | set(predictions.values.flatten())))

    # number of false positives, false negatives, true positives and true negatives for each class
    FP = (cm.sum(axis=0) - np.diag(cm)).astype(int)
    FN = (cm.sum(axis=1) - np.diag(cm)).astype(int)
    TP = np.diag(cm).astype(int)
    TN = (cm.sum() - (FP + FN + TP)).astype(int)

    # Sensitivity, hit rate, recall, or true positive rate
    TPR = robust_divide(TP, TPFN := TP + FN)
    # Specificity or true negative rate
    TNR = robust_divide(TN, TNFP := TN + FP)
    # Precision or positive predictive value
    PPV = robust_divide(TP, TP + FP)
    # Negative predictive value
    NPV = robust_divide(TN, TN + FN)
    # Overall accuracy for each class
    ACC = robust_divide(TP + TN, TPFN + TNFP)
    # F1 score
    metrics["f1"]["micro-average"] = f1_score(labels, predictions, average="micro")
    metrics["f1"]["macro-average"] = f1_score(labels, predictions, average=None)

    # for each class
    for class_num, label in enumerate(all_labels):
        metrics["f1"][label] = metrics["f1"]["macro-average"][class_num]
        metrics["accuracy"][label] = ACC[class_num]
        metrics["sensitivity"][label] = TPR[class_num]
        metrics["specificity"][label] = TNR[class_num]
        metrics["ppv"][label] = PPV[class_num]
        metrics["npv"][label] = NPV[class_num]
    # averages across all classes
    metrics["f1"]["macro-average"] = np.mean(metrics["f1"]["macro-average"])
    metrics["accuracy"]["macro-average"] = np.mean(ACC)
    metrics["sensitivity"]["macro-average"] = np.mean(TPR)
    metrics["specificity"]["macro-average"] = np.mean(TNR)
    metrics["ppv"]["macro-average"] = np.mean(PPV)
    metrics["npv"]["macro-average"] = np.mean(NPV)

    cm = ConfusionMatrixDisplay(cm, display_labels=all_labels)

    # if we are building plot, then can display and log all the confusion matrices
    if build_plot:
        fig, axes = plt.subplots(1, 1, figsize=(6, 6), tight_layout=True)
        cm.plot(ax=axes, cmap=vis.get_cmap())
        axes.set_title(f"Confusion matrix: {output_name}")
        axes.grid(False)
        axes.set_xticklabels(labels=axes.get_xticklabels(), ha="right", rotation=45)
        axes.set_yticklabels(labels=axes.get_yticklabels(), ha="right", rotation=45)

        if mlflow_logging:
            mlflow.log_figure(fig, f"confusion-matrix/{output_name}.svg")
            plt.close()

    # in all cases, can still return the confusion matrices as a DataFrame into the info dictionary
    cm = pd.DataFrame(
        data=cm.confusion_matrix,
        index=pd.Index(cm.display_labels, name="True"),
        columns=pd.Index(cm.display_labels, name="Predicted"),
    )
    return cm, metrics


def build_precision_recall_curves(
    confidences: DaitaFraime,
    Y: DaitaFraime,
    mlflow_logging: bool = False,
    build_plots: bool = True,
) -> dict[str, Any]:
    r"""Build precision recall curves and get average precision scores.

    Build precision recall curves for each output and additionally get the average precision scores.
    In the case of multioutput objectives, it requires that each output should have output space the
    same as every other.

    Args:
        confidences: DaitaFraime of confidences of shape
            :math:`n_{\text{instances}} \times (n_{\text{outputs}} \times n_{\text{classes}})`.
        Y: Targets.
        mlflow_logging: Whether to log outputs to MLflow. Defaults to :code:`False`.
        build_plots: Whether to build the plots, often set to false if there are too many outputs
            and in this case it will not display them, but will still calculate and return them as a
            DataFrame. Defaults to :code:`False`.

    Returns:
        Average precision scores for each output and each class.
    """
    # generate the iso-F1 lines
    iso_f1s = {}
    for f1 in [0.2, 0.4, 0.6, 0.8]:
        x_iso_f1 = np.linspace(0.11, 1, 100)
        y_iso_f1 = f1 * x_iso_f1 / (2 * x_iso_f1 - f1)
        # only keep the x and y points for where y is positive (do not want to plot below the axis)
        x_iso_f1, y_iso_f1 = x_iso_f1[y_iso_f1 >= 0], y_iso_f1[y_iso_f1 >= 0]
        iso_f1s[f1] = (x_iso_f1, y_iso_f1)

    avg_precision = {}
    for output_name in Y:
        confidence, one_hot_encoded_y = get_confidences_and_one_hot_encoded_y_for_all_classes(
            confidences[output_name], Y[output_name]
        )
        avg_precision[output_name] = build_precision_recall_curve(
            confidence,
            one_hot_encoded_y,
            iso_f1s=iso_f1s,
            output_name=output_name,
            build_plot=build_plots,
            mlflow_logging=mlflow_logging,
        )
    return avg_precision


def build_precision_recall_curve(
    confidences: DaitaFraime,
    labels: pd.DataFrame,
    iso_f1s: dict[float, tuple[np.ndarray, np.ndarray]],
    output_name: str,
    build_plot: bool = True,
    mlflow_logging: bool = False,
) -> dict[str, Any]:
    """Build a precision recall curve for a particular output.

    Args:
        confidences: Confidences for the output as a DaitaFraime with each row an example and each
            column the probability of being that example.
        labels: True output labels as a one-hot encoded DaitaFraime.
        iso_f1s: Iso-F1 curves.
        output_name: The name of the output.
        mlflow_logging: Whether to log outputs to MLflow. Defaults to :code:`False`.
        build_plot: Whether to build the plots, often set to false if there are too many outputs
            and in this case it will not display them, but will still calculate and return them as a
            DataFrame. Defaults to :code:`False`.

    Returns:
        Average precision scores, including macro and micro.
    """
    if build_plot:
        fig, axes = plt.subplots(1, 1, figsize=(6, 6), tight_layout=True)
        for f1, curve in iso_f1s.items():
            axes.plot(*curve, color=plt.rcParams["axes.labelcolor"], alpha=0.2)
            axes.annotate(
                rf"$F_1$={f1:0.1f}",
                xy=(1, curve[1][-1] - 0.01),
                size=10,
                color=plt.rcParams["axes.labelcolor"],
                alpha=0.5,
            )

        axes.set_title(f"Precision-recall curve: {output_name}")
        axes.set_xlim([-0.01, 1.01])
        axes.set_ylim([-0.01, 1.01])
        cmap = vis.get_cmap(N=(n_classes := labels.shape[1]))
        area = 1 / n_classes
        axes.plot(
            [0, 1],
            [area, area],
            linestyle="dotted",
            color=plt.rcParams["axes.labelcolor"],
            alpha=0.25,
            label=f"Random classifier (AP = {area:.2f})",
        )

    avg_precision, recalls, precisions, thresholds = {}, [], [], np.linspace(0, 1)
    # first calculate metrics and plot curves for each class
    for i, class_name in enumerate(labels):
        # get the curve and precision score for this class
        precision, recall, threshold = precision_recall_curve(
            labels[class_name], confidences[class_name]
        )
        avg_precision[class_name] = average_precision_score(
            labels[class_name], confidences[class_name]
        )
        # plot the curve for each class
        if build_plot:
            PrecisionRecallDisplay(
                precision,
                recall,
                average_precision=avg_precision[class_name],
                estimator_name=class_name,
            ).plot(ax=axes, color=cmap(i))
        # standardize the curves to all the same length with all the same thresholds so
        # that a macro-average can be calculated later
        precisions.append(np.interp(thresholds, threshold, precision[:-1]))
        recalls.append(np.interp(thresholds, threshold, recall[:-1]))

    avg_precision["macro-average"] = average_precision_score(labels, confidences)
    labels, confidences = labels.values.flatten(), confidences.values.flatten()
    micro_precision, micro_recall, _ = precision_recall_curve(labels, confidences)
    avg_precision["micro-average"] = average_precision_score(labels, confidences)

    if build_plot:
        PrecisionRecallDisplay(
            np.mean(precisions, axis=0),
            np.mean(recalls, axis=0),
            average_precision=avg_precision["macro-average"],
            estimator_name="Macro-average",
        ).plot(linestyle="--", ax=axes, color=cmap(0))
        PrecisionRecallDisplay(
            micro_precision,
            micro_recall,
            average_precision=avg_precision["micro-average"],
            estimator_name="Micro-average",
        ).plot(linestyle="--", ax=axes, color=cmap.reversed()(0))

        axes.legend(title="Label")
        if mlflow_logging:
            mlflow.log_figure(fig, f"precision-recall-curve/{output_name}.svg")
            plt.close()
            for k, v in avg_precision.items():
                mlflow.log_param(f"Average precision - {output_name} - {k}", v)
    return avg_precision


def build_roc_curves(
    confidences: DaitaFraime,
    Y: DaitaFraime,
    mlflow_logging: bool = False,
    build_plots: bool = True,
) -> dict[str, Any]:
    r"""Build receiver operating characteristic curves for each output.

    Build receiver operating characteristic curves for each output and additionally get the area
    under curve scores. In the case of multioutput objectives, it requires that each output should
    have output space the same as every other.

    Args:
        confidences: DaitaFraime of confidences of shape
            :math:`n_{\text{instances}} \times (n_{\text{outputs}} \times n_{\text{classes}})`.
        Y: Targets.
        mlflow_logging: Whether to log outputs to MLflow. Defaults to :code:`False`.
        build_plots: Whether to build the plots, often set to false if there are too many outputs
            and in this case it will not display them, but will still calculate and return them as a
            DataFrame. Defaults to :code:`False`.

    Returns:
        Area under curve scores for each output and each class.
    """
    roc_auc = {}
    for output_name in Y:
        confidence, one_hot_encoded_y = get_confidences_and_one_hot_encoded_y_for_all_classes(
            confidences[output_name], Y[output_name]
        )
        roc_auc[output_name] = build_roc_curve(
            confidence,
            one_hot_encoded_y,
            output_name=output_name,
            build_plot=build_plots,
            mlflow_logging=mlflow_logging,
        )
    return roc_auc


def build_roc_curve(
    confidences: DaitaFraime,
    labels: DaitaFraime,
    output_name: str,
    build_plot: bool = True,
    mlflow_logging: bool = False,
) -> dict[str, Any]:
    """Build an ROC curve for a particular output.

    Args:
        confidences: Confidences for the output as a DaitaFraime with each row an example and each
            column the probability of being that example.
        labels: True output labels as a one-hot encoded DaitaFraime.
        output_name: The name of the output.
        mlflow_logging: Whether to log outputs to MLflow. Defaults to :code:`False`.
        build_plot: Whether to build the plots, often set to false if there are too many outputs
            and in this case it will not display them, but will still calculate and return them as a
            DataFrame. Defaults to :code:`False`.

    Returns:
        Area under curve scores, including macro and micro.
    """
    if build_plot:
        fig, axes = plt.subplots(1, 1, figsize=(6, 6), tight_layout=True)
        axes.plot(
            [0, 1],
            [0, 1],
            linestyle="dotted",
            color=plt.rcParams["axes.labelcolor"],
            alpha=0.25,
            label="Random classifier (AUC = 0.50)",
        )
        axes.set_title(f"ROC curve: {output_name}")
        axes.set_xlim([-0.01, 1.01])
        axes.set_ylim([-0.01, 1.01])
        cmap = vis.get_cmap(N=labels.shape[1])

    roc_auc, fprs, tprs, thresholds, all_auc_calculable = {}, [], [], np.linspace(0, 1), True
    # first calculate metrics and plot curves for each class
    for i, class_name in enumerate(labels):
        # get the curve and ROC AUC for this class
        fpr, tpr, threshold = roc_curve(labels[class_name], confidences[class_name])
        if labels[class_name].nunique().squeeze() > 1:
            roc_auc[class_name] = roc_auc_score(labels[class_name], confidences[class_name])
        else:
            roc_auc[class_name], all_auc_calculable = np.nan, False
        # plot the curve for each class
        if build_plot:
            RocCurveDisplay(
                fpr=fpr, tpr=tpr, roc_auc=roc_auc[class_name], estimator_name=class_name
            ).plot(ax=axes, color=cmap(i))
        # standardize the curves to all the same length with all the same thresholds so that a
        # macro-average can be calculated later
        fprs.append(np.interp(thresholds, threshold[::-1], fpr[::-1]))
        tprs.append(np.interp(thresholds, threshold[::-1], tpr[::-1]))

    roc_auc["macro-average"] = roc_auc_score(labels, confidences) if all_auc_calculable else np.nan
    labels, confidences = labels.values.flatten(), confidences.values.flatten()
    micro_fpr, micro_tpr, _ = roc_curve(labels, confidences)
    roc_auc["micro-average"] = roc_auc_score(labels, confidences)

    if build_plot:
        RocCurveDisplay(
            fpr=np.mean(fprs, axis=0),
            tpr=np.mean(tprs, axis=0),
            roc_auc=roc_auc["macro-average"],
            estimator_name="Macro-average",
        ).plot(linestyle="--", ax=axes, color=cmap(0))
        RocCurveDisplay(
            fpr=micro_fpr,
            tpr=micro_tpr,
            roc_auc=roc_auc["micro-average"],
            estimator_name="Micro-average",
        ).plot(linestyle="--", ax=axes, color=cmap.reversed()(0))

        axes.legend(title="Label")
        if mlflow_logging:
            mlflow.log_figure(fig, f"roc-auc/{output_name}.svg")
            plt.close()
            for k, v in roc_auc.items():
                mlflow.log_param(f"ROC AUC - {output_name} - {k}", v)
    return roc_auc


def build_confidence_plots(
    confidences: DaitaFraime,
    Y: DaitaFraime,
    mlflow_logging: bool = False,
) -> None:
    r"""Build plots showing the confidences of the model.

    Build plots showing the confidences of the model predicting on for each class of each output.
    In the case of multioutput objectives, it requires that each output should have output space the
    same as every other.

    Args:
        confidences: DaitaFraime of confidences of shape
            :math:`n_{\text{instances}} \times (n_{\text{outputs}} \times n_{\text{classes}})`.
        Y: Targets.
        mlflow_logging: Whether to log outputs to MLflow. Defaults to :code:`False`.
    """
    for output_name in Y:
        confidence, one_hot_encoded_y = get_confidences_and_one_hot_encoded_y_for_all_classes(
            confidences[output_name], Y[output_name]
        )
        one_hot_encoded_y = one_hot_encoded_y.replace({False: "Negative", True: "Positive"})
        build_confidence_plot(confidence, one_hot_encoded_y, output_name, mlflow_logging)


def build_confidence_plot(
    confidences: DaitaFraime,
    labels: DaitaFraime,
    output_name: str,
    mlflow_logging: bool = False,
) -> None:
    """Build plots showing the confidences of the predictions for a particular output.

    Args:
        confidences: Confidences for the output as a DaitaFraime with each row an example and each
            column the probability of being that example.
        labels: True output labels as a one-hot encoded DaitaFraime.
        output_name: The name of the output.
        mlflow_logging: Whether to log outputs to MLflow. Defaults to :code:`False`.
    """
    for class_name in labels:
        fig, axes = plt.subplots(1, 1, figsize=(6, 6), tight_layout=True)
        cmap = vis.get_cmap(N=2)
        palette = [cmap(i) for i in range(2)]
        sns.scatterplot(
            x=confidences[class_name].values.flatten(),
            y=np.arange(len(labels)),
            hue=labels[class_name].values.flatten(),
            hue_order=["Negative", "Positive"],
            palette=palette,
            ax=axes,
            alpha=0.75,
        )
        decision_boundary = 0.5
        axes.vlines(
            x=decision_boundary,
            ymin=0,
            ymax=len(labels) - 1,
            linestyles="dashed",
            color=plt.rcParams["axes.labelcolor"],
            label="Decision boundary",
        )
        axes.axhspan(
            xmin=0,
            xmax=decision_boundary,
            ymin=0,
            ymax=len(labels) - 1,
            color=palette[0],
            alpha=0.1,
        )
        axes.axhspan(
            xmin=decision_boundary,
            xmax=1,
            ymin=0,
            ymax=len(labels) - 1,
            color=palette[1],
            alpha=0.1,
        )
        axes.annotate(
            "Negative",
            fontsize=plt.rcParams["axes.labelsize"],
            color=palette[0],
            xy=(0.42, 0.03),
            xytext=(0, 0),
            xycoords="axes fraction",
            textcoords="data",
            arrowprops=dict(arrowstyle="<-", lw=1, color=palette[0], relpos=(1, 0.5)),
            horizontalalignment="left",
            verticalalignment="top",
        )
        axes.annotate(
            "Positive",
            fontsize=plt.rcParams["axes.labelsize"],
            color=palette[1],
            xy=(0.58, 0.03),
            xytext=(1, 0),
            xycoords="axes fraction",
            textcoords="data",
            arrowprops=dict(arrowstyle="<-", lw=1, color=palette[1], relpos=(0, 0.5)),
            horizontalalignment="right",
            verticalalignment="top",
        )
        axes.text(
            s="Prediction",
            fontsize=plt.rcParams["axes.labelsize"],
            color=plt.rcParams["axes.labelcolor"],
            x=0.5,
            y=0,
            verticalalignment="top",
            horizontalalignment="center",
        )

        axes.set_xlim([-0.01, 1.01])
        axes.set_xlabel(f"Model confidence of class {class_name}")
        axes.set_ylabel("Example")
        axes.yaxis.set_major_locator(MaxNLocator(integer=True))
        axes.set_title(f"Confidences - {output_name} - {class_name}")
        axes.legend(title="True class")
        if mlflow_logging:
            mlflow.log_figure(fig, f"confidences/{output_name}/{class_name}.svg")
            plt.close()


def get_confidences_and_one_hot_encoded_y_for_all_classes(
    confidence: DaitaFraime, Y: DaitaFraime
) -> tuple[DaitaFraime, DaitaFraime]:
    r"""Get the confidence scores and one-hot-encoded targets for all classes.

    All classes are the union of those in the targets, and those that are in the model output space.
    This accounts for the cases when there are targets that the model did not see while training, or
    when there are examples in the model output space that are not in this series of targets.

    Args:
        confidence: Confidences for a single output of shape
            :math:`n_{\text{instances}} \times n_{\text{classes}}`.
        Y: Targets for this output.

    Returns:
        Confidences with any missing classes filled in as zeros (in order defined by
        `np.unique() <https://numpy.org/doc/stable/reference/generated/numpy.unique.html>`_), and
        one-hot-encoded targets with missing classes similarly filled.
    """
    predicted_classes = confidence.classes
    all_classes = np.unique(np.concatenate((Y.values.flatten(), predicted_classes)))
    n_classes = len(all_classes)

    # append all class names as temporary instances onto end of targets
    Y = pd.concat(
        (
            Y.to_pandas(),
            pd.DataFrame(
                all_classes, index=pd.Index(range(n_classes), name=Y.index.name), columns=Y.columns
            ),
        )
    )
    # remove the temporary instances after one-hot-encoding. The extra [all_classes] indexing
    # ensures that the columns are in the correct order.
    Y = DaitaFraime.from_pandas(pd.get_dummies(Y.values.flatten())[all_classes].iloc[:-n_classes])
    confidence = set_missing_classes_to_0_prob(confidence, predicted_classes, all_classes)
    return confidence, Y
