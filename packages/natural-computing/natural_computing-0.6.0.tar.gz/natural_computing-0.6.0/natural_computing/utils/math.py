"""
math.py - Math Operations Utilities

    This module provides utility functions for math operations.
"""

import random
from operator import add, sub
from typing import List, Tuple

import numpy as np


def sum_lists(list_0: List[float], list_1: List[float]) -> List[float]:
    """
    Add corresponding elements of two lists.

    Args:
        list_0 (List[float]): The first input list.
        list_1 (List[float]): The second input list.

    Returns:
        List[float]: A list containing the element-wise sum.
    """
    return list(map(add, list_0, list_1))


def sub_lists(list_0: List[float], list_1: List[float]) -> List[float]:
    """
    Subtract corresponding elements of two lists.

    Args:
        list_0 (List[float]): The first input list.
        list_1 (List[float]): The second input list.

    Returns:
        List[float]: A list containing the element-wise subtraction.
    """
    return list(map(sub, list_0, list_1))


def mul_list(constant: float, list_0: List[float]) -> List[float]:
    """
      Multiply each element in the list by the constant value.

      Args:
          constant (Number): The constant value to multiply.
          list_0 (List[float]): The input list.

    Returns:
          List[float]: A list containing the element-wise subtraction.
    """
    return list(map(lambda x: constant * x, list_0))


def bounded_random_vectors(bounds: List[Tuple[float, float]]) -> List[float]:
    """
    Create a random vector with dimension equal to the length of the list.

    Each component in the list
    is limited by the corresponding index tuple, that is, the first generated
    number is limited with the values ​​of the first tuple in the list, the
    second value generated is limited by the second tuple.

    Args:
        bounds (List[Tuple[float, float]]): List of tuples where each tuple
            represents the bounds for a component of the vector.

    Returns:
        List[float]: Vector of random numbers respecting the bounds.
    """
    return [
        random.random() * (max_val - min_val) + min_val
        for min_val, max_val in bounds
    ]


def argsort(list: List[float]) -> List[int]:
    """
    Returns a list with the index in ascending order of value.

    Args:
        bounds (List[Tuple[Number, Number]]): List of tuples where each tuple
            represents the bounds for a component of the vector.

    Returns:
        List[int]: List of ordered value indices.
    """
    return sorted(range(len(list)), key=list.__getitem__)


def zeros_initializer(rows: int, cols: int) -> np.ndarray:
    """
    Initialize weights with zeros.

    Args:
        rows (int): Number of rows in the weight matrix.
        cols (int): Number of columns in the weight matrix.

    Returns:
        np.ndarray: Weight matrix filled with zeros.
    """
    return np.zeros((rows, cols))


def ones_initializer(rows: int, cols: int) -> np.ndarray:
    """
    Initialize weights with ones.

    Args:
        rows (int): Number of rows in the weight matrix.
        cols (int): Number of columns in the weight matrix.

    Returns:
        np.ndarray: Weight matrix filled with ones.
    """
    return np.ones((rows, cols))


def random_uniform_initializer(rows: int, cols: int) -> np.ndarray:
    """
    Initialize weights with random values from a standard normal distribution.

    Args:
        rows (int): Number of rows in the weight matrix.
        cols (int): Number of columns in the weight matrix.

    Returns:
        np.ndarray: Weight matrix with random values.
    """
    return np.random.randn(rows, cols)


def glorot_normal_initializer(rows: int, cols: int) -> np.ndarray:
    """
    Initialize weights using Glorot normal initialization (Xavier
        initialization).

    Args:
        rows (int): Number of rows in the weight matrix.
        cols (int): Number of columns in the weight matrix.

    Returns:
        np.ndarray: Weight matrix initialized with Glorot normal values.
    """
    std_dev = np.sqrt(2.0 / (rows + cols))
    return std_dev * np.random.randn(rows, cols)


def glorot_uniform_initializer(rows: int, cols: int) -> np.ndarray:
    """
    Initialize weights using Glorot uniform initialization.

    Args:
        rows (int): Number of rows in the weight matrix.
        cols (int): Number of columns in the weight matrix.

    Returns:
        np.ndarray: Weight matrix initialized with Glorot uniform values.
    """
    limit = np.sqrt(6.0 / (rows + cols))
    return 2 * limit * np.random.randn(rows, cols) - limit


def r2_score(y_true, y_pred):
    """
    Calculate the R-squared (R2) score for a regression model.

    R-squared is a statistical measure that represents the proportion
    of the variance in the dependent variable that is explained by the
    independent variables in a regression model. It provides an indication
    of the goodness of fit of the model.

    Args:
        y_true (numpy.ndarray): The true target values (ground truth).
        y_pred (numpy.ndarray): The predicted target values.

    Returns:
        float: The R-squared (R2) score, which is a value between 0 and 1.
            A higher R2 score indicates a better fit of the model to the data.
    """
    ssr = np.sum((y_true - y_pred) ** 2)
    sst = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = 1 - (ssr / sst)

    return r2
