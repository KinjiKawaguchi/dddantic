import pytest

from dddantic import Specification, default_registry


class Even(Specification[int]):
    def is_satisfied_by(self, candidate: int) -> bool:
        return candidate % 2 == 0


class Positive(Specification[int]):
    def is_satisfied_by(self, candidate: int) -> bool:
        return candidate > 0


def test_leaf_specification():
    assert Even().is_satisfied_by(4)
    assert not Even().is_satisfied_by(3)


def test_and():
    spec = Even() & Positive()
    assert spec.is_satisfied_by(4)
    assert not spec.is_satisfied_by(-4)
    assert not spec.is_satisfied_by(3)


def test_or():
    spec = Even() | Positive()
    assert spec.is_satisfied_by(3)
    assert spec.is_satisfied_by(-4)
    assert not spec.is_satisfied_by(-3)


def test_not():
    spec = ~Even()
    assert spec.is_satisfied_by(3)
    assert not spec.is_satisfied_by(4)


def test_chained_composition():
    spec = (Even() | Positive()) & ~Even()
    assert spec.is_satisfied_by(3)
    assert not spec.is_satisfied_by(4)


def test_abstract_cannot_instantiate():
    with pytest.raises(TypeError):
        Specification()  # type: ignore[abstract]


def test_registered():
    class Multiple(Specification[int]):
        def is_satisfied_by(self, candidate: int) -> bool:
            return candidate % 3 == 0

    _ = Multiple() & Multiple()  # combinators must not register
    kinds = {info.kind for info in default_registry.elements()}
    assert "specification" in kinds
    names = {info.name for info in default_registry.elements()}
    assert "Multiple" in names
    assert "_AndSpecification" not in names
