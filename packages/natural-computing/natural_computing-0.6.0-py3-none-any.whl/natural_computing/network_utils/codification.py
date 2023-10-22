"""
Codification Module

    This module provides functions for unpacking and packing neural network
    weights.
"""

from typing import Any, Dict, List, Tuple

import numpy as np

from .factories import LayerFactory
from natural_computing.neural_network import NeuralNetwork


def unpack_network(
    model: NeuralNetwork,
) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
    """
    Unpack the weights and layer configurations of a neural network model.

    Args:
        model (NeuralNetwork): The neural network model to be unpacked.

    Returns:
        Tuple[np.ndarray, List[Dict[str, Any]]]: A tuple containing the
            concatenated weights
        as a numpy array and a list of dictionaries describing the layer
            configurations.
    """
    weights, decode_guide = [], []

    # unpack all layers
    for layer in model._layers:
        weights.append(layer._weights.reshape(-1, 1))
        weights.append(layer._biases.reshape(-1, 1))
        decode_guide.append(
            {
                'weights_shape': layer._weights.shape,
                'biases_shape': layer._biases.shape,
                'activation': layer._activation,
            }
        )

    return np.concatenate(weights), decode_guide


def pack_network(
    weights_vector: np.ndarray, decode_guide: List[Dict[str, Any]]
) -> NeuralNetwork:
    """
    Pack weights and layer configurations into a neural network model.

    Args:
        weights_vector (np.ndarray): The concatenated weights as a numpy array.
        decode_guide (List[Dict[str, Any]]): A list of dictionaries describing
            the layer configurations.

    Returns:
        NeuralNetwork: A neural network model with weights and layer
            configurations.
    """
    module = NeuralNetwork(0)

    for layer in decode_guide:
        x, y = layer['weights_shape']
        a, b = layer['biases_shape']

        # unpack weights
        weights = weights_vector[: x * y].reshape((x, y))
        weights_vector = weights_vector[x * y:]

        # unpack biases
        biases = weights_vector[: a * b].reshape((a, b))
        weights_vector = weights_vector[a * b:]

        # add layer to network
        activation = layer['activation'].__name__
        module.add_layer(
            LayerFactory.dense_layer(
                weights.shape[1], weights.shape[0], activation=activation
            )
        )

        # change weights
        module._layers[-1]._weights = weights
        module._layers[-1]._biases = biases

    return module
