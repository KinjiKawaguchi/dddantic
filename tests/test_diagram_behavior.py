import pytest

from dddantic import (
    AggregateRoot,
    DomainService,
    Factory,
    Identifier,
    Repository,
    Specification,
    ValueObject,
    diagram,
)


@pytest.fixture
def rendered() -> str:
    """Define the domain after the registry is cleared, then render it."""

    class OrderId(Identifier):
        value: int

    class Money(ValueObject):
        amount: int

    class Order(AggregateRoot[OrderId]):
        total: Money

    class BigOrder(Specification[Order]):
        def is_satisfied_by(self, candidate: Order) -> bool:
            return candidate.total.amount > 100

    class OrderRepository(Repository[Order]):
        pass

    class Pricing(DomainService):
        pass

    class OrderFactory(Factory):
        pass

    return diagram.to_mermaid()


def test_behavior_stereotypes_present(rendered: str):
    assert "<<Specification>>" in rendered
    assert "<<Repository>>" in rendered
    assert "<<DomainService>>" in rendered
    assert "<<Factory>>" in rendered


def test_repository_targets_aggregate_edge(rendered: str):
    assert "OrderRepository ..> Order : manages" in rendered


def test_specification_targets_candidate_edge(rendered: str):
    assert "BigOrder ..> Order : checks" in rendered


def test_service_and_factory_have_no_auto_edges(rendered: str):
    assert "Pricing ..>" not in rendered
    assert "OrderFactory ..>" not in rendered
