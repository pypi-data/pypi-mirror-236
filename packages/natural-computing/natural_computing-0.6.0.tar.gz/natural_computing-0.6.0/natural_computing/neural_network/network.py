"""
Neural Network Module

    This module implements a Multi-Layer Perceptron with backpropagation for
    weight optimization.
"""

from __future__ import annotations
from copy import deepcopy
import pickle
from itertools import zip_longest
from typing import Callable, Iterable, List, Tuple, Union

import numpy as np

from .layers import Dense
from .loss_functions import mse
from .regularization import (
    batch_normalization_backward,
    batch_normalization_forward,
    learning_rate_no_decay,
)
from .utils import batch_sequential

# type hinting for functions
loss_fn = Callable[[np.ndarray, np.ndarray], np.ndarray]
lr_decay_fn = Callable[[float, int, float, int], int]
batch_generator_fn = Iterable[Tuple[np.ndarray, np.ndarray]]


class NeuralNetwork:
    def __init__(
        self,
        learning_rate: float,
        lr_decay_fn: lr_decay_fn = learning_rate_no_decay,
        lr_decay_rate: float = 0.0,
        lr_decay_steps: int = 1,
        loss_function: loss_fn = mse,
        momentum: float = 0.0,
        patience: int | float = float('inf'),
    ) -> None:
        """
        Initialize a neural network.

        Args:
            learning_rate (float): Learning rate for training.

            lr_decay_fn (lr_decay_fn, optional):
                Learning rate decay function (defaults to learning rate
                no decay).

            lr_decay_rate (float, optional):
                Learning rate decay rate (defaults to 0.0).

            lr_decay_steps (int, optional):
                Number of steps for learning rate decay (defaults to 1).

            loss_function (loss_fn): Loss function used for
                training (defaults to the mean squared error (MSE)).

            momentum (float, optional):
                Momentum for optimizing the training process (defaults to 0.0).

            patience (int | float, optional):
                Patience for early stopping during training (defaults to
                infinity (no early stopping)).

        Returns:
            None
        """
        self._layers: List[Dense] = []
        self._learning_rate = learning_rate
        self._lr_decay_fn = lr_decay_fn
        self._lr_decay_rate = lr_decay_rate
        self._lr_decay_steps = lr_decay_steps
        self._loss_function = loss_function
        self._momentum = momentum
        self._patience = patience
        self._waiting = 0
        self._best_loss = float('inf')
        self._best_model: List[Dense]

    def add_layer(self, layer: Dense | List[Dense]) -> None:
        """
        Add a Dense layer to the neural network.

        Args:
            layer (Dense | List[Dense]): The Dense layer, or list of
                Dense Layers, to be added to the network.

        Returns:
            None
        """
        if isinstance(layer, Dense):
            self._layers.append(layer)
        else:
            self._layers.extend(layer)

    def save(self, file_path: str) -> None:
        """
        Save the neural network to a file using pickle.

        Args:
            file_path (str): The file path where the network will be saved.

        Returns:
            None
        """
        pickle.dump(self, open(file_path, 'wb'), -1)

    @staticmethod
    def load(file_path: str) -> NeuralNetwork:
        """
        Load a neural network from a saved file using pickle.

        Args:
            file_path (str): The file path from which the network will be
            loaded.

        Returns:
            NeuralNetwork: The loaded neural network.
        """
        return pickle.load(open(file_path, 'rb'))

    def fit(
        self,
        x_train: np.ndarray,
        y_train: np.ndarray,
        x_val: Union[np.ndarray, None] = None,
        y_val: Union[np.ndarray, None] = None,
        epochs: int = 100,
        batch_generator: batch_generator_fn = batch_sequential,
        batch_size: int | None = None,
        verbose: int = 10,
    ) -> None:
        """
        Train the neural network.

        Args:
            x_train (np.ndarray): Input training data.

            y_train (np.ndarray): Target training data.

            x_val (np.ndarray | None, optional):
                Input validation data (defaults to None (no validation set)).

            y_val (np.ndarray | None, optional):
                Target validation data (defaults to None (no validation set)).

            epochs (int, optional): Number of training epochs
                (defaults to 100).

            verbose (int, optional): Frequency of progress updates
                (defaults to 10).

            batch_generator (batch_generator_fn): Batch generator function to
                use for training (defaults to batch_sequential).

            batch_size (int | None, optional): Size of each batch (defaults to
                None).

        Returns:
            None
        """
        # saves initial learning rate for restoration after fit
        learning_rate = self._learning_rate

        # initial settings for patience to work
        self._best_model = deepcopy(self._layers)
        self._best_loss = float('inf')

        # update x_val and y_val
        if x_val is None or y_val is None:
            print(
                '* The X_val or Y_val set was not informed, '
                'the training sets will be used'
            )
            x_val, y_val = x_train, y_train

        for epoch in range(epochs):
            self._learning_rate = self._lr_decay_fn(
                learning_rate,
                epoch,
                self._lr_decay_rate,
                self._lr_decay_steps,
            )
            batches = batch_generator(x_train, y_train, batch_size)

            for x_batch, y_batch in batches:
                y_pred = self.__feedforward(x_batch)
                self.__backpropagation(y_batch, y_pred)

            # check early stop
            loss_val = self._loss_function(y_val, self.predict(x_val))

            if loss_val < self._best_loss:
                self._best_model = deepcopy(self._layers)
                self._best_loss, self._waiting = loss_val, 0
            else:
                self._waiting += 1

                if self._waiting >= self._patience:
                    print(f'* early stopping at epoch {epoch + 1}')
                    self._layers = self._best_model
                    break

            # print loss
            if (epoch + 1) % verbose == 0:
                # compute regularization loss
                loss_reg = (1.0 / y_train.shape[0]) * np.sum(
                    [
                        layer._regularization_strength
                        * layer._regularization(layer._weights)
                        for layer in self._layers
                    ]
                )

                # compute train loss
                loss_train = self._loss_function(
                    y_train, self.predict(x_train)
                )

                # get information to format output
                d_length = len(str(epochs))

                print(
                    f'epoch: {epoch + 1:{d_length}d}/{epochs:{d_length}d} | '
                    f'loss train: {loss_train:.4f} | '
                    f'loss reg.: {loss_reg:.4f} | '
                    f'sum: {loss_train + loss_reg:.4f} '
                )

        # restore initial settings
        self._learning_rate = learning_rate

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Make predictions using the trained neural network.

        Args:
            x (np.ndarray): Input data.

        Returns:
            np.ndarray: Predicted output.
        """
        return self.__feedforward(x, training=False)

    def __feedforward(
        self, x: np.ndarray, training: bool = True
    ) -> np.ndarray:
        """
        Perform the feedforward pass through the Dense layer.

        Args:
            x (np.ndarray): Input data.

            training (bool, optional): Indicates whether the feedforward
                pass is performed during training (defaults to True).

        Returns:
            np.ndarray: Output of the feedforward pass.
        """
        self._layers[0]._input = x
        layer_pairs = zip_longest(self._layers, self._layers[1:])

        # process each layer
        for cur_layer, next_layer in layer_pairs:
            y = cur_layer._input.dot(cur_layer._weights.T) + cur_layer._biases

            # apply batch normalization
            if cur_layer._batch_norm:
                y = batch_normalization_forward(cur_layer, y, training)

            # dropout mask
            cur_layer._dropout_mask = np.random.binomial(
                1, 1.0 - cur_layer._dropout_probability, y.shape
            ) / (1.0 - cur_layer._dropout_probability)

            # save values
            cur_layer._activation_input = y
            cur_layer._activation_output = cur_layer._activation(y) * (
                cur_layer._dropout_mask if training else 1.0
            )

            if next_layer:
                next_layer._input = cur_layer._activation_output

        return self._layers[-1]._activation_output

    def __backpropagation(self, y: np.ndarray, y_pred: np.ndarray) -> None:
        """
        Perform the backpropagation algorithm to update weights and biases.

        Args:
            y (np.ndarray): Target values.
            y_pred (np.ndarray): Predicted values.

        Returns:
            None
        """
        last_delta = self._loss_function(y, y_pred, derivative=True)

        # calculate in reverse
        for layer in reversed(self._layers):
            dactivation = (
                layer._activation(layer._activation_input, derivative=True)
                * last_delta
                * layer._dropout_mask
            )

            # compute derivation for batch normalization
            if layer._batch_norm:
                dactivation = batch_normalization_backward(layer, dactivation)

            last_delta = dactivation.dot(layer._weights)
            layer._dweights = dactivation.T.dot(layer._input)
            layer._dbias = 1.0 * dactivation.sum(axis=0, keepdims=True)

        for layer in reversed(self._layers):
            # apply regularization
            layer._dweights = layer._dweights + (
                1.0 / y.shape[0]
            ) * layer._regularization_strength * layer._regularization(
                layer._weights, derivative=True
            )

            # apply momentum
            layer._prev_dweights = (
                -self._learning_rate * layer._dweights
                + self._momentum * layer._prev_dweights
            )

            # update weights and biases
            layer._weights = layer._weights + layer._prev_dweights
            layer._biases = layer._biases - self._learning_rate * layer._dbias

            # update batch normalization
            if layer._batch_norm:
                layer._beta = layer._beta - self._learning_rate * layer._dbeta
                layer._gamma = (
                    layer._gamma - self._learning_rate * layer._dgamma
                )
