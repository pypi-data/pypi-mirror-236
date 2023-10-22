"""
activation_functions.py - Activation functions for  simple neural networks

    This module provides some activation functions for use with implementing
    neural networks.
"""

import numpy as np


def sigmoid(x: np.ndarray, derivative: bool = False) -> np.ndarray:
    """
    Passes the vector through the sigmoid function. If the derivative value is
    true, pass the value through the derivative of the sigmoid function.

    Args:
        x (np.ndarray): Input vector.
        derivative (bool): indicates whether you want to go through the
            derivative (default is False).

    Returns:
        np.ndarray of values ​​passed by the sigmoid function.
    """
    sigma = 1 / (1.0 + np.exp(-x))
    return sigma * (1 - sigma) if derivative else sigma


def tanh(x: np.ndarray, derivative: bool = False) -> np.ndarray:
    """
    Apply the hyperbolic tangent (tanh) function to an input array.

    Args:
        x (np.ndarray): Input array.
        derivative (bool, optional): Indicates whether you want to compute the
        derivative (defaults to False).

    Returns:
        np.ndarray: Output array after applying the tanh function or its
        derivative if derivative is True.
    """
    if derivative:
        return 1 - tanh(x) ** 2
    return (np.exp(x) - np.exp(-x)) / ((np.exp(x) + np.exp(-x)))


def linear(x: np.ndarray, derivative: bool = False) -> np.ndarray:
    """
    Apply the linear function to an input array.

    Args:
        x (np.ndarray): Input array.
        derivative (bool, optional): Indicates whether you want to compute the
            derivative (defaults to False).

    Returns:
        np.ndarray: Output array after applying the linear function or its
            derivative if derivative is True.
    """
    return np.ones_like(x) if derivative else x


def relu(x: np.ndarray, derivative: bool = False) -> np.ndarray:
    """
    Apply the Rectified Linear Unit (ReLU) function to an input array.

    Args:
        x (np.ndarray): Input array.
        derivative (bool, optional): Indicates whether you want to compute the
            derivative (defaults to False).

    Returns:
        np.ndarray: Output array after applying the ReLU function or its
            derivative if derivative is True.
    """
    if derivative:
        return np.where(x <= 0, 0, 1)
    return np.maximum(0, x)
