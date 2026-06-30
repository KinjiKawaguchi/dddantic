"""Public API for DDD tactical building blocks."""

from dddantic.building_blocks.aggregate import AggregateRoot
from dddantic.building_blocks.context import bounded_context
from dddantic.building_blocks.entity import Entity
from dddantic.building_blocks.event import DomainEvent
from dddantic.building_blocks.factory import Factory
from dddantic.building_blocks.repository import Repository
from dddantic.building_blocks.service import DomainService
from dddantic.building_blocks.specification import Specification
from dddantic.building_blocks.value_object import Identifier, ValueObject

__all__ = [
    "AggregateRoot",
    "DomainEvent",
    "DomainService",
    "Entity",
    "Factory",
    "Identifier",
    "Repository",
    "Specification",
    "ValueObject",
    "bounded_context",
]
