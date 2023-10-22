"""Scihence's AI data utilities."""
import numpy as np


def get_batches(n_instances: int, batch_size: int = 0, shuffle: bool = False) -> list[np.ndarray]:
    """Get batch indices for a given number of instances.

    Args:
        n_instances: Number of instances to create batches for.
        batch_size: Size of each batch. The last one could be smaller to cover all of the instances.
            Defaults to :code:`0`.
        shuffle: Whether to randomise the order of the instances. Defaults to :code:`False`.

    Returns:
        List of arrays where array :math:`n` contains the indices to be used in the :math:`n^{th}`
        batch.
    """
    idxs = np.arange(n_instances)
    batch_size, batches = n_instances if batch_size <= 0 else batch_size, []
    if shuffle:
        np.random.shuffle(idxs)
    batches = []
    for i in range(int(np.ceil(n_instances / batch_size))):
        batches.append(idxs[int(i * batch_size) : int(min((i + 1) * batch_size, n_instances))])
    return batches
