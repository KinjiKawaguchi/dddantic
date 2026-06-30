"""DDD 戦術的構成要素の公開API。"""

from dddantic.building_blocks.aggregate import AggregateRoot
from dddantic.building_blocks.context import bounded_context
from dddantic.building_blocks.entity import Entity
from dddantic.building_blocks.event import DomainEvent
from dddantic.building_blocks.value_object import Identifier, ValueObject

__all__ = [
    "AggregateRoot",
    "DomainEvent",
    "Entity",
    "Identifier",
    "ValueObject",
    "bounded_context",
]
