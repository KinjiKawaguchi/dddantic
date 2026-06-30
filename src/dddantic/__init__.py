"""dddantic — Pydantic ベースの DDD 戦術的構成要素。"""

from dddantic import diagram
from dddantic.building_blocks import (
    AggregateRoot,
    DomainEvent,
    Entity,
    Identifier,
    ValueObject,
    bounded_context,
)
from dddantic.registry import ElementInfo, Registry, default_registry

__version__ = "0.1.0"

__all__ = [
    "AggregateRoot",
    "DomainEvent",
    "ElementInfo",
    "Entity",
    "Identifier",
    "Registry",
    "ValueObject",
    "__version__",
    "bounded_context",
    "default_registry",
    "diagram",
]
