"""
Polynomial Module
    This module defined functions to plot polynomial optimization results.

Methods:
    best_mean_plot
"""
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes


def polynomial_plot(
    polynomial: List[float],
    x_range: Tuple[float, float],
    n_points: int = 100,
    x_data: List[float] = None,
    y_data: List[float] = None,
) -> Axes:
    """
    Plot a polynomial function and optionally overlay data points.

    Parameters:
        polynomial (list): Coefficients of the polynomial, from lowest to
            highest degree.
        x_range (Tuple[float, float]): Range of x-values for the
            plot (start, end).
        n_points (int, optional): Number of points to generate on the x-axis
            for the polynomial plot. Default is 100.
        x_data (list, optional): X-values of data points to overlay on the
            plot. Default is None.
        y_data (list, optional): Y-values of data points to overlay on the
            plot. Default is None.

    Returns:
        Axes: The matplotlib Axes object containing the generated plot.

    This function generates a plot of a polynomial function defined by its
    coefficients and overlays data points if provided. It uses numpy to
    generate the polynomial curve based on the given coefficients and x_range.
    The polynomial coefficients should be listed from the highest degree to
    the lowest degree. The x_range specifies the range of x-values to be
    displayed on the plot. The optional x_data and y_data parameters allow you
    to overlay data points on the polynomial curve if provided. The plot
    includes the polynomial curve and, if data points are given, the data
    points as scatter markers.

    Example:
        # Define a polynomial (e.g., y = 2x^2 - 3x + 1)
        polynomial = [1, -3, 2]

        # Define the x-range for the plot
        x_range = (-5, 5)

        # Generate x and y data points
        x_data = [0, 1, 2, 3, 4]
        y_data = [1, 0, -3, -8, -15]

        # Plot the polynomial with data points
        ax = polynomial_plot(polynomial, x_range, x_data=x_data, y_data=y_data)
        plt.show()
    """
    # generate x and y data from polynomial
    x = np.linspace(*x_range, num=100)
    coefficients = [ci for ci in polynomial[::-1]]
    equation = np.poly1d(coefficients)
    y = equation(x)

    # plot the line
    axes = plt.axes()
    axes.plot(x, y, zorder=1)

    # if data points are provided, plot them on the line
    if x_data is not None and y_data is not None:
        axes.scatter(x_data, y_data, color='#ce4242', zorder=2)

    return axes
