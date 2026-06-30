"""Tagging for bounded contexts.

Assigns element classes to bounded contexts, enabling diagramming to group
by context.
"""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, TypeVar

from dddantic.building_blocks._kinds import ATTR_CONTEXT
from dddantic.registry import default_registry

if TYPE_CHECKING:
    from collections.abc import Callable

_T = TypeVar("_T", bound=type)


def bounded_context(name: str) -> Callable[[_T], _T]:
    """Decorator assigning an element class to bounded context ``name``."""

    def decorate(cls: _T) -> _T:
        setattr(cls, ATTR_CONTEXT, name)
        info = default_registry.info_for(cls)
        if info is not None:
            default_registry.register(replace(info, bounded_context=name))
        return cls

    return decorate
