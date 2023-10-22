"""Scihence's AI input/output objects."""
from collections.abc import Callable, Iterator
from typing import Any, Literal, Self

import numpy as np
import pandas as pd
import torch
from pandas._libs.lib import maybe_indices_to_slice
from pandas.core.common import is_bool_indexer
from pandas.core.indexing import _iLocIndexer, _LocIndexer
from torch import Tensor, tensor


def get_multi_loc_idx(idxs: tuple | slice | list | pd.Index) -> tuple | slice | list | pd.Index:
    """Standardise the way that indexing occurs in the :code:`loc` method.

    Args:
        idxs: Indexing.

    Returns:
        Adjusted index that is equivalent for a :code:`pandas.DataFrame.loc`.
    """
    if isinstance(idxs, tuple) and any(
        isinstance(idx, tuple | slice) or is_bool_indexer(idx) for idx in idxs
    ):
        idxs = list(idxs)
        for i, idx in enumerate(idxs):
            idxs[i] = get_multi_loc_idx(idx)
        return tuple(idxs)
    if isinstance(idxs, slice) or isinstance(idxs, list | pd.Index) or is_bool_indexer(idxs):
        return idxs
    return [idxs]


class _DaitaFraimeLocIndexer(_LocIndexer):
    """Class to facilitate the function of a :code:`.loc` on a :class:`DaitaFraime`."""

    def __getitem__(self, idxs):
        """Index a :class:`DaitaFraime` using :code:`DaitaFraime.loc[...]`."""
        return DaitaFraime(super().__getitem__(get_multi_loc_idx(idxs)))


class _DaitaFraimeiLocIndexer(_iLocIndexer):
    """Class to facilitate the function of a :code:`.iloc` on a :class:`DaitaFraime`."""

    def __getitem__(self, idx):
        """Index a :class:`DaitaFraime` using :code:`DaitaFraime.iloc[...]`."""
        return DaitaFraime(super().__getitem__(get_multi_loc_idx(idx)))


class DaitaFraime:
    """AI DataFrame."""

    _from_type_options = ("numpy", "pandas", "torch", "scihence")
    """Types from which a :class:`DaitaFraime` can be constructed."""

    def __init__(self, df: pd.DataFrame | pd.Series | Self) -> None:
        """Initialise an instance.

        Args:
            df: DataFrame backbone.
        """
        if isinstance(df, pd.Series):
            df = pd.DataFrame(df)
        if isinstance(df, DaitaFraime):
            df = df._dataframe
        elif isinstance(df, pd.DataFrame):
            DaitaFraime._is_dataframe_daitafraimeable(df, raise_err=True)
        else:
            raise TypeError("Input must be a pd.Series, pd.DataFrame, or DaitaFraime.")
        self._dataframe = df.sort_index(
            level=0 if df.index.nlevels > 1 else None, sort_remaining=False
        )
        self._AXIS_ORDERS = self._dataframe._AXIS_ORDERS

    @staticmethod
    def _is_dataframe_daitafraimeable(df: pd.DataFrame, raise_err: bool = False) -> bool:
        """Check if a DataFrame is suitable for the backbone of a DaitaFraime.

        Args:
            df: Potential DataFrame backbone.
            raise_err: Whether to raise an error if bad. Defaults to :code:`False`.

        Raises:
            TypeError: If the input is not a pd.DataFrame or a pd.Series.
            TypeError: If the input has :math`> 2` index levels.
            TypeError: If the input does not have a unique index.
            TypeError: If the input has :math`> 2` columns levels.
            TypeError: If the input does not have unique columns.

        Returns:
            Whether the input is valid.
        """
        if isinstance(df, pd.Series):
            df = pd.DataFrame(df)
        if not isinstance(df, pd.DataFrame):
            if raise_err:
                raise TypeError("DataFrame must be a pd.DataFrame.")
            return False
        if df.index.nlevels > 2:
            if raise_err:
                raise TypeError("DataFrame must have <= 2 index levels.")
            return False
        if not df.index.is_unique:
            if raise_err:
                raise TypeError("DataFrame must have unique indices.")
            return False
        if df.columns.nlevels > 2:
            if raise_err:
                raise TypeError("DataFrame must have <= 2 columns levels.")
            return False
        if not df.columns.is_unique:
            if raise_err:
                raise TypeError("DataFrame must have unique columns.")
            return False
        return True

    @staticmethod
    def coerce(
        x,
        from_type: Literal["numpy", "pandas", "torch", "scihence"] | None = None,
        none_ok: bool = False,
    ) -> bool:
        """Coerce the input to a :class:`DaitaFraime`.

        Args:
            x: Input to coerce.
            from_type: Type from which to coerce. If :code:`None`, will automatically select the
                appropriate one. Defaults to :code:`None`.
            none_ok: If an input of :code:`None` can be valid. Defaults to :code:`False`.

        Raises:
            ValueError: If uncoercible.

        Returns:
            Coerced :class:`DaitaFraime`.
        """
        if none_ok and x is None:
            return x
        if DaitaFraime._is_dataframe_daitafraimeable(x):
            return DaitaFraime(x)
        for type_option in DaitaFraime._from_type_options if from_type is None else [from_type]:
            if DaitaFraime.is_coercible(x, from_type=type_option):
                return DaitaFraime._from_obj(x, from_type=type_option)
        raise ValueError("Uncoercible to DaitaFraime.")

    @staticmethod
    def coerce_output(*coerce_args, **coerce_kwargs) -> Callable:
        """Decorator factory to coerce the output of a function to a :class:`DaitaFraime`.

        Returns:
            Decorator function that coerces the output of a wrapped function.
        """
        def coerce_decorator(f: Callable) -> Callable:
            def f_coerced(*args, **kwargs) -> Self:
                return DaitaFraime.coerce(f(*args, **kwargs), *coerce_args, **coerce_kwargs)

            return f_coerced

        return coerce_decorator

    @staticmethod
    def is_coercible(
        x: Any,
        raise_err: bool = False,
        sequential: bool | None = None,
        proba: bool | None = None,
        from_type: Literal["numpy", "pandas", "torch", "scihence"] | None = None,
    ) -> bool:
        """Check if an object is coercible to a :code:`DaitaFraime`.

        Args:
            x: Input.
            raise_err: Whether to raise an error if not coercible. Defaults to :code:`False`.
            sequential: Whether the DaitaFraime should be sequential. If :code:`None`, will try all
                options. Defaults to :code:`None`.
            proba: Whether the DaitaFraime should be probabilistic. If :code:`None`, will try all
                options. Defaults to :code:`None`.
            from_type: Type of input. If :code:`None`, will try all options. Defaults to
                :code:`None`.

        Raises:
            ValueError: If the input is neither sequential or non-sequential when
                :code:`sequential is None`.
            ValueError: If the input is neither probabilistic or non-probabilistic when
                :code:`proba is None`.
            ValueError: If the input does not conform to any of the type options when
                :code:`from_type is None`.
            ValueError: If :code:`from_type` input is not supported.

        Returns:
            Whether it is coercible.
        """
        if sequential is None:
            flag = any(
                DaitaFraime.is_coercible(x, sequential=sequential, proba=proba, from_type=from_type)
                for sequential in [False, True]
            )
            if raise_err and (not flag):
                raise ValueError("DaitaFraime input is neither sequential or non-sequential.")
            return flag
        if proba is None:
            flag = any(
                DaitaFraime.is_coercible(x, sequential=sequential, proba=proba, from_type=from_type)
                for proba in [False, True]
            )
            if raise_err and (not flag):
                raise ValueError("DaitaFraime input is neither probabilistic or non-probabilistic.")
            return flag
        if from_type is None:
            if isinstance(x, DaitaFraime):
                return True
            flag = any(
                DaitaFraime.is_coercible(x, sequential=sequential, proba=proba, from_type=from_type)
                for from_type in DaitaFraime._from_type_options
            )
            if raise_err and (not flag):
                raise ValueError(f"DaitaFraime input is none of {DaitaFraime._from_type_options}.")
            return flag
        if from_type not in DaitaFraime._from_type_options:
            raise ValueError(f"from_type must be one of {DaitaFraime._from_type_options}.")

        if sequential:
            return DaitaFraime._is_sequential_coercible(x, raise_err, proba, from_type)

        match from_type:
            case "numpy":
                return DaitaFraime._is_nonsequential_numpy_coercible(x, proba, raise_err)
            case "pandas":
                return DaitaFraime._is_nonsequential_pandas_coercible(x, proba, raise_err)
            case "torch":
                return DaitaFraime._is_nonsequential_torch_coercible(x, proba, raise_err)
            case "scihence":
                return isinstance(x, DaitaFraime)

    @staticmethod
    def _is_sequential_coercible(
        x: Any,
        raise_err: bool = False,
        proba: bool | None = None,
        from_type: Literal["numpy", "pandas", "torch", "scihence"] | None = None,
    ) -> bool:
        if not isinstance(x, list):
            if raise_err:
                raise TypeError(f"Unsupported sequential type. Received {type(x)}, requires list.")
            return False
        from_pandas = from_type == "pandas"
        for i, X in enumerate(x):
            if not DaitaFraime.is_coercible(
                X, raise_err, sequential=False, proba=proba, from_type=from_type
            ):
                return False
            if not isinstance(X, type(x[0])):
                if raise_err:
                    raise TypeError(
                        f"Elements of list must all be the same type. Element at position {i} "
                        f"is a {type(X)}, but the first element of the list is {type(x[0])}."
                    )
                return False
            if X.shape[1:] != x[0].shape[1:]:
                if raise_err:
                    raise TypeError("Shapes of all elements of list need to be equal.")
                return False
            if not from_pandas:
                continue
            if (X.columns != x[0].columns).any() or (X.columns.names != x[0].columns.names):
                if raise_err:
                    raise ValueError("Columns of all elements of list need to be equal.")
                return False
            if not (X.index.names == x[0].index.names):
                if raise_err:
                    raise ValueError("Index name of all elements of list need to be equal.")
                return False
        if from_pandas and not pd.concat(x).index.is_unique:
            if raise_err:
                raise ValueError("Input index is not unique.")
            return False
        if from_pandas and not pd.concat(x).columns.is_unique:
            if raise_err:
                raise ValueError("Input columns are not unique.")
            return False
        return True

    @staticmethod
    def _is_nonsequential_numpy_coercible(x: Any, proba: bool, raise_err: bool = False) -> bool:
        if not isinstance(x, np.ndarray):
            if raise_err:
                raise TypeError(
                    "Input (or elements of sequential input) must be of type numpy.ndarray, "
                    f"received {type(x)}."
                )
            return False
        if (not proba) and (x.ndim != 2):
            if raise_err:
                raise TypeError(
                    "Input (or elements of sequential input) must have 2 dimensions for a numpy "
                    f"non-probabilistic DaitaFraime, received {x.ndim}."
                )
            return False
        if proba and (x.ndim != 3):
            if raise_err:
                raise TypeError(
                    "Input (or elements of sequential input) must have 3 dimensions for a numpy "
                    f"probabilistic DaitaFraime, received {x.ndim}."
                )
            return False
        return True

    @staticmethod
    def _is_nonsequential_pandas_coercible(x: Any, proba: bool, raise_err: bool = False) -> bool:
        if isinstance(x, pd.Series):
            x = pd.DataFrame(x)
        if not isinstance(x, pd.DataFrame):
            if raise_err:
                raise TypeError(
                    "Input (or elements of sequential input) must be of type pandas.DataFrame, "
                    f"received {type(x)}."
                )
            return False
        if x.index.nlevels != 1:
            if raise_err:
                raise ValueError(
                    "Input (or elements of sequential input) must have 1 index level for a pandas "
                    f"DaitaFraime, received {x.index.nlevels}."
                )
            return False
        if (not proba) and (x.columns.nlevels != 1):
            if raise_err:
                raise ValueError(
                    "Input (or elements of sequential input) must have 1 column level for a pandas "
                    f"non-probabilistic DaitaFraime, received {x.columns.nlevels}."
                )
            return False
        if proba and (x.columns.nlevels != 2):
            if raise_err:
                raise ValueError(
                    "Input (or elements of sequential input) must have 2 column levels for a pandas"
                    f" probabilistic DaitaFraime, received {x.columns.nlevels}."
                )
            return False
        if not x.index.is_unique:
            if raise_err:
                raise ValueError("Input index is not unique.")
            return False
        if not x.columns.is_unique:
            if raise_err:
                raise ValueError("Input columns are not unique.")
            return False
        return True

    @staticmethod
    def _is_nonsequential_torch_coercible(x: Any, proba: bool, raise_err: bool = False) -> bool:
        if not isinstance(x, Tensor):
            if raise_err:
                raise TypeError(
                    "Input (or elements of sequential input) must be of type torch.Tensor, received"
                    f" {type(x)}."
                )
            return False
        if (not proba) and (x.ndim != 2):
            if raise_err:
                raise TypeError(
                    "Input (or elements of sequential input) must have 2 dimensions for a torch "
                    f"non-probabilistic DaitaFraime, received {x.ndim}."
                )
            return False
        if proba and (x.ndim != 3):
            if raise_err:
                raise TypeError(
                    "Input (or elements of sequential input) must have 3 dimensions for a torch "
                    f"probabilistic DaitaFraime, received {x.ndim}."
                )
            return False
        return True

    def __getitem__(self, idxs) -> Any:
        if pd.core.common.is_bool_indexer(idxs):
            return DaitaFraime.coerce(self._dataframe[idxs], from_type="pandas")
        if isinstance(idxs, slice):
            idxs = self.index._convert_slice_indexer(idxs, kind="getitem")
            if isinstance(idxs, np.ndarray):
                idxs = maybe_indices_to_slice(idxs.astype(np.intp, copy=False), len(self))
            if isinstance(idxs, np.ndarray):
                return self.take(idxs, axis=0)
            return DaitaFraime.coerce(self._slice(idxs, axis=0), from_type="pandas")
        return self.loc[:, idxs]

    @coerce_output(from_type="pandas")
    def apply(self, *args, **kwargs):
        return self._dataframe.apply(*args, **kwargs)

    @coerce_output(from_type="pandas")
    def take(self, *args, **kwargs):
        return self._dataframe.take(*args, **kwargs)

    def _get_value(self, *args, **kwargs) -> Any:
        return self._dataframe._get_value(*args, **kwargs)

    def _slice(self, *args, **kwargs) -> Any:
        return self._dataframe._slice(*args, **kwargs)

    def __array__(self, *args, **kwargs) -> np.ndarray:
        return self._dataframe.__array__(*args, **kwargs)

    def __iter__(self, *args, **kwargs) -> Iterator:
        return self._dataframe.__iter__(*args, **kwargs)

    def __repr__(self) -> str:
        return self._dataframe.__repr__()

    def _repr_html_(self) -> str | None:
        return self._dataframe._repr_html_()

    def __len__(self) -> int:
        return self._dataframe.__len__()

    @coerce_output(from_type="pandas")
    def __sub__(self, right) -> Self:
        if isinstance(right, DaitaFraime):
            right = right._dataframe
        if isinstance(right, pd.DataFrame):
            right = right.values
        return self._dataframe.__sub__(right)

    @coerce_output(from_type="pandas")
    def __rsub__(self, left) -> Self:
        if isinstance(left, DaitaFraime):
            left = left._dataframe
        if isinstance(left, pd.DataFrame):
            left = left.values
        return self._dataframe.__rsub__(left)

    @coerce_output(from_type="pandas")
    def __add__(self, right) -> Self:
        if isinstance(right, DaitaFraime):
            right = right._dataframe
        if isinstance(right, pd.DataFrame):
            right = right.values
        return self._dataframe.__add__(right)

    @coerce_output(from_type="pandas")
    def __radd__(self, left) -> Self:
        if isinstance(left, DaitaFraime):
            left = left._dataframe
        if isinstance(left, pd.DataFrame):
            left = left.values
        return self._dataframe.__radd__(left)

    @coerce_output(from_type="pandas")
    def __lt__(self, right) -> Self:
        if isinstance(right, DaitaFraime):
            right = right._dataframe
        if isinstance(right, pd.DataFrame):
            right = right.values
        return self._dataframe.__lt__(right)

    @coerce_output(from_type="pandas")
    def __le__(self, right) -> Self:
        if isinstance(right, DaitaFraime):
            right = right._dataframe
        if isinstance(right, pd.DataFrame):
            right = right.values
        return self._dataframe.__le__(right)

    @coerce_output(from_type="pandas")
    def __gt__(self, right) -> Self:
        if isinstance(right, DaitaFraime):
            right = right._dataframe
        if isinstance(right, pd.DataFrame):
            right = right.values
        return self._dataframe.__gt__(right)

    @coerce_output(from_type="pandas")
    def __ge__(self, right) -> Self:
        if isinstance(right, DaitaFraime):
            right = right._dataframe
        if isinstance(right, pd.DataFrame):
            right = right.values
        return self._dataframe.__ge__(right)

    @coerce_output(from_type="pandas")
    def __mul__(self, right) -> Self:
        if isinstance(right, DaitaFraime):
            right = right._dataframe
        if isinstance(right, pd.DataFrame):
            right = right.values
        return self._dataframe.__mul__(right)

    @coerce_output(from_type="pandas")
    def __rmul__(self, left) -> Self:
        if isinstance(left, DaitaFraime):
            left = left._dataframe
        if isinstance(left, pd.DataFrame):
            left = left.values
        return self._dataframe.__rmul__(left)

    @coerce_output(from_type="pandas")
    def __truediv__(self, right) -> Self:
        if isinstance(right, DaitaFraime):
            right = right._dataframe
        if isinstance(right, pd.DataFrame):
            right = right.values
        return self._dataframe.__truediv__(right)

    @coerce_output(from_type="pandas")
    def __rtruediv__(self, left) -> Self:
        if isinstance(left, DaitaFraime):
            left = left._dataframe
        if isinstance(left, pd.DataFrame):
            left = left.values
        return self._dataframe.__rtruediv__(left)

    @coerce_output(from_type="pandas")
    def __pow__(self, exponent) -> Self:
        if isinstance(exponent, DaitaFraime):
            exponent = exponent._dataframe
        if isinstance(exponent, pd.DataFrame):
            exponent = exponent.values
        return self._dataframe.__pow__(exponent)

    def _get_axis(self, *args, **kwargs) -> pd.Index:
        return self._dataframe._get_axis(*args, **kwargs)

    def _get_axis_name(self, *args, **kwargs) -> pd.Index:
        return self._dataframe._get_axis(*args, **kwargs)

    def _get_axis_number(self, *args, **kwargs):
        return self._dataframe._get_axis_number(*args, **kwargs)

    def _reindex_with_indexers(self, *args, **kwargs):
        return self._dataframe._reindex_with_indexers(*args, **kwargs)

    def _take_with_is_copy(self, *args, **kwargs):
        return self._dataframe._take_with_is_copy(*args, **kwargs)

    def _ixs(self, *args, **kwargs):
        return self._dataframe._ixs(*args, **kwargs)

    @coerce_output(from_type="pandas")
    def xs(self, *args, **kwargs):
        return self._dataframe.xs(*args, **kwargs)

    @coerce_output(from_type="pandas")
    def get(self, *args, **kwargs):
        return self._dataframe.get(*args, **kwargs)

    @property
    def ndim(self) -> int:
        return self._dataframe.ndim

    @property
    def axes(self) -> int:
        return self._dataframe.axes

    @property
    def plot(self):
        return self._dataframe.plot

    @coerce_output(from_type="pandas")
    def copy(self, *args, **kwargs):
        return self._dataframe.copy(*args, **kwargs)

    @staticmethod
    @coerce_output(from_type="pandas")
    def concat(objs: tuple[Self], *args, **kwargs) -> Self:
        return pd.concat((obj._dataframe for obj in objs), *args, **kwargs)

    @coerce_output(from_type="pandas", none_ok=True)
    def rename(self, *args, **kwargs):
        return self._dataframe.rename(*args, **kwargs)

    def squeeze(self, *args, **kwargs) -> Self | pd.Series | Any:
        return self._dataframe.squeeze(*args, **kwargs)

    @coerce_output(from_type="pandas")
    def abs(self, *args, **kwargs):
        return self._dataframe.abs(*args, **kwargs)

    @coerce_output(from_type="pandas")
    def mean(self, *args, **kwargs):
        return self._dataframe.mean(*args, **kwargs)

    @coerce_output(from_type="pandas")
    def std(self, *args, **kwargs):
        return self._dataframe.std(*args, **kwargs)

    @property
    def shape(self) -> tuple:
        return self._dataframe.shape

    @property
    def index(self) -> pd.Index:
        return self._dataframe.index

    @index.setter
    def index(self, value) -> None:
        self._dataframe.index = value

    @property
    def n_instances(self) -> int:
        if self.is_sequential:
            return self.n_sequences
        return self.__len__()

    @property
    def n_sequences(self) -> int:
        if self.is_sequential:
            return len(self.index.get_level_values(0).unique())
        raise AttributeError("DaitaFraime has no sequences.")

    @property
    def columns(self) -> pd.Index:
        return self._dataframe.columns

    @columns.setter
    def columns(self, value) -> None:
        self._dataframe.columns = value

    @property
    def n_fields(self) -> int:
        if self.is_proba:
            return len(self.columns.get_level_values(0).unique())
        return len(self.columns)

    @property
    def classes(self) -> int:
        if self.is_proba:
            return self.columns.get_level_values(1).unique()
        raise AttributeError("DaitaFraime is not probabilistic, thus, it has no classes.")

    @property
    def n_classes(self) -> int:
        return len(self.classes)

    @property
    def loc(self) -> _DaitaFraimeLocIndexer:
        return _DaitaFraimeLocIndexer("loc", self)

    @property
    def iloc(self) -> _DaitaFraimeiLocIndexer:
        return _DaitaFraimeiLocIndexer("iloc", self)

    @property
    def is_sequential(self) -> bool:
        return isinstance(self.index, pd.MultiIndex)

    @property
    def is_proba(self) -> bool:
        return isinstance(self.columns, pd.MultiIndex)

    @property
    def values(self) -> np.ndarray:
        return self._dataframe.values

    @classmethod
    def _from_obj(
        cls,
        data: np.ndarray
        | Tensor
        | pd.Series
        | pd.DataFrame
        | list[np.ndarray]
        | list[pd.DataFrame]
        | list[Tensor],
        index: pd.Index | None = None,
        columns: pd.Index | None = None,
        from_type: Literal["numpy", "pandas", "torch", "scihence"] | None = None,
    ) -> Self:
        if DaitaFraime.is_coercible(data, from_type="scihence"):
            data.index = data.index if index is None else index
            data.columns = data.columns if columns is None else columns
            return cls(data)

        from_pandas = from_type == "pandas"
        sequential = DaitaFraime.is_coercible(data, sequential=True, from_type=from_type)
        if (index is None) and sequential:
            if from_pandas:
                index = pd.MultiIndex.from_arrays(
                    (
                        pd.Index(
                            sum([[i] * len(ls) for i, ls in enumerate(data)], []), name="sequence"
                        ),
                        pd.concat(data).index,
                    ),
                )
            else:
                index = pd.MultiIndex.from_tuples(
                    ((i, j) for i, _ in enumerate(data) for j in range(data[i].shape[0])),
                    names=("sequence", "item"),
                )
        if (columns is None) and DaitaFraime.is_coercible(data, proba=True, from_type=from_type):
            eg_instance = data[0] if sequential else data
            if from_pandas:
                columns = eg_instance.columns
            else:
                columns = pd.MultiIndex.from_tuples(
                    (
                        (i, j)
                        for i in range(eg_instance.shape[1])
                        for j in range(eg_instance.shape[2])
                    ),
                    names=("output", "class"),
                )

        DaitaFraime.is_coercible(data, raise_err=True, from_type=from_type)
        data = cls._dataframeify(data)
        data.index = data.index if index is None else index
        data.columns = data.columns if columns is None else columns
        return cls(data)

    @classmethod
    def _dataframeify(
        cls,
        data: np.ndarray
        | Tensor
        | pd.Series
        | pd.DataFrame
        | list[np.ndarray]
        | list[pd.DataFrame]
        | list[Tensor],
    ) -> pd.DataFrame:
        if isinstance(data, list):
            return pd.concat(DaitaFraime._dataframeify(sequence) for sequence in data)
        if data.ndim == 3:
            data = data.swapaxes(1, 2).reshape(data.shape[0], np.prod(data.shape[1:]))
        return pd.DataFrame(data)

    @classmethod
    def from_numpy(
        cls,
        data: np.ndarray | list[np.ndarray],
        index: pd.Index | None = None,
        columns: pd.Index | None = None,
    ) -> Self:
        """Create a :class:`DaitaFraime` from a numpy input.

        This must be a numpy array or list thereof if sequential.

        Args:
            data: Data.
            index: Index to use, if :code:`None` then generates a default index. Defaults to
                :code:`None`.
            columns: Columns to use, if :code:`None` then generates a default columns. Defaults to
                :code:`None`.

        Returns:
            New DaitaFraime.
        """
        return cls._from_obj(data, index, columns, from_type="numpy")

    @classmethod
    def from_pandas(
        cls,
        data: pd.DataFrame | pd.Series | list[pd.DataFrame] | list[pd.Series],
        index: pd.Index | None = None,
        columns: pd.Index | None = None,
    ) -> Self:
        """Create a :class:`DaitaFraime` from a pandas input.

        This must be a pandas Series, DataFrame, or list thereof if sequential.

        Args:
            data: Data.
            index: Index to use, if :code:`None` then uses the current index. Defaults to
                :code:`None`.
            columns: Columns to use, if :code:`None` then uses the current columns. Defaults to
                :code:`None`.

        Returns:
            New DaitaFraime.
        """
        sequential = isinstance(data, list)
        index = data.index if (index is None and not sequential) else index
        columns = (
            data.columns
            if ((columns is None) and (not sequential) and (data.ndim == 2))
            else columns
        )
        return cls._from_obj(data, index, columns, from_type="pandas")

    @classmethod
    def from_torch(
        cls,
        data: Tensor | list[Tensor],
        index: pd.Index | None = None,
        columns: pd.Index | None = None,
    ) -> Self:
        """Create a :class:`DaitaFraime` from a PyTorch input.

        This must be a PyTorch Tensor, or list thereof if sequential.

        Args:
            data: Data.
            index: Index to use, if :code:`None` then generates a default index. Defaults to
                :code:`None`.
            columns: Columns to use, if :code:`None` then generates a default columns. Defaults to
                :code:`None`.

        Returns:
            New DaitaFraime.
        """
        return cls._from_obj(
            [seq.detach() for seq in data] if isinstance(data, list) else data.detach(),
            index,
            columns,
            from_type="torch",
        )

    @classmethod
    def from_scihence(
        cls,
        data: Self,
        index: pd.Index | None = None,
        columns: pd.Index | None = None,
    ) -> Self:
        """Create a :class:`DaitaFraime` from a DaitaFraime input.

        Args:
            data: Data.
            index: Index to use, if :code:`None` then uses the current index. Defaults to
                :code:`None`.
            columns: Columns to use, if :code:`None` then uses the current columns. Defaults to
                :code:`None`.

        Returns:
            New DaitaFraime.
        """
        return cls._from_obj(data, index, columns, from_type="scihence")

    def to_pandas(self, seq_to_list: bool = False) -> pd.DataFrame | list[pd.DataFrame]:
        if seq_to_list and self.is_sequential:
            return [self._dataframe.xs(idx) for idx in self.index.get_level_values(0).unique()]
        return self._dataframe

    def to_series(self, seq_to_list: bool = False) -> pd.DataFrame | list[pd.DataFrame]:
        if self.shape[1] != 1:
            raise AttributeError(
                "DaitaFraime has more than one column and cannot be coerced to pandas.Series."
            )
        if seq_to_list and self.is_sequential:
            return [
                self.xs(idx).squeeze("columns") for idx in self.index.get_level_values(0).unique()
            ]
        return self.squeeze("columns")

    def to_numpy(self) -> np.ndarray | list[np.ndarray]:
        if self.is_sequential:
            return [self.xs(idx).values for idx in self.index.get_level_values(0).unique()]
        return self.values

    def to_torch(self, to_kwargs: dict[str, object] = {}) -> Tensor | list[Tensor]:
        to_kwargs = {"dtype": torch.get_default_dtype()} | to_kwargs
        if self.is_sequential:
            return [
                tensor(self.xs(idx).values).to(**to_kwargs)
                for idx in self.index.get_level_values(0).unique()
            ]
        return tensor(self.values).to(**to_kwargs)

    @property
    def sequence_lens(self):
        if self.is_sequential:
            return self.index.get_level_values(0).value_counts().sort_index()
        raise AttributeError("DaitaFraime has no sequences.")

    @coerce_output(from_type="pandas", none_ok=True)
    def replace(self, *args, **kwargs) -> Self | None:
        return self._dataframe.replace(*args, **kwargs)

    @coerce_output(from_type="pandas")
    def idxmax(self, *args, **kwargs) -> Self | Any:
        return self._dataframe.idxmax(*args, **kwargs)

    @coerce_output(from_type="pandas")
    def nunique(self, *args, **kwargs) -> int:
        return self._dataframe.nunique(*args, **kwargs)

    @coerce_output(from_type="pandas")
    def isin(self, values) -> int:
        if isinstance(values, DaitaFraime):
            values = values._dataframe
        return self._dataframe.isin(values)

    def save_state_and_stack(self):
        df = self._dataframe.stack()
        return df, (df.index, df.columns if self.is_proba else df.name, self.index, self.columns)

    @classmethod
    def from_stacked(cls: type[Self], x: np.ndarray, state: tuple):
        x = pd.DataFrame(x.reshape(-1, 1), index=state[0], columns=state[1]).unstack()
        x.index, x.columns = state[2:]
        return cls(x)

    @coerce_output(from_type="pandas")
    def unstack(self, *args, **kwargs) -> Self:
        return self._dataframe.unstack(*args, **kwargs)

    @coerce_output(from_type="pandas")
    def stack(self, *args, **kwargs) -> Self:
        return self._dataframe.stack(*args, **kwargs)

    @coerce_output(from_type="pandas", none_ok=True)
    def drop(self, *args, **kwargs) -> Self:
        return self._dataframe.drop(*args, **kwargs)

    @coerce_output(from_type="pandas")
    def droplevel(self, *args, **kwargs) -> Self:
        return self._dataframe.droplevel(*args, **kwargs)

    @coerce_output(from_type="pandas")
    def swapaxes(self, *args, **kwargs) -> Self:
        return self._dataframe.swapaxes(*args, **kwargs)

    @coerce_output(from_type="pandas")
    def get_sequence_starts(self, max_n_items: int = 1):
        """Get all of the first at most :code:`max_n_items` from each sequence.

        Args:
            max_n_items: Maximum number of items to retrieve from each sequence. Defaults to
                :code:`1`.

        Raises:
            AttributeError: If DaitaFraime is not sequential.

        Returns:
            DaitaFraime with the first at most :code:`max_n_items` from each sequence.
        """
        if not self.is_sequential:
            raise AttributeError("DaitaFraime has no sequences.")
        return self._dataframe.groupby(level=0).head(max_n_items)

    @coerce_output(from_type="pandas")
    def get_sequence_ends(self, max_n_items: int = 1):
        """Get all of the last at most :code:`max_n_items` from each sequence.

        Args:
            max_n_items: Maximum number of items to retrieve from each sequence. Defaults to
                :code:`1`.

        Raises:
            AttributeError: If DaitaFraime is not sequential.

        Returns:
            DaitaFraime with the last at most :code:`max_n_items` from each sequence.
        """
        if not self.is_sequential:
            raise AttributeError("DaitaFraime has no sequences.")
        return self._dataframe.groupby(level=0).tail(max_n_items)
