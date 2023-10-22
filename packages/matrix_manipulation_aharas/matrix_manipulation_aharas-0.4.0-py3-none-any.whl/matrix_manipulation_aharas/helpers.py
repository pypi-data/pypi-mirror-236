import numpy as np
from .decorators import *
import math


@numerical_check
def transpose2d(input_matrix: list[list[float]]) -> list:
    """Function transposing a matrix.

    Args:
        input_matrix (list[list[float]]): a matrix

    Returns:
        list: a transposed matrix
    """
    transposed = [
        [False for _ in range(len(input_matrix))]
        for _ in range(len(input_matrix[0]))
    ]
    for i_row, row in enumerate(input_matrix):
        for i_column, entry in enumerate(row):
            if not transposed[i_column][i_row]:
                transposed[i_column][i_row] = entry
    return transposed


@numerical_check
def window1d(
    input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1
) -> list[list | np.ndarray]:
    """A helpers function splitting the array into windowed sequences.

    Args:
        input_array (list | np.ndarray): array to be windowed.
        size (int): size of the window
        shift (int, optional): size of window's step forward. Defaults to 1.
        stride (int, optional): size of entry's index increase in the window. Defaults to 1.

    Raises:
        Exception: if provided numerical values are non-positive.

    Returns:
        list[list | np.ndarray]: a list of windowed sequences.
    """
    if size <= 0 or shift <= 0 or stride <= 0:
        raise Exception('Size must be greater than 0')
    windowed_list = list()
    for i in range(0, len(input_array), shift):
        window = input_array[i::stride][:size]
        if len(window) < size:
            continue
        windowed_list.append(input_array[i::stride][:size])
    return windowed_list


@numerical_check
@square_matrix_check
def convolution2d(
    input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1
) -> np.ndarray:
    """A helper function performing a 2d convolution.

    Args:
        input_matrix (np.ndarray): matrix to be convoluted with kernel.
        kernel (np.ndarray): a filter matrix.
        stride (int, optional): a size of kernel's step forward. Defaults to 1.

    Raises:
        Exception: if provided numerical values are non-positive.

    Returns:
        np.ndarray: convoluted matrix
    """
    expected_size = math.ceil(((len(input_matrix) - len(kernel)) / stride) + 1)
    kernel_size = len(kernel)
    convoluted_matrix = [
        [False for _ in range(expected_size)] for x in range(expected_size)
    ]
    if stride <= 0:
        raise Exception('Stride must be greater than 0')
    for index, _ in enumerate(input_matrix[0::stride]):
        kernel_spanned_rows = input_matrix[index : index + kernel_size]
        matrix_cutout = [
            window1d(row, kernel_size, stride) for row in kernel_spanned_rows
        ]
        if len(matrix_cutout) < kernel_size:
            continue
        for cutout_index, cutout_rows in enumerate(transpose2d(matrix_cutout)):
            correlation_value = 0
            if len(cutout_rows[0]) < kernel_size:
                continue
            for kernel_index, kernel_row in enumerate(cutout_rows):
                correlated_row_value = sum(
                    [a * b for a, b in zip(kernel_row, kernel[kernel_index])]
                )
                correlation_value += correlated_row_value
            convoluted_matrix[cutout_index][index] = correlation_value
    return np.array(transpose2d(convoluted_matrix))


def print_matrix(data: np.ndarray | list):
    print(np.array(data))
