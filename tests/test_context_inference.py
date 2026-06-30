import sys

import pytest

from dddantic import (
    AggregateRoot,
    Identifier,
    Repository,
    ValueObject,
    bounded_context,
    default_registry,
)


@pytest.fixture
def _module_context(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys.modules[__name__], "__bounded_context__", "sales", raising=False)


@pytest.mark.usefixtures("_module_context")
def test_module_context_applies_to_defined_elements():
    class Sku(Identifier):
        value: str

    class Price(ValueObject):
        amount: int

    assert default_registry.info_for(Sku).bounded_context == "sales"
    assert default_registry.info_for(Price).bounded_context == "sales"


@pytest.mark.usefixtures("_module_context")
def test_module_context_applies_to_behavior_blocks():
    class OrderId(Identifier):
        value: int

    class Order(AggregateRoot[OrderId]):
        n: int

    class OrderRepository(Repository[Order]):
        pass

    assert default_registry.info_for(OrderRepository).bounded_context == "sales"


@pytest.mark.usefixtures("_module_context")
def test_decorator_overrides_module_context():
    @bounded_context("billing")
    class InvoiceId(Identifier):
        value: int

    assert default_registry.info_for(InvoiceId).bounded_context == "billing"


def test_no_context_when_module_undeclared():
    class Loose(ValueObject):
        x: int

    assert default_registry.info_for(Loose).bounded_context is None
