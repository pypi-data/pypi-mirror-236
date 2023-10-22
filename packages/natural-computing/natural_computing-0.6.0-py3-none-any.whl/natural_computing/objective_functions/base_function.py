"""
BaseFunction Interface
This module defines the interface for objective functions.

Classes:
    BaseFunction: The base interface for objective functions.
"""

from abc import ABC, abstractmethod
from typing import List


class BaseFunction(ABC):
    """
    The base interface for objective functions.

    Methods:
        evaluate(x): Abstract method to evaluate the function at the given
            point.
    """

    def __init__(self, best_fit: float = None) -> None:
        self.best_fit: float | None = best_fit

    @abstractmethod
    def evaluate(self, point: List[float]) -> float:
        """
        Evaluate the function at the given point.

        Args:
            point: The Rn point at which to evaluate the function.

        Returns:
            float value indicates the fitness of the point with the
            current objective function.
        """
