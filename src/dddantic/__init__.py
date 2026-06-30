"""dddantic — Pydantic-based DDD tactical building blocks."""

from dddantic import diagram
from dddantic.building_blocks import (
    AggregateRoot,
    DomainEvent,
    DomainService,
    Entity,
    Factory,
    Identifier,
    Repository,
    Specification,
    ValueObject,
    bounded_context,
)
from dddantic.registry import ElementInfo, Registry, default_registry

__version__ = "0.1.0"

__all__ = [
    "AggregateRoot",
    "DomainEvent",
    "DomainService",
    "ElementInfo",
    "Entity",
    "Factory",
    "Identifier",
    "Registry",
    "Repository",
    "Specification",
    "ValueObject",
    "__version__",
    "bounded_context",
    "default_registry",
    "diagram",
]
