"""
Factories Module

    This module implement some classes using factory design pattern
    to improve the usability of the entire code.
"""

from typing import Any

from natural_computing.neural_network import (
    Dense,
    l1_regularization,
    l2_regularization,
    linear,
    relu,
    sigmoid,
    tanh,
)

from natural_computing.utils import (
    glorot_normal_initializer,
    glorot_uniform_initializer,
    ones_initializer,
    random_uniform_initializer,
    zeros_initializer,
)

activation_functions = {
    'linear': linear,
    'sigmoid': sigmoid,
    'tanh': tanh,
    'relu': relu,
}

initializer_functions = {
    'glorot_normal': glorot_normal_initializer,
    'glorot_uniform': glorot_uniform_initializer,
    'random_uniform': random_uniform_initializer,
    'ones': ones_initializer,
    'zeros': zeros_initializer,
}

regularization_functions = {
    'l1': l1_regularization,
    'l2': l2_regularization,
}


def check_parameter(
    param: Any, default: Any, error_msg: str
) -> None:  # type: ignore[misc] # noqa: F821
    """
    Check if a parameter is None and provide a default value.

    Args:
        param (Any): The parameter to check.
        default (Any): The default value to use if param is None.
        error_msg (str): The error message to display if using the default.

    Returns:
        None: The parameter value or the default value if param is None.
    """
    if param is None:
        print(
            f"* The param {error_msg} don't exists, "
            f'using the {default.__name__} instead.'
        )
        return default
    return param


class LayerFactory:
    """Factory for creating Neural Network Layer."""

    @staticmethod
    def dense_layer(
        input_size: int,
        output_size: int,
        activation: str = 'linear',
        weights_initializer: str = 'glorot_uniform',
        biases_initializer: str = 'zeros',
        regularization: str = 'l2',
        regularization_strength: float = 0.0,
        dropout_probability: float = 0.0,
        batch_normalization: bool = False,
        batch_normalization_decay: float = 0.9,
    ) -> Dense:
        """
        Create a custom Dense object with user-defined configurations.

        Args:
            input_size (int): The size of the input layer.

            output_size (int): The size of the output layer.

            activation (str): The name of the activation function.

            weights_initializer (str): The name of the weights initializer
                function.

            biases_initializer (str): The name of the biases initializer
                function.

            regularization (str): The name of the regularization function.

            regularization_strength (float, optional):
                Strength of the regularization term (defaults to 0.0).

            dropout_probability (float): The dropout probability
                (default is 0.0).

            batch_normalization (bool, optional):
                Whether to apply batch normalization (defaults to False).

            batch_normalization_decay (float, optional):
                Decay rate for batch normalization (defaults to 0.9).

        Returns:
            Dense: A custom Dense layer with the specified configurations.
        """

        # get values from dicts
        activation_fn = activation_functions.get(activation, None)
        weights_fn = initializer_functions.get(weights_initializer, None)
        biases_fn = initializer_functions.get(biases_initializer, None)
        regularization_fn = regularization_functions.get(regularization, None)

        # check all values
        activation_fn = check_parameter(
            activation_fn, linear, 'activation function'
        )
        biases_fn = check_parameter(
            biases_fn, zeros_initializer, 'bias initializer'
        )
        weights_fn = check_parameter(
            weights_fn, glorot_uniform_initializer, 'weights initializer'
        )
        regularization_fn = check_parameter(
            regularization_fn, l2_regularization, 'regularization method'
        )

        return Dense(
            input_size=input_size,
            output_size=output_size,
            activation=activation_fn,
            weights_initializer=weights_fn,
            biases_initializer=biases_fn,
            regularization=regularization_fn,
            regularization_strength=regularization_strength,
            dropout_probability=dropout_probability,
            batch_norm=batch_normalization,
            batch_decay=batch_normalization_decay,
        )
