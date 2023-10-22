"""
loss_functions.py - Loss functions for  simple neural networks

    This module provides some loss functions for use with implementing
    neural networks.
"""

import numpy as np


def softmax(x: np.ndarray, derivative: bool = False) -> np.ndarray:
    """
    Passes the vector through the softmax function.

    Obs.: This implementation subtracts max(x) for numerical stability.

    Args:
        x (np.ndarray): Input vector.
        derivative (bool): indicates whether you want to go through the
            derivative (default is False).

    Returns:
        np.ndarray: Output vector after applying the softmax function.
    """
    e_x = np.exp(x - np.max(x))
    sum_e_x = e_x.sum(axis=1, keepdims=True)

    result = e_x / sum_e_x

    if derivative:
        result *= 1 - result

    return result


def neg_log_likelihood(
    y: np.ndarray,
    y_pred: np.ndarray,
    derivative: bool = False,
) -> np.ndarray:
    """
    Calculate the negative log-likelihood loss between predicted and true
    values.

    Args:
        y (np.ndarray): True values.
        y_pred (np.ndarray): Predicted values.
        derivative (bool, optional): Indicates whether you want to compute the
            derivative (default is False).

    Returns:
        np.ndarray: Negative log-likelihood loss or its derivative if
            derivative is True.
    """
    indices = np.nonzero(y_pred * y)
    values = y_pred[indices]

    if derivative:
        y_pred[indices] = -1.0 / values
        return y_pred

    return np.mean(-np.log(values))


def softmax_neg_log_likelihood(
    y: np.ndarray,
    y_pred: np.ndarray,
    derivative: bool = False,
) -> np.ndarray:
    """
    Calculate the softmax negative log-likelihood loss between predicted and
    true values.

    Args:
        y (np.ndarray): True values.
        y_pred (np.ndarray): Predicted values.
        derivative (bool, optional): Indicates whether you want to compute the
            derivative. Defaults to False.

    Returns:
        np.ndarray: Softmax negative log-likelihood loss or its derivative if
        derivative is True.
    """
    out = softmax(y_pred)

    if derivative:
        return -(y - out) / y.shape[0]

    return neg_log_likelihood(y, out)


def mae(y: np.ndarray, y_pred: np.ndarray, derivative=False) -> np.ndarray:
    """
    Calculate the Mean Absolute Error (MAE) between predicted and true values.

    Args:
        y (np.ndarray): True values.
        y_pred (np.ndarray): Predicted values.
        derivative (bool, optional): Indicates whether you want to compute the
            derivative (defaults to True).

    Returns:
        np.ndarray: MAE or its derivative if derivative is True.
    """
    if derivative:
        return np.where(y_pred > y, 1, -1) / y.shape[0]
    return np.mean(np.abs(y - y_pred))


def mse(y: np.ndarray, y_pred: np.ndarray, derivative=False) -> np.ndarray:
    """
    Calculate the Mean Squared Error (MSE) between predicted and true values.

    Args:
        y (np.ndarray): True values.
        y_pred (np.ndarray): Predicted values.
        derivative (bool, optional): Indicates whether you want to compute the
            derivative (defaults to True).

    Returns:
        np.ndarray: MSE or its derivative if derivative is True.
    """
    if derivative:
        return (y_pred - y) / y.shape[0]
    return 0.5 * np.mean((y - y_pred) ** 2)


def rmse(y: np.array, y_pred: np.array, derivative=False) -> np.array:
    """
    Calculate the Root Mean Squared Error (RMSE) between predicted and true
    values.

    Args:
        y (np.array): True values.
        y_pred (np.array): Predicted values.
        derivative (bool, optional): Indicates whether you want to compute the
            derivative (defaults to True).

    Returns:
        np.array: RMSE or its derivative if derivative is True.
    """
    difference = y - y_pred
    mse_value = np.sqrt(np.mean(difference ** 2))

    if derivative:
        return -difference/(y.shape[0] * mse_value)

    return mse_value
