"""Helper to extract concrete classes referenced in field type annotations.

Expands compound types like ``list[Money]`` and ``Optional[CustomerId]`` so
constraint checks and diagramming apply the same rules for relationship detection.
"""

from __future__ import annotations

import typing
from typing import Any

_MUTABLE_CONTAINER_ORIGINS = (list, set, dict, bytearray)


def referenced_types(annotation: Any) -> tuple[type, ...]:
    """Recursively collect concrete classes appearing in annotation.

    Excludes ``None`` from ``Optional[X]``. Ignores non-type objects (TypeVar, etc).
    """
    origin = typing.get_origin(annotation)
    if origin is None:
        return (annotation,) if isinstance(annotation, type) else ()
    collected: list[type] = []
    for arg in typing.get_args(annotation):
        if arg is type(None):
            continue
        collected.extend(referenced_types(arg))
    return tuple(collected)


def has_mutable_container(annotation: Any) -> bool:
    """Check if outermost layer of annotation is a mutable container (list/set/dict).

    Detects both bare ``list`` and parameterized ``list[X]``.
    """
    if annotation in _MUTABLE_CONTAINER_ORIGINS:
        return True
    return typing.get_origin(annotation) in _MUTABLE_CONTAINER_ORIGINS


def type_label(annotation: Any) -> str:
    """Format annotation into readable string for Mermaid display."""
    origin = typing.get_origin(annotation)
    if origin is None:
        return getattr(annotation, "__name__", str(annotation))
    args = ", ".join(
        type_label(arg) for arg in typing.get_args(annotation) if arg is not type(None)
    )
    origin_name = getattr(origin, "__name__", str(origin))
    return f"{origin_name}~{args}~" if args else origin_name
