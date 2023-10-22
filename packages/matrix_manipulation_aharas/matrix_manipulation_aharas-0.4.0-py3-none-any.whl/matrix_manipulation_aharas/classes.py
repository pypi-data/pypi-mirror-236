from typing import Generic, Protocol, TypeAlias, TypeVar, runtime_checkable
from abc import abstractmethod


@runtime_checkable
class SupportsMatrixOperations(Protocol):
    """A Protocol with one abstract method add to identify an additive matrix."""

    __slots__ = ()

    @abstractmethod
    def add(self) -> complex:
        pass


T = TypeVar('T', int, float, complex)   # makes float and integer compliant
ListMatrix: TypeAlias = list[list[T]]


class Matrix(Generic[T]):
    """A class representing matrix objects. Inherits from Generic.
    Entries of matrix are of formal type parameter T.
    Meant to accept matrices populated with numerical values.

    matrix: ListMatrix - list of list of respective type T.
    """

    __match_args__ = 'matrix'
    __slots__ = 'matrix'

    def __init__(self, matrix: ListMatrix):
        self.matrix: ListMatrix = matrix

    def __repr__(self):
        return (
            '[\n  '
            + '\n  '.join(
                [
                    ' '.join([str(entry) for entry in row])
                    for row in self.matrix
                ]
            )
            + '\n]'
        )

    def __getitem__(self, index: int) -> ListMatrix:
        return self.matrix[index]

    def __setitem__(self, index: int, value: list[T]) -> None:
        self.matrix[index] = value

    def __len__(self) -> int:
        return len(self.matrix)

    def add(self, other: ListMatrix) -> 'Matrix':
        element_wise_addition = [
            [a + b for a, b in zip(row1, row2)]
            for row1, row2 in zip(self.matrix, other)
        ]
        return Matrix(element_wise_addition)
