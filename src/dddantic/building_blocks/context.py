"""Assigning element classes to bounded contexts.

A bounded context maps to a module: declare ``__bounded_context__ = "name"`` once at
the top of a module and every element defined in it joins that context. The
``@bounded_context`` decorator overrides this per class for the occasional exception
(e.g. an element living in a shared module).
"""

from __future__ import annotations

import sys
from dataclasses import replace
from typing import TYPE_CHECKING, TypeVar

from dddantic.building_blocks._kinds import ATTR_CONTEXT
from dddantic.registry import default_registry

if TYPE_CHECKING:
    from collections.abc import Callable

_T = TypeVar("_T", bound=type)

MODULE_CONTEXT = "__bounded_context__"


def resolve_context(cls: type) -> str | None:
    """Return the bounded context of ``cls``.

    An explicit attribute on the class itself wins; otherwise the defining module's
    ``__bounded_context__`` applies. Returns ``None`` when neither is set.
    """
    explicit = cls.__dict__.get(ATTR_CONTEXT)
    if explicit is not None:
        return explicit
    module = sys.modules.get(cls.__module__)
    return getattr(module, MODULE_CONTEXT, None) if module is not None else None


def bounded_context(name: str) -> Callable[[_T], _T]:
    """Decorator assigning a single element class to bounded context ``name``.

    Use ``__bounded_context__`` at module scope for the common case; reach for this
    decorator only to override that default for one class.
    """

    def decorate(cls: _T) -> _T:
        setattr(cls, ATTR_CONTEXT, name)
        info = default_registry.info_for(cls)
        if info is not None:
            default_registry.register(replace(info, bounded_context=name))
        return cls

    return decorate
