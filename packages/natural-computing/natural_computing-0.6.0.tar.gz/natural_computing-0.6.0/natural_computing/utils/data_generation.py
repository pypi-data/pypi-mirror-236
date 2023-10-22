"""
Data Generation Module

    This module implement some useful functions to generate toy datasets.
"""

import numpy as np


def make_cubic(
    n_samples: int,
    x_min: float,
    x_max: float,
    a: float = 1,
    b: float = 0,
    c: float = 0,
    d: float = 0,
    noise: float = 0.0,
):
    """
    Generate cubic data with optional noise.

    Args:
        n_samples (int): Number of data points to generate.
        x_min (float): Minimum value of x.
        x_max (float): Maximum value of x.
        a (float, optional): Coefficient for cubic term (defaults to 1).
        b (float, optional): Coefficient for quadratic term (defaults to 0).
        c (float, optional): Coefficient for linear term (defaults to 0).
        d (float, optional): Constant term (defaults to 0).
        noise (float, optional): Standard deviation of white noise to add
            (defaults to 0).

    Returns:
        np.ndarray, np.ndarray: Returns a tuple containing two arrays:
            - The first array is `x` values (shape: (n_samples, 1)).
            - The second array is `y` values corresponding to the cubic
                function with noise (shape: (n_samples, 1)).
    """
    x = np.linspace(x_min, x_max, n_samples)
    y = a * x**3 + b * x**2 + c * x + d

    # add white noise
    y += np.random.normal(0, noise / 2, n_samples)

    return x.reshape(-1, 1), y.reshape(-1, 1)
