from typing import Generic, Protocol, TypeAlias, TypeVar, runtime_checkable
from abc import abstractmethod


@runtime_checkable
class SupportsMatrixOperations(Protocol):
    """An ABC with one abstract method __complex__."""

    __slots__ = ()

    @abstractmethod
    def add(self) -> complex:
        pass


T = TypeVar('T', int, float, complex)   # makes float and integer compliant
ListMatrix: TypeAlias = list[list[T]]


class Matrix(Generic[T]):
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

    def add(self, other: ListMatrix) -> ListMatrix:
        element_wise_addition = [
            [a + b for a, b in zip(row1, row2)]
            for row1, row2 in zip(self.matrix, other)
        ]
        return element_wise_addition
