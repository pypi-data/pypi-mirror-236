"""
Regularization Module

    This module implements regularization techniques for use with the neural
    network implementation.
"""

import numpy as np

from .layers import Dense


def l1_regularization(
    weights: np.ndarray, derivative: bool = False
) -> np.ndarray:
    """
    Calculate L1 regularization for a set of weights.

    Args:
        weights (np.ndarray): Array of model weights.
        derivative (bool, optional): Indicates whether you want to compute the
            derivative (defaults to False).

    Returns:
        np.ndarray: L1 regularization term or its derivative if derivative is
            True.
    """
    if derivative:
        return np.array([np.where(w >= 0, 1, -1) for w in weights])
    return np.sum([np.sum(np.abs(w)) for w in weights])  # type: ignore


def l2_regularization(
    weights: np.ndarray, derivative: bool = False
) -> np.ndarray:
    """
    Calculate L2 regularization for a set of weights.

    Args:
        weights (np.ndarray): Array of model weights.
        derivative (bool, optional): Indicates whether you want to compute the
            derivative (defaults to False).

    Returns:
        np.ndarray: L2 regularization term or its derivative if derivative is
        True.
    """
    if derivative:
        return weights
    return 0.5 * np.sum(weights**2)  # type: ignore


def learning_rate_no_decay(
    learning_rate: float, epoch: int, decay_rate: float, decay_steps: int = 1
) -> float:
    """
    Learning rate scheduling with no decay.

    Args:
        learning_rate (float): Initial learning rate.
        epoch (int): Current epoch.
        decay_rate (float): Decay rate (not used in this function).
        decay_steps (int, optional): Number of steps for decay (not used in
            this function). Defaults to 1.

    Returns:
        float: Unchanged initial learning rate.
    """
    return learning_rate


def learning_rate_time_based_decay(
    learning_rate: float, epoch: int, decay_rate: float, decay_steps: int = 1
) -> float:
    """
    Learning rate scheduling with time-based decay.

    Args:
        learning_rate (float): Initial learning rate.
        epoch (int): Current epoch.
        decay_rate (float): Decay rate.
        decay_steps (int, optional): Number of steps for decay (not used in
            this function). Defaults to 1.

    Returns:
        float: Updated learning rate with time-based decay.
    """
    return learning_rate / (1 + decay_rate * epoch)


def learning_rate_exponential_decay(
    learning_rate: float, epoch: int, decay_rate: float, decay_steps: int = 1
) -> float:
    """
    Learning rate scheduling with exponential decay.

    Args:
        learning_rate (float): Initial learning rate.
        epoch (int): Current epoch.
        decay_rate (float): Decay rate.
        decay_steps (int, optional): Number of steps for decay (not used in
            this function) (defaults to 1).

    Returns:
        float: Updated learning rate with exponential decay.
    """
    return learning_rate * decay_rate**epoch


def learning_rate_staircase_decay(
    learning_rate: float, epoch: int, decay_rate: float, decay_steps: int = 1
) -> float:
    """
    Learning rate scheduling with staircase decay.

    Args:
        learning_rate (float): Initial learning rate.
        epoch (int): Current epoch.
        decay_rate (float): Decay rate.
        decay_steps (int, optional): Number of steps for decay (defaults to 1).

    Returns:
        float: Updated learning rate with staircase decay.
    """
    return learning_rate * decay_rate ** (epoch // decay_steps)


def batch_normalization_forward(
    layer: Dense, x: np.ndarray, training: bool = True
):
    """
    Perform batch normalization forward pass.

    Args:
        layer (Dense): The dense layer with batch normalization.

        x (np.ndarray): Input data.

        training (bool, optional): Flag indicating if it's during training
            (defaults to True).

    Returns:
        np.ndarray: Output data after batch normalization.
    """
    mu = np.mean(x, axis=0) if training else layer._population_mean
    var = np.var(x, axis=0) if training else layer._population_var
    x_norm = (x - mu) / np.sqrt(var + 1e-8)
    out = layer._gamma * x_norm + layer._beta

    if training:
        # mean average
        layer._population_mean = (
            layer._batch_decay * layer._population_mean
            + (1 - layer._batch_decay) * mu
        )
        # mean var
        layer._population_var = (
            layer._batch_decay * layer._population_var
            + (1 - layer._batch_decay) * var
        )
        # update batch norm cache
        layer._batch_norm_cache = (x, x_norm, mu, var)

    return out


def batch_normalization_backward(
    layer: Dense, dactivation: np.ndarray
) -> np.ndarray:
    """
    Perform batch normalization backward pass.

    Args:
        layer (Dense): The dense layer with batch normalization.

        dactivation (np.ndarray): Gradient of the activation.

    Returns:
        np.ndarray: Gradient with respect to the input data.
    """
    # extract cached values from the layer, and batch size from input
    x, x_norm, mu, var = layer._batch_norm_cache
    m = layer._activation_input.shape[0]

    # compute gradients
    x_mu = x - mu
    std_inv = 1.0 / np.sqrt(var + 1e-8)
    dx_norm = dactivation * layer._gamma
    dvar = np.sum(dx_norm * x_mu, axis=0) * -0.5 * (std_inv**3)
    dmu = np.sum(dx_norm * -std_inv, axis=0) + dvar * np.sum(-2 * x_mu, axis=0)
    dx = (dx_norm * std_inv) + (dvar * 2 * x_mu / m) + (dmu / m)
    layer._dgamma = np.sum(dactivation * x_norm, axis=0)
    layer._dbeta = np.sum(dactivation, axis=0)

    return dx
