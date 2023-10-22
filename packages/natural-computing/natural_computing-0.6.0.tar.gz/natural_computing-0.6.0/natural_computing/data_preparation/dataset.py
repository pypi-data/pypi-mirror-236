"""
Dataset Module

This module provides functions for creating and splitting datasets.
"""

from typing import Tuple, List

import numpy as np
import requests


def create_window(
    data: np.ndarray, window_size: int
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create input-output pairs for a sliding window from a given dataset.

    Args:
        data (np.ndarray): The input data.
        window_size (int): The size of the sliding window.

    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing input and output
        data arrays.
    """
    x_data, y_data = [], []
    dataset_size = len(data)

    for i in range(dataset_size):
        # check if there is enough data
        if i + window_size + 1 > dataset_size:
            break

        # append data
        x_data.append(data[i: i + window_size])
        y_data.append(data[i + window_size])

    return (np.array(x_data), np.array(y_data).reshape(-1, 1))


def split_train_test(
    x: np.ndarray, y: np.ndarray, train_size: float, sequential: bool = False
) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
    """
    Split a dataset into training and testing sets.

    Args:
        x (np.ndarray): The input data.
        y (np.ndarray): The target data.
        train_size (float): The proportion of data to use for training.
        sequential (bool, optional): If True, perform sequential splitting
        (default is False).

    Returns:
        Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]: A
        tuple containing training and testing data tuples.
    """
    # calculate the size of the sets
    data_size = len(x)
    train_size = int(train_size * data_size)

    # generate indices
    if not sequential:
        train_indices = np.random.choice(
            range(data_size), size=train_size, replace=False
        )
        test_indices = np.array(
            [i for i in range(data_size) if i not in train_indices]
        )
    else:
        train_indices = np.array(range(train_size))
        test_indices = np.array(range(train_size, data_size))

    return (
        (x[train_indices], y[train_indices]),
        (x[test_indices], y[test_indices]),
    )


def filter_strings(input_list, filters):
    """
    Apply a list of filter functions to each element of the input list.

    Args:
        input_list (list): The list of strings to be filtered.
        filters (list): A list of filter functions to apply to each element.

    Returns:
        list: A list of elements after applying the filter functions.

    Note:
        - The function iterates through the input list and applies each filter
            function
          to every element in the list.
        - It returns a new list containing the filtered elements.
    """
    result = input_list[:]

    for filter_func in filters:
        result = list(map(filter_func, result))

    return result


def fetch_file_and_convert_to_array(
    url: str,
    separator: str = ',',
    new_line: str = '\n',
    skiprows: int = 1,
    usecols: List[int] | None = None,
    dtype=np.float32,
) -> np.ndarray:
    """
    Fetch data from a URL, parse it, and convert it into a NumPy array.

    Args:
        url (str): The URL of the file to fetch.
        separator (str, optional): The delimiter used to split the data into
            columns (default is ',').
        new_line (str, optional): The newline character used to split the data
            into rows (default is '\\n').
        skiprows (int, optional): The number of header rows to skip
            (default is 1).
        usecols (List[int] | None, optional): A list of column indices to
            select, or None to select all columns (default is None).
        dtype (type, optional): The data type to which the parsed values
            should be converted (default is np.float32).

    Returns:
        np.ndarray: A NumPy array containing the parsed data.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the
            HTTP request or the status code is not 200.

    Note:
        - The function fetches the file from the given URL using the requests
            library.
        - It processes the content by splitting it into lines, removing empty
            lines, and applying transformations.
        - The resulting data is stored in a NumPy array with the specified
            data type.
    """

    def remove_r_fn(s):
        return s.replace('\r', '')

    def split_fn(s):
        return s.split(separator)

    def select_cols_fn(s):
        return (
            [item for i, item in enumerate(s) if i in usecols]
            if usecols is not None
            else s
        )

    try:
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            content = response.text.split(new_line)

            # get only the needed data
            content = filter_strings(
                [line for line in content if line.strip() != ''][skiprows:],
                [remove_r_fn, split_fn, select_cols_fn]
            )

            return np.array(content, dtype=dtype)

        else:
            raise requests.exceptions.RequestException(
                'Failed to fetch the file. HTTP Status Code: '
                f'{response.status_code}'
            )

    except requests.exceptions.RequestException as e:
        raise e
