"""AggregateRoot.

Consistency boundary. Access only through the root from outside; reference other
aggregates by identity (Evans: consistency boundary / Vernon: reference other
aggregates by identity). Accumulates domain events and exposes them at commit boundary.
"""

from typing import Generic

from dddantic._compat import PrivateAttr
from dddantic.building_blocks.entity import Entity, TId
from dddantic.building_blocks.event import DomainEvent


class AggregateRoot(Entity[TId], Generic[TId]):
    """Root entity forming the aggregate boundary."""

    __dddantic_base__ = True
    __dddantic_kind__ = "aggregate"

    _events: list[DomainEvent] = PrivateAttr(default_factory=list)

    def register_event(self, event: DomainEvent) -> None:
        """Record an occurred domain event."""
        self._events.append(event)

    def collect_events(self) -> tuple[DomainEvent, ...]:
        """Drain accumulated events and clear the internal queue."""
        drained = tuple(self._events)
        self._events.clear()
        return drained

    @property
    def pending_events(self) -> tuple[DomainEvent, ...]:
        """Peek at pending events in read-only mode."""
        return tuple(self._events)
