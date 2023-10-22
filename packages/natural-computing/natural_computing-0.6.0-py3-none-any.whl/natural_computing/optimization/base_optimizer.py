"""
BaseOptimizer Interface
    This module defines the interface for optimization algorithms.

Classes:
    BaseOptimizer: The base interface for optimization algorithms.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from natural_computing.objective_functions import BaseFunction


class BaseOptimizer(ABC):
    """
    The base interface for optimization algorithms.

    Methods:
        optimize(objective_function): Abstract method to optimize using the
            given objective function.
    """

    @abstractmethod
    def optimize(
        self,
        objective_function: BaseFunction,
    ) -> None:
        """
        Optimize the given objective function.

        Args:
            objective_function (BaseFunction): The objective function to be
                optimized.
        """


class PopulationBaseOptimizer(ABC):
    """
    The base interface for optimization by algorithms that have some kind of
    population.

    Args:
        max_iterations (int): The maximum number of optimization iterations.
        population_size (int): The size of the algorithm population.
        search_space (list of tuples): The search space for initial particle
            positions.

    Attributes:
        history (Dict[str, list]): Dict with the record of the best and the
            average of the values of the solution solutions by the solver.
        max_iterations (int): The maximum number of optimization iterations.
        population_size (int): The size of the algorithm population.
        search_space (list of tuples): The search space for initial particle
            positions.

    Methods:
        optimize(objective_function): Abstract method to optimize using the
            given objective function.
    """

    def __init__(
        self,
        max_iterations: int,
        population_size: int,
        search_space: List[Tuple[float, float]],
    ) -> None:
        self.max_iterations: int = max_iterations
        self.population_size = population_size
        self.search_space = search_space
        self.best_global_value: float = float('inf')
        self.history: Dict[str, List[float]] = {
            'best': [],
            'mean': [],
        }

    @abstractmethod
    def _optimization_step(
        self,
        objective_function: BaseFunction,
    ) -> List[float]:
        """
        Optimization step using the implemented algorithm, this method is used
            to process a specific population in each iteration of the
            optimizer.

        Args:
            objective_function (BaseFunction): The objective function to be
                optimized.

        Returns:
            list: Fit value for each individual in the population.
        """

    def optimize(
        self,
        objective_function: BaseFunction,
    ) -> None:
        """
        Optimization pipeline.

        Args:
            objective_function (BaseFunction): The objective function to be
                optimized.
        """
        for i in range(self.max_iterations):
            fit_list: List[float] = self._optimization_step(objective_function)

            # print current best value
            print(
                f'[{i + 1}] current min value: {self.best_global_value:.4f}',
                end='\r',
            )

            # add values ​​to history
            self.history['best'].append(self.best_global_value)
            self.history['mean'].append(sum(fit_list) / len(fit_list))
        print()
