"""Registry collecting defined DDD elements.

Does not depend on building_blocks (dependency direction is one-way: building_blocks
→ registry). Element types are held as string kind, avoiding circular imports by not
importing concrete classes.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ElementInfo:
    """Metadata for a single registered element."""

    cls: type
    kind: str
    name: str
    module: str
    bounded_context: str | None


class Registry:
    """Holds elements and mapping of "id type → aggregate"."""

    def __init__(self) -> None:
        self._elements: dict[type, ElementInfo] = {}
        self._id_type_to_aggregate: dict[type, type] = {}

    def register(self, info: ElementInfo) -> None:
        self._elements[info.cls] = info

    def register_id_type(self, id_type: type, aggregate_cls: type) -> None:
        self._id_type_to_aggregate[id_type] = aggregate_cls

    def elements(self) -> tuple[ElementInfo, ...]:
        return tuple(self._elements.values())

    def info_for(self, cls: type) -> ElementInfo | None:
        return self._elements.get(cls)

    def aggregate_for_id_type(self, id_type: type) -> type | None:
        return self._id_type_to_aggregate.get(id_type)

    def clear(self) -> None:
        """Clear registry for testing."""
        self._elements.clear()
        self._id_type_to_aggregate.clear()


default_registry = Registry()
