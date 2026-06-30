"""Specification.

Encapsulates a predicate over a domain object that can be combined with ``&`` / ``|``
/ ``~`` (Evans: Specification pattern). Concrete specifications implement
``is_satisfied_by``; the combinators below build composite specifications.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from dddantic.building_blocks._behavior import BehaviorBlock

T = TypeVar("T")


class Specification(BehaviorBlock, ABC, Generic[T]):
    """Predicate over a candidate of type ``T``, composable with ``&`` / ``|`` / ``~``."""

    __dddantic_base__ = True
    __dddantic_kind__ = "specification"

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """Return whether ``candidate`` satisfies this specification."""

    def __and__(self, other: Specification[T]) -> Specification[T]:
        return _AndSpecification(self, other)

    def __or__(self, other: Specification[T]) -> Specification[T]:
        return _OrSpecification(self, other)

    def __invert__(self) -> Specification[T]:
        return _NotSpecification(self)


class _AndSpecification(Specification[T]):
    """Conjunction of two specifications."""

    __dddantic_base__ = True

    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self._left.is_satisfied_by(candidate) and self._right.is_satisfied_by(candidate)


class _OrSpecification(Specification[T]):
    """Disjunction of two specifications."""

    __dddantic_base__ = True

    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self._left.is_satisfied_by(candidate) or self._right.is_satisfied_by(candidate)


class _NotSpecification(Specification[T]):
    """Negation of a specification."""

    __dddantic_base__ = True

    def __init__(self, inner: Specification[T]) -> None:
        self._inner = inner

    def is_satisfied_by(self, candidate: T) -> bool:
        return not self._inner.is_satisfied_by(candidate)
