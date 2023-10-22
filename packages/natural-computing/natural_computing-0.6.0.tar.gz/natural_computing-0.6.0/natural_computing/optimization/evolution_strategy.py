"""
Evolution Strategy
    This module implements the Evolution Strategy Optimization algorithm.

Classes:
    EvolutionStrategy: An implementation of the Evolution Strategy.
"""

import random
from typing import List, Tuple

from natural_computing.objective_functions import BaseFunction
from natural_computing.utils import argsort, bounded_random_vectors, sum_lists

from .base_optimizer import PopulationBaseOptimizer


class EvolutionStrategy(PopulationBaseOptimizer):
    def __init__(
        self,
        mu: int,
        lambda_value: int,
        step_size: float,
        max_iterations: int,
        search_space: List[Tuple[float, float]],
        plus_version: bool = False,
    ) -> None:
        """
        Initialize the Evolution Strategy optimizer.

        Args:
            mu (int): Number of selected parents.
            lambda_value (int): The size of the population.
            step_size (float): Constant that multiples Gaussian values
            max_iterations (int): The maximum number of optimization
                iterations.
            search_space (List[Tuple[float, float]]): The search space bounds
                for each dimension.
            plus_version (bool): Indicates whether to add selected parents to
                new generation.
        """
        super().__init__(max_iterations, lambda_value, search_space)
        self._mu = mu
        self._step_size = step_size
        self._dimension = len(search_space)
        self._plus_version = plus_version
        self.population: List[List[float]] = []
        self.best_global_position: List[float] = [0.0 for _ in search_space]
        self.initialize_population()

    def initialize_population(self) -> None:
        """
        Initialize individuals with random values.
        """
        # clear current population
        self.population.clear()

        for _ in range(self.population_size):
            self.population.append(bounded_random_vectors(self.search_space))

    def _optimization_step(
        self, objective_function: BaseFunction
    ) -> List[float]:
        """
        Perform a single optimization step using Evolution Strategy.

        Args:
            objective_function (BaseFunction): The objective function to be
                optimized.

        Returns:
            List[float]: List of fitness values for the population.
        """
        new_population: List[List[float]] = []

        # selected the best individuals based on the rank
        ranks = argsort(
            [objective_function.evaluate(x) for x in self.population]
        )
        selected = [self.population[x] for x in ranks[: self._mu]]

        # generate children
        for parent in selected:
            # add parent
            if self._plus_version:
                new_population.append(parent)

            for _ in range(self.population_size // self._mu):
                # create child
                new_population.append(
                    sum_lists(
                        parent,
                        [
                            self._step_size * random.gauss(0, 1)
                            for _ in range(self._dimension)
                        ],
                    )
                )

        # update the best value found
        self.population = new_population
        fits = [objective_function.evaluate(x) for x in self.population]

        for i in range(self.population_size):
            if fits[i] < self.best_global_value:
                self.best_global_value = fits[i]
                self.best_global_position = self.population[i]

        return fits
