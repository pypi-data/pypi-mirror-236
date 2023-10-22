"""
Polynomial Module
    This module implements commonly used difference functions to optimize
    polynomial problems.

Classes:
    SquaredError: The implementation of the squared error function.
"""

from typing import List

from .base_function import BaseFunction


class SquaredError(BaseFunction):
    """
    Squared error function implementation.

    Args:
        x_data (list): The x data for each point to be tested on the
            polynomial solution.
        y_data (list): The y data for each point to be tested on the
            polynomial solution.
        mean (bool): Indicates whether the error should be the mean or not.

    Attributes:
        x_data (list): The x data for each point to be tested on the
            polynomial solution.
        y_data (list): The y data for each point to be tested on the
            polynomial solution.
        mean (bool): Indicates whether the error should be the mean or not.

    Methods:
        evaluate(x): Evaluate the squared error function at the given point.
    """

    def __init__(
        self, x_data: List[float], y_data: List[float], mean: bool = False
    ):
        super().__init__()
        self.x_data = x_data
        self.y_data = y_data
        self.mean = mean

    def evaluate(self, polynomial: List[float]) -> float:
        """
        Evaluate the squared error function at the given point.

        Args:
            polynomial (list): The polynomial coefficients on which you want
                to evaluate the function.

        Returns:
            float: The sum of the squared error at each point saved in this
            object instance.
        """
        error: float = 0.0

        for x, y in zip(self.x_data, self.y_data):
            # calculate the polynomial y
            y_hat = 0.0
            for i, coefficient in enumerate(polynomial):
                y_hat += coefficient * (x**i)

            # calculate the difference from y_hat and the real y
            error += (y_hat - y) ** 2

        if self.mean:
            return error / len(self.x_data)
        else:
            return error
