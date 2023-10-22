"""
Layers Module

    This module implements layers used to compose the neural
    network implementation.
"""

from typing import Callable

import numpy as np

from natural_computing.utils import ones_initializer, zeros_initializer

weight_generator_fn = Callable[[int, int], np.ndarray]
regularization_fn = Callable[[np.ndarray, bool], np.ndarray]


class Dense:
    def __init__(
        self,
        input_size: int,
        output_size: int,
        activation: Callable[[np.ndarray, bool], np.ndarray],
        weights_initializer: weight_generator_fn,
        biases_initializer: weight_generator_fn,
        regularization: regularization_fn,
        regularization_strength: float = 0.0,
        dropout_probability: float = 0.0,
        batch_norm: bool = False,
        batch_decay: float = 0.9,
    ) -> None:
        """
        Implementation of a fully-connected layer.

        Args:
            input_size (int): Number of input neurons.

            output_size (int): Number of output neurons.

            activation (Callable[[np.ndarray, bool], np.ndarray], optional):
                Activation function to be used in the layer
                (defaults to linear).

            weights_initializer (weight_generator_fn, optional):
                Weight initialization function (defaults to glorot normal
                initializer).

            biases_initializer (weight_generator_fn, optional):
                Biases initialization function. Defaults to zeros_initializer.

            regularization (regularization_fn, optional):
                Regularization function to apply to the weights (defaults to
                l2_regularization).

            regularization_strength (float, optional):
                Strength of the regularization term (defaults to 0.0).

            dropout_probability (float, optional):
                Dropout probability for regularization (defaults to 0.0).

            batch_norm (bool, optional):
                Whether to apply batch normalization (defaults to False).

            batch_decay (float, optional):
                Decay rate for batch normalization (defaults to 0.9).
        """
        # params
        self._weights = weights_initializer(output_size, input_size)
        self._biases = biases_initializer(1, output_size)
        self._gamma = ones_initializer(1, output_size)
        self._beta = zeros_initializer(1, output_size)

        # hyper params
        self._activation = activation
        self._regularization = regularization
        self._regularization_strength = regularization_strength
        self._dropout_probability = dropout_probability
        self._batch_norm = batch_norm
        self._batch_decay = batch_decay

        # intermediary values
        self._input = None
        self._dropout_mask = None
        self._activation_input, self._activation_output = None, None
        self._dweights, self._dbiases = None, None
        self._dgamma, self._dbeta = None, None
        self._prev_dweights = 0.0
        self._population_mean = zeros_initializer(1, output_size)
        self._population_var = zeros_initializer(1, output_size)
        self._batch_norm_cache = None
