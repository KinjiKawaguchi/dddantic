from datetime import datetime

import pytest

from dddantic import DomainEvent, Identifier
from dddantic._compat import FROZEN_VIOLATION_ERRORS


class OrderId(Identifier):
    value: int


class OrderPlaced(DomainEvent):
    order_id: OrderId


def test_event_value_equality():
    when = datetime(2020, 1, 1)
    left = OrderPlaced(order_id=OrderId(value=1), occurred_on=when)
    right = OrderPlaced(order_id=OrderId(value=1), occurred_on=when)
    assert left == right


def test_event_is_frozen():
    event = OrderPlaced(order_id=OrderId(value=1), occurred_on=datetime(2020, 1, 1))
    with pytest.raises(FROZEN_VIOLATION_ERRORS):
        event.order_id = OrderId(value=2)


def test_event_records_occurred_on():
    when = datetime(2021, 6, 30)
    event = OrderPlaced(order_id=OrderId(value=1), occurred_on=when)
    assert event.occurred_on == when
