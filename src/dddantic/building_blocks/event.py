"""DomainEvent.

Immutable record of past occurrences published by aggregates. Like ValueObject,
immutable and carries ``occurred_on`` timestamp (Vernon: aggregates publish
domain events).
"""

from datetime import datetime

from dddantic.building_blocks.value_object import ValueObject


class DomainEvent(ValueObject):
    """Immutable record of an event that occurred in the domain."""

    __dddantic_base__ = True
    __dddantic_kind__ = "domain_event"

    occurred_on: datetime
