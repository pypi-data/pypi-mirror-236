"""
Objective Functions Module

    This module provides objective functions for neural network
    training with optimization algorithms.
"""

import numpy as np
from typing import List, Tuple

from .codification import pack_network
from natural_computing.objective_functions import BaseFunction


class RootMeanSquaredErrorForNN(BaseFunction):
    """
    Root Mean Squared Error (RMSE) objective function for neural network
    training with optimization algorithms.

    Args:
        x_data (np.ndarray): The input data.
        y_data (np.ndarray): The target data.
        decode_guide (List[Tuple[int, int]]): A list of tuples specifying the
            layer dimensions for decoding network weights.
        l2_regularization (float, optional): L2 regularization strength
            (default is 0.0).

    Attributes:
        _x_data (np.ndarray): The input data.
        _y_data (np.ndarray): The target data.
        _decode_guide (List[Tuple[int, int]]): A list of tuples specifying the
            layer dimensions for decoding network weights.
        _l2_regularization (float): L2 regularization strength.

    Methods:
        evaluate(nn_weights: List[float]) -> float: Evaluate the RMSE for a
            given set of network weights.

    """

    def __init__(
        self,
        x_data: np.ndarray,
        y_data: np.ndarray,
        decode_guide: List[Tuple[int, int]],
        l2_regularization: float = 0.0,
    ):
        super().__init__()
        self._x_data = x_data
        self._y_data = y_data
        self._decode_guide = decode_guide
        self._l2_regularization = l2_regularization

    def evaluate(self, nn_weights: List[float]) -> float:
        """
        Evaluate the Root Mean Squared Error (RMSE) for a given set of network
            weights.

        Args:
            nn_weights (List[float]): A list of network weights.

        Returns:
            float: The RMSE value or 'inf' if a RuntimeWarning (e.g., overflow
                encountered in exp) occurs.

        Note:
            - The function decodes the network weights into a neural network.
            - It computes the RMSE between the predictions of the neural
                network and the target data.
            - L2 regularization is applied to the network weights.
        """
        # Decode network
        nn_weights = np.array(nn_weights).reshape(-1, 1)
        nn = pack_network(nn_weights, self._decode_guide)

        with np.errstate(all='raise'):
            try:
                y_pred = nn.predict(self._x_data)
            except FloatingPointError:
                return float('inf')

        # Compute error
        error = np.sqrt(np.mean((y_pred - self._y_data) ** 2))
        weights = [layer._weights.squeeze()**2 for layer in nn._layers]
        error += self._l2_regularization * np.sum([w.sum() for w in weights])

        return error
