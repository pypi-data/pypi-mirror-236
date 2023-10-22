from numbers import Complex
import numpy as np


def numerical_check(func):
    def inner(*args):
        def check_iterable(args):
            for entry in args:
                if isinstance(entry, Complex):
                    continue
                elif isinstance(entry, (list, np.ndarray)):
                    return check_iterable(entry)
                else:
                    raise TypeError(
                        f'Argument {entry} must be of numerical type'
                    )

        for arg in args:
            if isinstance(arg, Complex):
                continue
            if isinstance(arg, (list, np.ndarray)):
                check_iterable(arg)

        return func(*args)

    return inner


def square_matrix_check(func):
    def inner(*args):
        for arg in args:
            if isinstance(arg, (list, np.ndarray)):
                if len(arg) != len(arg[0]):
                    raise Exception('Matrix must be square')
        return func(*args)

    return inner
