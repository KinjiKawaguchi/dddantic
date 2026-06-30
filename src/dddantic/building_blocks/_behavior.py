"""Registration and definition-time checks for behavior-oriented building blocks.

Specification / Repository / DomainService / Factory model behavior and interfaces
rather than data, so they are plain classes that self-register via ``__init_subclass__``
instead of the pydantic metaclass. They populate the same registry as the data models,
so diagramming and context maps treat all building blocks uniformly.
"""

from __future__ import annotations

from typing import Any

from dddantic.building_blocks._kinds import ATTR_BASE, ATTR_KIND
from dddantic.building_blocks.context import resolve_context
from dddantic.registry import ElementInfo, default_registry


class BehaviorBlock:
    """Base for non-model building blocks; self-registers concrete subclasses."""

    __dddantic_kind__: str

    @classmethod
    def __dddantic_validate__(cls) -> None:
        """Definition-time invariant hook; overridden by blocks that need it."""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if cls.__dict__.get(ATTR_BASE) or "[" in cls.__name__:
            return  # Block bases and generic intermediate artifacts are excluded
        kind = getattr(cls, ATTR_KIND, None)
        if kind is None:
            return
        cls.__dddantic_validate__()
        default_registry.register(
            ElementInfo(
                cls=cls,
                kind=kind,
                name=cls.__name__,
                module=cls.__module__,
                bounded_context=resolve_context(cls),
            )
        )
