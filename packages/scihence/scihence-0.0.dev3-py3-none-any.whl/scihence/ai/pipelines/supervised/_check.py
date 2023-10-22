import logging

import numpy as np

from scihence.ai._io import DaitaFraime
from scihence.ai.models._utils import ModelObjective

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def check_supervised_pipeline_inputs(
    X: DaitaFraime,
    Y: DaitaFraime,
    objective: ModelObjective,
    instance_tags: DaitaFraime | None = None,
    feature_tags: DaitaFraime | None = None,
) -> None:
    """Check the inputs to the supervised learning pipeline.

    Args:
        X: Model input data.
        Y: Model target data.
        objective: Objective of the learning problem, from {"binary", "multiclass",
            "mulitlabel-indicator", "multiclass-multioutput", "continuous", "continuous-multioutput"
            }.
        instance_tags: Tags associated with each instance. Defaults to :code:`None`.
        feature_tags: Tags associated with each feature. Defaults to :code:`None`.

    Raises:
        ValueError: If the number of input instances does not equal the number of output instances.
        ValueError: If the index of :code:`X` is not equal to the index of :code:`Y`.
    """
    if not isinstance(X, DaitaFraime):
        raise TypeError("X must be a DaitaFraime.")
    if not isinstance(Y, DaitaFraime):
        raise TypeError("Y must be a DaitaFraime.")
    if (instance_tags is not None) and (not isinstance(instance_tags,DaitaFraime)):
        raise TypeError("instance_tags must be DaitaFraime.")
    if (feature_tags is not None) and (not isinstance(feature_tags, DaitaFraime)):
        raise TypeError("feature_tags must be a DaitaFrame.")

    X_index_lvl0_values = X.index.get_level_values(0).unique()
    if (X_index_lvl0_values != Y.index.get_level_values(0).unique()).any():
        raise ValueError("X and Y first index levels contain non-common indices.")
    if (X.index.names[0] != Y.index.names[0]):
        raise ValueError("X and Y first index level names are not equivalent.")

    if instance_tags is not None:
        if instance_tags.is_sequential:
            if (X.index != instance_tags.index).any():
                raise ValueError("Per-item sequential instance_tags' index does not match X's.")
            if (instance_tags.index.names != X.index.names):
                raise ValueError("Per-item sequential instance_tags' index does not match X's.")
        else:
            if (X_index_lvl0_values != instance_tags.index.get_level_values(0).unique()).any():
                raise ValueError("instance_tags' first level index does not match X's.")
            if (X.index.names[0] != instance_tags.index.names[0]):
                raise ValueError("instance_tags' first level index name does not match X's.")

    if feature_tags is not None:
        if (feature_tags.index != X.columns).any():
            raise ValueError("feature_tags index is not the same as X's columns.")
        if (feature_tags.index.names != X.columns.names):
            raise ValueError("feature_tags index names are not the same as X's columns' names.")

    check_objective(Y, objective)


def check_objective(Y: DaitaFraime, objective: ModelObjective) -> None:
    """Check the objective of the supervised learning pipeline.

    Args:
        Y: Model target data.
        objective: Objective of the learning problem, from {"binary", "multiclass",
            "mulitlabel-indicator", "multiclass-multioutput", "continuous", "continuous-multioutput"
            }.

    Raises:
        ValueError: If binary objective but moer than one output.
        ValueError: If binary objective but more than two classes.
        ValueError: If multiclass objective but more than one output.
        ValueError: If multiclass objective but two classes.
        ValueError: If multilabel-indicator objective but one output.
        ValueError: If multilabel-indicator objective but more than two classes.
        ValueError: If multiclass-multioutput objective but one output.
        ValueError: If multiclass-multioutput objective but two classes.
        ValueError: If continuous objective but more than one output.
        ValueError: If continuous-multioutput objective but one output.
        ValueError: If unsupported objective.
    """
    n_outputs, n_classes = Y.n_fields, len(np.unique(Y))

    def n_output_error_message(multioutput: bool) -> str:
        """Generate an error message for the incorrect number of outputs.

        Args:
            multioutput:  If the output should be multioutput.

        Returns:
            Error message.
        """
        return (
            f"Number of outputs is {n_outputs}, but {'>1 are' if multioutput else '1 is'} required"
            f" for a {objective} objective."
        )

    def n_classes_error_message(multiclass: bool) -> str:
        """Generate an error message for the incorrect number of classes.

        Args:
            multiclass: If the output should be multiclass.

        Returns:
            Error message.
        """
        return (
            f"Number of output classes is {n_classes}, but {'>' if multiclass else ''}2 are "
            f"required for a {objective} objective."
        )

    if objective == "binary":
        if n_outputs != 1:
            raise ValueError(n_output_error_message(multioutput=False))
        if n_classes != 2:
            raise ValueError(n_classes_error_message(multiclass=False))
    elif objective == "multiclass":
        if n_outputs != 1:
            raise ValueError(n_output_error_message(multioutput=False))
        if n_classes < 3:
            raise ValueError(n_classes_error_message(multiclass=True))
    elif objective == "multilabel-indicator":
        if n_outputs < 2:
            raise ValueError(n_output_error_message(multioutput=True))
        if n_classes != 2:
            raise ValueError(n_classes_error_message(multiclass=False))
    elif objective == "multiclass-multioutput":
        if n_outputs < 2:
            raise ValueError(n_output_error_message(multioutput=True))
        if n_classes < 3:
            raise ValueError(n_classes_error_message(multiclass=True))
    elif objective == "continuous":
        if n_outputs != 1:
            raise ValueError(n_output_error_message(multioutput=False))
    elif objective == "continuous-multioutput":
        if n_outputs < 2:
            raise ValueError(n_output_error_message(multioutput=True))
    else:
        raise ValueError(
            f"Unsupported objective: {objective}. Only supports objectives in {ModelObjective}."
        )
