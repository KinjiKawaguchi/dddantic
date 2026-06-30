from datetime import datetime

import pytest

from dddantic import AggregateRoot, DomainEvent, Identifier, ValueObject


class AId(Identifier):
    value: int


class BId(Identifier):
    value: int


class A(AggregateRoot[AId]):
    n: int


def test_holds_value_object():
    class Money(ValueObject):
        amount: int

    class B(AggregateRoot[BId]):
        total: Money

    instance = B(id=BId(value=1), total=Money(amount=5))
    assert instance.total.amount == 5


def test_holding_aggregate_instance_rejected():
    with pytest.raises(TypeError):

        class Bad(AggregateRoot[BId]):
            other: A


def test_holding_aggregate_in_collection_rejected():
    with pytest.raises(TypeError):

        class BadList(AggregateRoot[BId]):
            others: list[A]


def test_events_register_collect_drain():
    class Created(DomainEvent):
        pass

    class C(AggregateRoot[BId]):
        n: int

    aggregate = C(id=BId(value=1), n=1)
    aggregate.register_event(Created(occurred_on=datetime(2020, 1, 1)))
    assert len(aggregate.pending_events) == 1

    drained = aggregate.collect_events()
    assert len(drained) == 1
    assert aggregate.pending_events == ()
