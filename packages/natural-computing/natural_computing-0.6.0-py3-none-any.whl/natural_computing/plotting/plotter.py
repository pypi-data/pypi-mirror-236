"""
Plotter class
    This module defines the class for tracing curves in 3D and 2D space.

Classes:
    Plotter: The class that has the methods to make plots with objective
        functions.
"""

from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.axes import Axes

from natural_computing.objective_functions import BaseFunction


class Plotter:
    """
    The class for make plots using the give objective function.

    Methods:
        plot_3d_curve(objective_function, x_range, y_range, num_points):
            Draws a curve with num_points for each axis in 3D space,
            delimited by x_range and y_range.
    """

    @staticmethod
    def plot_3d_curve(
        objective_function: BaseFunction,
        x_range: Tuple[float, float],
        y_range: Tuple[float, float],
        num_points: int = 40,
    ) -> Axes:
        """
        Draws the given objective function.

        Args:
            objective_function (BaseFunction): The objective function to be
                drawn. Note that the function must have a point with two
                variables.
        """
        # generate x and y axis
        x_points = np.linspace(x_range[0], x_range[1], num_points)
        y_points = np.linspace(y_range[0], y_range[1], num_points)
        x_axis, y_axis = np.meshgrid(x_points, y_points)

        # compute z axis for each point
        z_axis = np.zeros_like(x_axis)
        for i in range(x_axis.shape[0]):
            for j in range(x_axis.shape[1]):
                z_axis[i][j] = objective_function.evaluate(
                    [x_points[i], y_points[j]]
                )

        # plot curve
        axes = plt.axes(projection='3d')
        axes.plot_surface(
            x_axis,
            y_axis,
            z_axis,
            cmap=cm.coolwarm,
            lw=0.5,
            rstride=2,
            cstride=2,
            alpha=0.75,
        )

        return axes
