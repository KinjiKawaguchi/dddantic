"""Generate a Mermaid context map from registered elements.

A context map is a strategic-design overview: each bounded context is a node, and an
edge ``A --> B`` means context ``A`` references an aggregate owned by context ``B``
(``A`` is downstream / depends on ``B``). Dependencies are derived from the same
identity references the class diagram draws, plus repository / specification targets.
"""

from __future__ import annotations

import re

from dddantic._compat import field_annotations
from dddantic.building_blocks._introspect import first_type_arg, referenced_types
from dddantic.building_blocks._kinds import (
    ATTR_KIND,
    KIND_IDENTIFIER,
    KIND_REPOSITORY,
    KIND_SPECIFICATION,
)
from dddantic.building_blocks.repository import Repository
from dddantic.building_blocks.specification import Specification
from dddantic.registry import ElementInfo, Registry, default_registry

_MODEL_KINDS = frozenset({"value_object", "identifier", "entity", "aggregate", "domain_event"})


def to_context_map(registry: Registry | None = None) -> str:
    """Return a Mermaid ``graph`` showing dependencies between bounded contexts."""
    registry = registry or default_registry
    elements = registry.elements()
    contexts = sorted({info.bounded_context for info in elements if info.bounded_context})
    deps: set[tuple[str, str]] = set()
    for info in elements:
        source = info.bounded_context
        if not source:
            continue
        for target_ctx in _referenced_contexts(info, registry):
            if target_ctx and target_ctx != source:
                deps.add((source, target_ctx))

    lines = ["graph LR"]
    lines.extend(f'  {_node_id(ctx)}["{ctx}"]' for ctx in contexts)
    lines.extend(f"  {_node_id(src)} --> {_node_id(dst)}" for src, dst in sorted(deps))
    return "\n".join(lines)


def _referenced_contexts(info: ElementInfo, registry: Registry) -> list[str]:
    contexts: list[str] = []
    for aggregate in _referenced_aggregates(info, registry):
        target = registry.info_for(aggregate)
        if target is not None and target.bounded_context:
            contexts.append(target.bounded_context)
    return contexts


def _referenced_aggregates(info: ElementInfo, registry: Registry) -> list[type]:
    if info.kind in _MODEL_KINDS:
        return _aggregates_from_fields(info, registry)
    if info.kind == KIND_REPOSITORY:
        return _as_aggregate(first_type_arg(info.cls, Repository))
    if info.kind == KIND_SPECIFICATION:
        return _as_aggregate(first_type_arg(info.cls, Specification))
    return []


def _aggregates_from_fields(info: ElementInfo, registry: Registry) -> list[type]:
    aggregates: list[type] = []
    for annotation in field_annotations(info.cls).values():
        for referenced in referenced_types(annotation):
            if getattr(referenced, ATTR_KIND, None) != KIND_IDENTIFIER:
                continue
            owner = registry.aggregate_for_id_type(referenced)
            if owner is not None and owner is not info.cls:
                aggregates.append(owner)
    return aggregates


def _as_aggregate(candidate: object) -> list[type]:
    return [candidate] if isinstance(candidate, type) else []


def _node_id(context: str) -> str:
    return re.sub(r"\W", "_", context)
