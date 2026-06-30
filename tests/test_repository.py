import pytest

from dddantic import AggregateRoot, Identifier, Repository, ValueObject, default_registry


class OrderId(Identifier):
    value: int


class Order(AggregateRoot[OrderId]):
    n: int


def test_repository_targets_aggregate():
    class OrderRepository(Repository[Order]):
        pass

    info = default_registry.info_for(OrderRepository)
    assert info is not None
    assert info.kind == "repository"


def test_repository_rejects_non_aggregate():
    class Money(ValueObject):
        amount: int

    with pytest.raises(TypeError):

        class BadRepository(Repository[Money]):
            pass


def test_repository_subclass_can_define_methods():
    class OrderRepository(Repository[Order]):
        def __init__(self) -> None:
            self._store: dict[int, Order] = {}

        def add(self, order: Order) -> None:
            self._store[order.id.value] = order

        def get(self, order_id: OrderId) -> Order:
            return self._store[order_id.value]

    repo = OrderRepository()
    order = Order(id=OrderId(value=1), n=5)
    repo.add(order)
    assert repo.get(OrderId(value=1)) is order
