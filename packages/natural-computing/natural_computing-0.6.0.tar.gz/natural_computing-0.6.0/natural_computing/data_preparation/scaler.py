"""
Scaler Module

This module provides classes for scaling data.
"""

import numpy as np


class StandardScaler:
    """
    StandardScaler scales data to have a mean of 0 and a standard deviation of
    1.

    Args:
        centered_on_zero (bool, optional): If True, the data is centered
        around zero after scaling (default is True).

    Attributes:
        _mean (float): The mean value of the fitted data.
        _std (float): The standard deviation of the fitted data.
        _fitted (bool): A flag indicating whether the scaler has been fitted.

    Methods:
        fit(x: np.ndarray) -> None: Compute the mean and standard deviation
            of the input data.
        transform(x: np.ndarray) -> np.ndarray: Scale the input data using the
            computed mean and standard deviation.
        fit_transform(x: np.ndarray) -> np.ndarray: Fit the scaler to the
            input data and then scale the data.

    """

    def __init__(self) -> None:
        self._mean = 0
        self._std = 0
        self._fitted = False

    def fit(self, x: np.ndarray) -> None:
        """
        Compute the mean and standard deviation of the input data.

        Args:
            x (np.ndarray): The input data to be fitted.

        Returns:
            None: The scaler object is updated with the computed mean and
                standard deviation.
        """
        self._mean = np.mean(x)
        self._std = np.std(x)
        self._fitted = True

    def transform(self, x: np.ndarray) -> np.ndarray:
        """
        Scale the input data using the computed mean and standard deviation.

        Args:
            x (np.ndarray): The input data to be scaled.

        Returns:
            np.ndarray: The scaled data.
        """
        x_transformed = (x - self._mean) / self._std

        return x_transformed

    def fit_transform(self, x: np.ndarray) -> np.ndarray:
        """
        Fit the scaler to the input data and then scale the data.

        Args:
            x (np.ndarray): The input data to be fitted and scaled.

        Returns:
            np.ndarray: The fitted and scaled data.
        """
        self.fit(x)
        return self.transform(x)


class MinMaxScaler:
    """
    MinMaxScaler scales data to the range [0, 1] or [-1, 1] if
        centered_on_zero is false.

    Args:
        centered_on_zero (bool, optional): If True, the scaled data is
            centered around zero after scaling (default is True).

    Attributes:
        _min (float): The minimum value of the fitted data.
        _max (float): The maximum value of the fitted data.
        _fitted (bool): A flag indicating whether the scaler has been fitted.
        _centered_on_zero (bool): A flag that indicates whether the data is
            zero-centered, otherwise the data is set to [-1, 1].

    Methods:
        fit(x: np.ndarray) -> None: Compute the minimum and maximum values of
            the input data.
        transform(x: np.ndarray) -> np.ndarray: Scale the input data to
            the range [0, 1].
        fit_transform(x: np.ndarray) -> np.ndarray: Fit the scaler to the
            input data and then scale the data.

    """

    def __init__(self, centered_on_zero: bool = True) -> None:
        self._min = 0
        self._max = 0
        self._fitted = False
        self._centered_on_zero = centered_on_zero

    def fit(self, x: np.ndarray) -> None:
        """
        Compute the minimum and maximum values of the input data.

        Args:
            x (np.ndarray): The input data to be fitted.

        Returns:
            None: The scaler object is updated with the computed minimum and
                maximum values.
        """
        self._min = np.min(x)
        self._max = np.max(x)
        self._fitted = True

    def transform(self, x: np.ndarray) -> np.ndarray:
        """
        Scale the input data to the range [0, 1] or [-1, 1] if
        centered_on_zero is false.

        Args:
            x (np.ndarray): The input data to be scaled.

        Returns:
            np.ndarray: The scaled data in the range [0, 1] or [-1, 1].
        """
        x_transformed = (x - self._min) / (self._max - self._min)

        if not self._centered_on_zero:
            x_transformed = 2 * x_transformed - 1

        return x_transformed

    def fit_transform(self, x: np.ndarray) -> np.ndarray:
        """
        Fit the scaler to the input data and then scale the data.

        Args:
            x (np.ndarray): The input data to be fitted and scaled.

        Returns:
            np.ndarray: The fitted and scaled data.
        """
        self.fit(x)
        return self.transform(x)
