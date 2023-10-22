"""Math utilities."""
import numpy as np


def set_sig_figs(x: float, n_sig_figs: int = 3) -> str:
    r"""Formats a number to a specified number of significant figures.

    Args:
        x: The number to be formatted.
        n_sig_figs: The number of significant figures in the output format. Defaults to :code:`3`.

    Returns:
        A string representation of the formatted number to a specified number of significant
        figures.

    Examples:
        >>> set_sig_figs(1234.5678, 3)
        '$1.23 \\times 10^{3}$'
        >>> set_sig_figs(0.123456, 4)
        '$1.235 \\times 10^{-1}$'
        >>> set_sig_figs(-0.987, 1)
        '$-1 \\times 10^{0}$'
        >>> set_sig_figs(149, 2)
        '$1.5 \\times 10^{2}$'
        >>> set_sig_figs(150, 3)
        '$1.50 \\times 10^{2}$'
    """
    if n_sig_figs < 1:
        raise ValueError(
            f"Number of significant figures (n_sig_figs) must be >= 1, received {n_sig_figs}."
        )
    x = f"{x:.{n_sig_figs-1}e}"
    exponent = x.split("e")[1]
    exponent_sign = "" if int(exponent) >= 0 else "-"
    return rf"${x.split('e')[0]} \times 10^{{{exponent_sign}{abs(int(exponent)):d}}}$"


def robust_divide(
    dividend: np.ndarray,
    divisor: np.ndarray,
    neg_inf: float = -np.inf,
    pos_inf: float = np.inf,
    zero_div_zero: float = np.nan,
) -> np.ndarray:
    """Divide a dividend by a divisor, accounting for the scenarios where the divisor is 0.

    Args:
        dividend: Numerator of the division.
        divisor: Denominator of the division.
        neg_inf: Value to return if the divisor is 0 but the dividend is negative. Defaults to
            :code:`-np.inf`.
        pos_inf: Value to return if the divisor is 0 but the dividend is positive. Defaults to
            :code:`np.inf`.
        zero_div_zero: Value to return if both the dividend and the divisor are 0. Defaults to
            :code:`np.nan`.

    Raises:
        ValueError: If the divdend and the divisor are of different shapes.

    Returns:
        Division robust to the divisor being 0.

    Examples:
        >>> robust_divide(np.array([1, -1, 1, 0, 0]), np.array([2, 0, 0, 1, 0]))
        array([ 0.5, -inf,  inf,  0. ,  nan])
        >>> robust_divide(
        ...     np.array([[1, -1, 1], [0, 0, 1]]),
        ...     np.array([[2, 0, 0], [1, 0, 4]]),
        ...     neg_inf=-1/5,
        ...     pos_inf=7,
        ...     zero_div_zero=42,
        ... )
        array([[ 0.5 , -0.2 ,  7.  ],
               [ 0.  , 42.  ,  0.25]])
    """
    if dividend.shape != divisor.shape:
        raise ValueError("robust_divide does not yet broadcast arrays of different shapes.")
    division = np.where(
        divisor != 0,
        np.divide(dividend, divisor, where=divisor != 0),
        np.where(dividend < 0, neg_inf, np.where(dividend > 0, pos_inf, zero_div_zero)),
    )
    return division


def around(x: float, n_decimals: int = 0) -> float:
    """Round a number to a given number of decimal places.

    Args:
        x: Number to round.
        n_decimals: Number of decimal places to round to. Negative numbers refer to places to the
            left of the decimal point. Defaults to 0.

    Returns:
        Rounded number.

    The purpose of this function is to fix `numpy's around <https://numpy.org/doc/stable/reference/g
    enerated/numpy.around.html>`_ 'round half to even' behaviour such as:

        >>> np.around(0.5)
        0.0
        >>> np.around(1.5)
        2.0

    This fix, which is more suited to rounding individual numbers rather than many for statistical
    purposes, has the following beahviours:

        >>> around(0.5)
        1.0
        >>> around(1.5)
        2.0
        >>> around(-0.15, 1)
        -0.1
        >>> around(10.34, 1)
        10.3
        >>> around(1378, -2)
        1400.0
        >>> around(499, -1)
        500.0
    """
    exponent = 10 ** n_decimals
    return np.floor(x * exponent + 0.5) / exponent
