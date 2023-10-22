"""Facilitate reproduction of random events."""

import random

import numpy as np
import torch


def set_random_seed(seed: int) -> None:
    """Set the random seed for all of the random, NumPy, and PyTorch packages.

    Args:
        seed: Random seed.

    Examples:
        >>> set_random_seed(42)
        >>> random.randint(0, 10000)
        1824
        >>> np.random.randint(0, 10000)
        7270
        >>> torch.randint(0, 10000, (1,)).item()
        7542
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
