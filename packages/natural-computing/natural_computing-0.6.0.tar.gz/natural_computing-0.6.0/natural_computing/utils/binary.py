"""
binary.py - Binary Representation Conversion Utilities

    This module provides utility functions for converting between
    floating-point numbers and their IEEE 754 binary representations,
    as well as flipping (inverting) binary strings.

Functions:
    float_to_binary_ieee754(number: float) -> str:
        Convert a floating-point number to its IEEE 754 binary representation.

    binary_ieee754_to_float(binary_string: str) -> float:
        Convert an IEEE 754 binary representation to a floating-point number.

    inverse_binary(binary_string: str) -> str:
        Invert (flip) the bits in a binary string.
"""

import struct
from typing import cast


def float_to_binary_ieee754(number: float) -> str:
    """
    Convert a floating-point number to its IEEE 754 binary representation.

    Args:
        number (float): The floating-point number to be converted.

    Returns:
        str: The IEEE 754 binary representation of the input number as a
            string.
    """
    binary_representation = struct.pack('>f', number)
    binary_string = ''.join(f'{byte:08b}' for byte in binary_representation)
    return binary_string


def binary_ieee754_to_float(binary_string: str) -> float:
    """
    Convert an IEEE 754 binary representation to a floating-point number.

    Args:
        binary_string (str): The IEEE 754 binary representation as a string.

    Returns:
        float: The floating-point number converted from the binary
            representation.
    """
    bytes_list = [
        binary_string[i : i + 8] for i in range(0, len(binary_string), 8)
    ]
    byte_sequence = bytes([int(byte, 2) for byte in bytes_list])
    (float_number,) = cast(float, struct.unpack('>f', byte_sequence))
    return float_number


def inverse_binary(binary_string: str) -> str:
    """
    Invert (flip) the bits in a binary string.

    Args:
        binary_string (str): The binary string to be inverted.

    Returns:
        str: The inverted binary string.
    """
    return ''.join(['1' if c == '0' else '0' for c in binary_string])
