"""
Differential Evolution
    This module implements the Differential Evolution Optimization algorithm.

Classes:
    DifferentialEvolution: An implementation of the Differential Evolution.
"""

import random
from typing import List, Tuple

from natural_computing.objective_functions import BaseFunction
from natural_computing.utils import (
    bounded_random_vectors,
    mul_list,
    sub_lists,
    sum_lists,
)

from .base_optimizer import PopulationBaseOptimizer


class DifferentialEvolution(PopulationBaseOptimizer):
    def __init__(
        self,
        max_iterations: int,
        population_size: int,
        search_space: List[Tuple[float, float]],
        f_const: float = 0.75,
        cr_const: float = 0.90,
    ) -> None:
        """
        Initialize the Differential Evolution optimizer.

        Args:
            max_iterations (int): The maximum number of optimization
                iterations.
            population_size (int): The size of the population.
            search_space (List[Tuple[float, float]]): The search space bounds
                for each dimension.
            f_const (float): Scaling factor for differential mutation
                (default is 0.75).
            cr_const (float): Crossover rate for recombination
                (default is 0.90).
        """
        super().__init__(max_iterations, population_size, search_space)
        self.f_const: float = f_const
        self.cr_const: float = cr_const
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
        Perform a single optimization step using Differential Evolution.

        Args:
            objective_function (BaseFunction): The objective function to be
                optimized.

        Returns:
            List[float]: List of fitness values for the population.
        """
        fits = []
        population_m: List[List[float]] = []

        for _ in range(self.population_size):
            # randomly select three distinct indices
            indices = random.sample(range(0, self.population_size), 3)

            # apply the differential mutation
            population_m.append(
                sum_lists(
                    self.population[indices[0]],
                    mul_list(
                        self.f_const,
                        sub_lists(
                            self.population[indices[1]],
                            self.population[indices[2]],
                        ),
                    ),
                )
            )

        # perform crossover and recombination
        for _ in range(self.population_size):
            i_o = random.choice(range(0, self.population_size))
            i_m = random.choice(range(0, self.population_size))

            for i in range(len(self.population[0])):
                if random.random() > self.cr_const:
                    population_m[i_m][i] = self.population[i_o][i]

        # select best individuals
        for i in range(self.population_size):
            fit_m = objective_function.evaluate(population_m[i])
            fit_o = objective_function.evaluate(self.population[i])

            if fit_m < fit_o:
                fits.append(fit_m)
                self.population[i] = population_m[i]
            else:
                fits.append(fit_o)

            # update the best value found
            if fits[i] < self.best_global_value:
                self.best_global_value = fits[i]
                self.best_global_position = self.population[i]

        return fits
