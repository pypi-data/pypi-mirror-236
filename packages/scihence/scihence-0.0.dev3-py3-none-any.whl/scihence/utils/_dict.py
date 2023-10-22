"""Dictionary utilities."""

import pandas as pd


def unpack_dict(dictionary: dict, separator: str = "-") -> dict:
    """Unpack a nested dictionary into a dictionary of a single-layer.

    Args:
        dictionary: Dictionary to unpack.
        separator: String to use to separate levels of the dictionary hierarchy. Defaults to
            :code:`"-"`.

    Returns:
        Single-layer dictionary.

    Examples:
        >>> unpack_dict({"a": 1, "b": {"c": 2}})
        {'a': 1, 'b-c': 2}
    """
    return pd.json_normalize(dictionary, sep=separator).to_dict(orient="records")[0]


def get_dict_without_keys(dictionary: dict, keys: list) -> dict:
    """Return the dictionary without the specified keys, without modifying the original dictionary.

    Args:
        dictionary: Dictionary with keys to be removed.
        keys: Keys to be removed.

    Returns:
        Dictionary without the specified keys.

    Examples:
        >>> get_dict_without_keys({"a": 1, "b": 2}, ["b"])
        {'a': 1}
    """
    return {k: v for k, v in dictionary.items() if k not in keys}
