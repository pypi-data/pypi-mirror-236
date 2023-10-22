"""Function tools for scihence."""
from functools import partial, wraps

WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__', '__doc__')

wraps_without_annotations = partial(wraps, assigned=WRAPPER_ASSIGNMENTS)
"""`functools.wraps`_ but maintain the annotations of the wrapper function.

.. _functools.wraps:: https://docs.python.org/3/library/functools.html#functools.wraps
"""
