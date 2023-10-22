from matrix_manipulation_aharas.classes import Matrix, SupportsMatrixOperations
from matrix_manipulation_aharas.helpers import *
import unittest
import numpy as np

test_matrix = [
    [10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

test_kernel = [
    [1, 2, 1],
    [0, 0, 0],
    [-1, -2, -1],
]


class TestClass(unittest.TestCase):
    def test_non_square_matrix(self):
        non_square_matrix = [
            [10, 11, 12, 13, 14, 15],
            [20, 21, 22, 23, 24, 25],
            [30, 31, 32, 33, 34, 35],
            [1, 2, 3, 4, 5, 6],
            [0, 0, 0, 0, 0, 0],
        ]
        with self.assertRaises(Exception) as context:
            convolution2d(non_square_matrix, test_kernel, 1)
        self.assertTrue('Matrix must be square' in str(context.exception))

    def test_non_numerical_matrix(self):
        non_numerical_matrix = [
            [10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10],
            [0, 0, 0, 0, 'a', 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]
        with self.assertRaises(Exception) as context:
            convolution2d(non_numerical_matrix, test_kernel, 1)
        self.assertTrue('Argument' in str(context.exception))

    def test_convolution(self):
        result_matrix = [
            [0, 0, 0, 0],
            [40, 40, 40, 40],
            [40, 40, 40, 40],
            [0, 0, 0, 0],
        ]
        expected = np.array(result_matrix)
        convoluted = convolution2d(test_matrix, test_kernel, 1)
        for x, y in zip(convoluted, expected):
            self.assertTrue(np.array_equal(x, y, equal_nan=True))

    def test_convolution_numpy(self):
        result_matrix = np.array([[0, 0, 0], [40, 40, 0], [40, 40, 0]])
        expected = np.array(result_matrix)
        convoluted = convolution2d(test_matrix, test_kernel, 2)
        for x, y in zip(convoluted, expected):
            self.assertTrue(np.array_equal(x, y, equal_nan=True))

    def test_windowing(self):
        expected = np.array(
            [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6], [5, 6, 7]]
        )
        windowed = np.array(window1d([1, 2, 3, 4, 5, 6, 7], 3, 1))
        self.assertTrue(np.array_equal(windowed, expected))

    def test_transpose(self):
        expected = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
        result = np.array(transpose2d(test_kernel))
        self.assertTrue(np.array_equal(result, expected))

    def test_matrix_compatibility(self):
        test_matrix = [[1, 2], [2, 5]]
        matrix = Matrix(test_matrix)
        self.assertTrue(isinstance(matrix, SupportsMatrixOperations))

    def test_literal(self):
        test_matrix = [['a', 2], [2, 5]]
        with self.assertRaises(Exception) as context:
            matrix = Matrix(test_matrix)
            print(context.exception)


unittest.main()
