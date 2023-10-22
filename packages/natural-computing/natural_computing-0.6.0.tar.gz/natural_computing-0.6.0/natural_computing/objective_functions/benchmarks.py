"""
Benchmarks Module
    This module implements benchmark functions commonly used for testing
    optimization algorithms.

Classes:
    RastriginFunction: The implementation of the Rastrigin function.
"""

import math
from typing import List

from .base_function import BaseFunction


class RastriginFunction(BaseFunction):
    """
    Rastrigin function implementation.

    Args:
        dimension (int): The dimensionality of the Rastrigin function.
        factor (int): The value of the factor that each point is divided before
            calculate the function.

    Attributes:
        dimension (int): The dimensionality of the Rastrigin function.
        factor (int): The value of the factor that each point is divided before
            calculate the function.

    Methods:
        evaluate(x): Evaluate the Rastrigin function at the given point.
    """

    def __init__(self, dimension: int, factor: float = 1.0):
        super().__init__(0.0)
        self.dimension = dimension
        self.factor = factor

    def evaluate(self, point: List[float]) -> float:
        """
        Evaluate the Rastrigin function at the given point.

        Args:
            x (list): The point at which to evaluate the function.

        Returns:
            float: The value of the Rastrigin function at the given point.
        """
        a_const = 10
        value: float = a_const * self.dimension
        for x_i in point:
            value += x_i**2 - a_const * math.cos(2 * math.pi * x_i)
        return value
