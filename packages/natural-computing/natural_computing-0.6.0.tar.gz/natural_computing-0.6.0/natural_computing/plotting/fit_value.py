"""
Fit Value Module
    This module defines functions to plot fitness values.

Methods:
    best_mean_plot
"""

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from natural_computing.optimization import PopulationBaseOptimizer


def best_mean_plot(optimizer: PopulationBaseOptimizer) -> Axes:
    """
    Plot the best and mean fitness values over iterations for a
    population-based optimizer.

    Parameters:
        optimizer (PopulationBaseOptimizer): An instance of a
            population-based optimizer.

    Returns:
        Axes: The matplotlib Axes object containing the generated plot.

    This function takes an optimizer object and plots the best and mean
    fitness values over the iterations of the optimizer's history. It creates
    a line plot with the best fitness values and another line plot with the
    mean fitness values. The x-axis represents the number of iterations, and
    the y-axis represents the fitness values. The plot also includes a legend,
    and labels for the x and y axes.

    Example:
        # Create an optimizer object (e.g., a ParticleSwarmOptimization)
        optimizer = ParticleSwarmOptimization(...)

        # Plot the best and mean fitness values
        ax = best_mean_plot(optimizer)
        plt.show()
    """
    # get history
    history = optimizer.history
    x_values = range(optimizer.max_iterations)

    # plot curves
    _, ax = plt.subplots()
    plt.plot(x_values, history['best'], label='best value')
    plt.plot(x_values, history['mean'], label='mean value')

    # add information
    ax.legend()
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Fitness')

    return ax
