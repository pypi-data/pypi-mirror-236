"""Experiment tracking with MLflow."""


import mlflow

from scihence.utils._dict import unpack_dict


def set_mlflow_experiment(
    experiment_name: str | None = None,
    experiment_id: str | None = None,
) -> None:
    """Set the MLflow experiment.

    Will set it by its or name (only one can be specified), and if neither are specified then send
    to the experiment specified by :code:`default`.

    Args:
        experiment_name: Name of the experiment. Defaults to :code:`None`.
        experiment_id: ID of the experiment. Defaults to :code:`None`.

    Examples:
        >>> set_mlflow_experiment()
        >>> default_experiment = mlflow.get_experiment(mlflow.tracking.fluent._active_experiment_id)
        >>> default_experiment.name
        'Default'

        >>> my_experiment_name = "Test"
        >>> set_mlflow_experiment(experiment_name=my_experiment_name)
        >>> my_experiment = mlflow.get_experiment(mlflow.tracking.fluent._active_experiment_id)
        >>> my_experiment.name
        'Test'

        >>> set_mlflow_experiment(experiment_id=my_experiment.experiment_id)
        >>> my_experiment = mlflow.get_experiment(mlflow.tracking.fluent._active_experiment_id)
        >>> my_experiment.name
        'Test'
    """
    if (experiment_id is None) and (experiment_name is None):
        mlflow.set_experiment(experiment_name="Default")
    else:
        mlflow.set_experiment(experiment_name, experiment_id)


def mlflow_log_nested_dict(d: dict, separator: str = " - ") -> None:
    """Log a nested dictionary to MLflow.

    Args:
        d: Dictionary with potentially nested structure.
        separator: Separating string to place between levels of the hierarchy. Defaults to
            :code:`" - "`.

    Examples:
        >>> set_mlflow_experiment(experiment_name="Test")
        >>> with mlflow.start_run(run_name="test_mlflow_log_nested_dict") as run:
        ...     mlflow_log_nested_dict({"a": 1, "b": {"c": 2}})
        >>> mlflow.get_run(run.info.run_id).data.params
        {'b - c': '2', 'a': '1'}
    """
    mlflow.log_params({k: str(v)[:250] for k, v in unpack_dict(d, separator).items()})
