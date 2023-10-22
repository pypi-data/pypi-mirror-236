import logging

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold, StratifiedGroupKFold, train_test_split
from sklearn.model_selection._split import _BaseKFold
from sklearn.utils import shuffle as synchronized_shuffle

from scihence.ai._io import DaitaFraime
from scihence.ai.models._utils import ModelObjective
from scihence.utils import around

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def supervised_train_valid_test_split(
    X: DaitaFraime,
    Y: DaitaFraime,
    objective: ModelObjective,
    valid: int | float | _BaseKFold = 0,
    test: int | float | pd.Index = 0,
    remove_train_groups_from_test_when_idxs: bool = False,
    instance_tags: DaitaFraime | None = None,
) -> tuple[
    DaitaFraime,
    DaitaFraime,
    DaitaFraime,
    DaitaFraime,
    DaitaFraime | None,
    DaitaFraime | None,
    np.ndarray,
    np.ndarray,
    list[tuple[np.ndarray, np.ndarray]],
    bool,
    bool,
]:
    """Split data into training, validation, and testing sets.

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

    Returns:
        A tuple containing:

            * Training :code:`X`.
            * Testing :code:`X`.
            * Training :code:`Y`.
            * Testing :code:`Y`.
            * Training :code:`instance_tags`.
            * Testing :code:`instance_tags`.
            * Training numerical indices.
            * Testing numerical indices.
            * Folds as a list of length number of folds (length 1 if the validation set was
              specified as a number) with each element a tuple where the first item is for the
              training set and the second is for the testing set. Each of those items is a NumPy
              array specifying the indicies (as integers) of each of the instances in that fold.
            * Whether the pipeline includes a validation set.
            * Whether the pipeline includes a testing set.
    """
    groups = None if instance_tags is None else instance_tags.get("group")
    index_train, index_test = robust_stratified_train_test_split(
        X, Y, objective, test, valid, groups, remove_train_groups_from_test_when_idxs
    )

    X_train, X_test = X.loc[index_train], X.loc[index_test]
    Y_train, Y_test = Y.loc[index_train], Y.loc[index_test]
    groups_train = None if (groups is None) else groups.loc[index_train]
    if instance_tags is not None:
        instance_tags_train = instance_tags.loc[index_train]
        instance_tags_test = instance_tags.loc[index_test]
    else:
        instance_tags_train, instance_tags_test = None, None

    folds = fold_split(X_train, Y_train, objective, valid, groups_train)
    validating, testing = len(folds[0][1]) > 0, len(X_test) > 0

    if testing:
        train_percentage = int(around(100 * X_train.n_instances / X.n_instances))
        train_split = f"{X_train.n_instances} ({train_percentage}%)"
        test_percentage = int(around(100 * X_test.n_instances / X.n_instances))
        test_split = f"{X_test.n_instances} ({test_percentage}%)"
        logger.info(f"Actual train-test split: {train_split} - {test_split}.")
    if validating:
        for i, fold in enumerate(folds):
            train_percentage = int(around(100 * len(fold[0]) / X_train.n_instances))
            train_split = f"{len(fold[0])} ({train_percentage}%)"
            valid_percentage = int(around(100 * len(fold[1]) / X_train.n_instances))
            valid_split = f"{len(fold[1])} ({valid_percentage}%)"
            logger.info(f"Actual fold {i} train-valid split: {train_split} - {valid_split}.")
    return (
        X_train,
        X_test,
        Y_train,
        Y_test,
        instance_tags_train,
        instance_tags_test,
        index_train,
        index_test,
        folds,
        validating,
        testing,
    )


def robust_stratified_train_test_split(
    X: DaitaFraime,
    Y: DaitaFraime,
    objective: ModelObjective,
    test: int | float | pd.Index = 0,
    valid: int | float | _BaseKFold = 0,
    groups: pd.Series | None = None,
    remove_train_groups_from_test_when_idxs: bool = False,
) -> tuple[np.ndarray, np.ndarray]:
    """Perform a stratified group training-testing split, to get indices in each split.

    If the :code:`objective` is not for a single output, then only do a group split, but if we have
    a single output, then use a stratified group split.

    Args:
        X: Model input data.
        Y: Model target data.
        objective: Objective of the learning problem, from {"binary", "multiclass",
            "mulitlabel-indicator", "multiclass-multioutput", "continuous", "continuous-multioutput"
            }.
        test: How to build the testing set. Can be an integer to specify the number to use, can be a
            float to specify a proportion to use, or can be a sequence of integers to specfy the
            indices of inputs to use as the test set. Defaults to :code:`0`.
        valid: How to build the cross-validation set. Can be an integer to specify the number to use
            , can be a float to specify a proportion to use, or can be a `cross validation
            class that inherits from _BaseKFold <https://github.com/scikit-learn/scikit-learn/blob/9
            aaed498795f68e5956ea762fef9c440ca9eb239/sklearn/model_selection/_split.py#L285>`_.
            Defaults to :code:`0`.
        groups: The groups that should define how instances are stratified when split into training
            folds, and test sets, and must be in the same order as :code:`X` and :code:`Y`. Defaults
            to :code:`None`.
        remove_train_groups_from_test_when_idxs: When specifying the test set by its specific
            indices, it may have some examples of training groups within the test set. By setting
            this to :code:`True`, the training groups (if specified by their numerical indices) will
            be removed from the test set. Defaults to :code:`False`.

    Raises:
        ValueError: If the test set is incorrectly specified.

    Returns:
        Numerical indices to use in the training set and in the testing set respectively.
    """
    # if test size is a number and no need to stratify by group, do normal train-test split
    if (test_is_numeric := isinstance(test, float | int)) and ((groups is None) or (test == 0)):
        return robust_train_test_split(
            Y.index.get_level_values(0).unique(), test_size=test, shuffle=True
        )
    # if test size is a number, and need to stratify by group
    elif test_is_numeric:
        return stratified_group_train_test_split(
            X,
            Y,
            objective,
            groups,
            test_size=test,
            split_procedure=valid if isinstance(valid, _BaseKFold) else None,
        )
    # if the test set is specified as an array of indices
    elif isinstance(test, pd.Index):
        if isinstance(test, pd.MultiIndex):
            raise TypeError(
                "Test indices must not be MultiIndex. Only the first index level should be given."
            )
        index_train = Y.index.get_level_values(0).unique()
        index_train = index_train[~index_train.isin(index_test := test.unique())]
        if remove_train_groups_from_test_when_idxs and (groups is not None):
            test_group_in_train = groups.loc[index_test].isin(groups.loc[index_train]).to_series()
            test_idxs_to_remove = groups[test_group_in_train].index.get_level_values(0).unique()
            index_test = index_test[~np.isin(index_test, test_idxs_to_remove)]
        elif remove_train_groups_from_test_when_idxs:
            logger.warning(
                "Specified to remove instances from the test set if their group was also in the "
                "training set, however, no groups have been provided."
            )
        return index_train, index_test
    raise ValueError("Unsupported test set specification.")


def robust_train_test_split(*args, test_size: float, shuffle: bool = False) -> list[pd.Index]:
    """Perform a train-test split, including if :code:`test_size` is specified as :code:`0`.

    Args:
        *args: Indexable :code:`pd.Index` objects of the same length to split into two sets.
        test_size: How to build the testing set. Can be an integer to specify the number to use, or
            can be a float to specify a proportion to use. Defaults to :code:`0`.
        shuffle: Whether to shuffle the instances randomly. Defaults to :code:`False`.

    Returns:
        Split arguments in the form of :code:`[args[0]_train, args[0]_test, args[1]_train,
        args[1]_test, ...]`.
    """
    if test_size == 0:
        if shuffle:
            n_args = len(args)
            args = synchronized_shuffle(*args) if shuffle else args
            args = (args,) if n_args == 1 else args
        arg_empty_tuples = [(arg, arg.copy(deep=True)[:0]) for arg in args]
        return [obj for tup in arg_empty_tuples for obj in tup]
    return train_test_split(*args, test_size=test_size, shuffle=shuffle)


def stratified_group_train_test_split(
    X: DaitaFraime,
    Y: DaitaFraime,
    objective: ModelObjective,
    groups: DaitaFraime,
    test_size: float = 0,
    split_procedure: _BaseKFold | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Perform a train-test split when stratification dependent upon :code:`groups` is required.

    Args:
        X: Model input data.
        Y: Model target data.
        objective: Objective of the learning problem, from {"binary", "multiclass",
            "mulitlabel-indicator", "multiclass-multioutput", "continuous", "continuous-multioutput"
            }.
        groups: The groups that should define how instances are stratified when split into training
            folds, and test sets, and must be in the same order as :code:`X` and :code:`Y`. Defaults
            to :code:`None`.
        test_size: How to build the testing set. Can be an integer to specify the number to use, or
            can be a float to specify a proportion to use. Defaults to :code:`0`.
        split_procedure: The splitting procedure, if a :class:`_BaseKFold` instance, then will use
            this class to do the split, else will choose one automatically. Defaults to
                :code:`None`.

    Returns:
        Fold specification as a tuple where the first item is for the training set and the second is
        for the testing set. Each of those items is a NumPy array specifying the indicies (as
        integers) of each of the instances in that fold.
    """
    # get number of splits for a stratified split
    test_size = test_size / Y.n_instances if test_size >= 1 else test_size
    n_splits = int(around(1 / test_size))
    n_splits = 2 if n_splits == 1 else n_splits

    # use a scikit-learn KFold class to do a stratified split
    if (
        objective in ModelObjective.filter("classification", "single-output")
        and not Y.is_sequential
    ):
        # stratify by output class if single output classification objective
        if split_procedure:
            splitter = split_procedure.__class__(n_splits=n_splits)
        else:
            splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True)
    else:
        splitter = GroupKFold(n_splits=n_splits)

    Y = Y.get_sequence_starts(1).droplevel(1) if Y.is_sequential else Y
    X = X.get_sequence_starts(1).droplevel(1) if X.is_sequential else X
    if groups.is_sequential:
        groups = groups.get_sequence_starts(1).droplevel(1)
        logger.warning(
            "Groups specified per sequence item. Assuming sequence group is equivalent to first "
            "sequence item group."
        )

    # get indices for each split
    index_train, index_test = next(splitter.split(X, Y, groups))
    index_train, index_test = Y.index[index_train], Y.index[index_test]
    # if the train and test sets are the wrong way round, then switch
    train_ratio, test_ratio = len(index_train) / Y.n_instances, len(index_test) / Y.n_instances
    if np.abs(test_ratio - test_size) > np.abs(train_ratio - test_size):
        index_train, index_test = index_test, index_train
    return index_train, index_test


def fold_split(
    X: DaitaFraime,
    Y: DaitaFraime,
    objective: ModelObjective,
    valid: int | float | _BaseKFold = 0,
    groups: pd.Series | None = None,
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Create data folds.

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
        groups: The groups that should define how instances are stratified when split into training
            folds, and test sets, and must be in the same order as :code:`X` and :code:`Y`. Defaults
            to :code:`None`.

    Raises:
        ValueError: If unsupported cross-validation set specification

    Returns:
        Folds as a list of length number of folds (length 1 if the validation set was specified as
        a number) with each element a tuple where the first item is for the training set and the
        second is for the testing set. Each of those items is a NumPy array specifying the indicies
        (as integers) of each of the instances in that fold.
    """
    # if validation size is numeric and no need to stratify by group, do a normal train-test split
    if (valid_is_numeric := isinstance(valid, float | int)) and ((groups is None) or valid == 0):
        return [robust_train_test_split(Y.index.get_level_values(0).unique(), test_size=valid)]
    # if test size is a number, and need to stratify by group
    if valid_is_numeric:
        return [stratified_group_train_test_split(X, Y, objective, groups, test_size=valid)]
    # if it is a scikit-learn KFold object
    if isinstance(valid, _BaseKFold):
        Y = Y.get_sequence_starts(1).droplevel(1) if Y.is_sequential else Y
        X = X.get_sequence_starts(1).droplevel(1) if X.is_sequential else X
        if groups.is_sequential:
            groups = groups.get_sequence_starts(1).droplevel(1)
            logger.warning(
                "Groups specified per sequence item. Assuming sequence group is equivalent to first"
                " sequence item group."
            )
        return [
            (Y.index[fold[0]], Y.index[fold[1]])
            for fold in valid.split(X.loc[Y.index], Y, groups=groups)
        ]
    raise ValueError("Unsupported cross-validation specification.")
