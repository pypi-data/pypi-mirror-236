"""
Utils Module

    This module implements functions and/or classes that help training neural
    networks, but do not have a specific definition.
"""

import math
from typing import Iterable, Tuple

import numpy as np


def batch_sequential(
    x: np.ndarray, y: np.ndarray, batch_size: int | None = None
) -> Iterable[Tuple[np.ndarray, np.ndarray]]:
    """
    Generate batches of data sequentially.

    Args:
        x (np.ndarray): Input data.
        y (np.ndarray): Target data.
        batch_size (int, optional): Size of each batch (defaults to None).

    Yields:
        Iterable[Tuple[np.ndarray, np.ndarray]]: A tuple of input and target data
        for each batch.
    """
    batch_size = x.shape[0] if batch_size is None else batch_size
    n_batches = math.ceil(x.shape[0] / batch_size)

    for i in range(n_batches):
        offset = batch_size * i
        x_batch = x[offset: offset + batch_size]
        y_batch = y[offset: offset + batch_size]
        yield x_batch, y_batch


def batch_shuffle(
    x: np.ndarray, y: np.ndarray, batch_size: int | None = None
) -> Iterable[Tuple[np.ndarray, np.ndarray]]:
    """
    Generate batches of shuffled data.

    Args:
        x (np.ndarray): Input data.
        y (np.ndarray): Target data.
        batch_size (int, optional): Size of each batch (defaults to None).

    Yields:
        Iterable[Tuple[np.ndarray, np.ndarray]]: A tuple of input and target data
        for each batch.
    """
    shuffle_index = np.random.permutation(range(x.shape[0]))
    return batch_sequential(x[shuffle_index], y[shuffle_index], batch_size)
