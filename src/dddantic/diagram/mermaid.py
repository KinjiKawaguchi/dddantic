"""Generate Mermaid class diagrams from registered DDD elements.

Relationship rules:
- Aggregate/Entity holds ValueObject or child Entity → composition ``*--``
- Holds other aggregate's Identifier type → reference ``..>`` (identity reference)
- Repository targets its aggregate → reference ``..> : manages``
- Specification targets its candidate type → reference ``..> : checks``
"""

from __future__ import annotations

from dddantic._compat import field_annotations
from dddantic.building_blocks._introspect import (
    first_type_arg,
    referenced_types,
    type_label,
)
from dddantic.building_blocks._kinds import (
    ATTR_KIND,
    KIND_AGGREGATE,
    KIND_DOMAIN_EVENT,
    KIND_DOMAIN_SERVICE,
    KIND_ENTITY,
    KIND_FACTORY,
    KIND_IDENTIFIER,
    KIND_REPOSITORY,
    KIND_SPECIFICATION,
    KIND_VALUE_OBJECT,
)
from dddantic.building_blocks.repository import Repository
from dddantic.building_blocks.specification import Specification
from dddantic.registry import ElementInfo, Registry, default_registry

_STEREOTYPE = {
    KIND_VALUE_OBJECT: "ValueObject",
    KIND_IDENTIFIER: "Identifier",
    KIND_ENTITY: "Entity",
    KIND_AGGREGATE: "AggregateRoot",
    KIND_DOMAIN_EVENT: "DomainEvent",
    KIND_SPECIFICATION: "Specification",
    KIND_REPOSITORY: "Repository",
    KIND_DOMAIN_SERVICE: "DomainService",
    KIND_FACTORY: "Factory",
}
_MODEL_KINDS = (
    KIND_VALUE_OBJECT,
    KIND_IDENTIFIER,
    KIND_ENTITY,
    KIND_AGGREGATE,
    KIND_DOMAIN_EVENT,
)
_COMPOSITION_KINDS = (KIND_VALUE_OBJECT, KIND_ENTITY, KIND_DOMAIN_EVENT)
_IDENTITY_KINDS = (KIND_ENTITY, KIND_AGGREGATE)


def to_mermaid(registry: Registry | None = None, within: str | None = None) -> str:
    """Return Mermaid ``classDiagram`` text.

    If ``within`` is specified, only elements in that bounded context are drawn.
    """
    registry = registry or default_registry
    elements = [
        info for info in registry.elements() if within is None or info.bounded_context == within
    ]
    known = {info.cls for info in elements}

    lines = ["classDiagram"]
    edges: list[str] = []
    for info in elements:
        lines.extend(_class_block(info))
        edges.extend(_edges_for(info, registry, known))

    seen: set[str] = set()
    for edge in edges:
        if edge not in seen:
            seen.add(edge)
            lines.append(edge)
    return "\n".join(lines)


def _class_block(info: ElementInfo) -> list[str]:
    block = [f"class {info.name} {{", f"  <<{_STEREOTYPE[info.kind]}>>"]
    if info.kind in _MODEL_KINDS:
        for name, annotation in field_annotations(info.cls).items():
            block.append(f"  +{type_label(annotation)} {name}")
    block.append("}")
    return block


def _edges_for(info: ElementInfo, registry: Registry, known: set[type]) -> list[str]:
    if info.kind in _MODEL_KINDS:
        return _model_edges(info, registry, known)
    return _behavior_edges(info, known)


def _model_edges(info: ElementInfo, registry: Registry, known: set[type]) -> list[str]:
    edges: list[str] = []
    for name, annotation in field_annotations(info.cls).items():
        if name == "id" and info.kind in _IDENTITY_KINDS:
            continue
        for referenced in referenced_types(annotation):
            edge = _edge(info, referenced, registry, known)
            if edge is not None:
                edges.append(edge)
    return edges


def _behavior_edges(info: ElementInfo, known: set[type]) -> list[str]:
    if info.kind == KIND_REPOSITORY:
        return _behavior_target_edge(info, Repository, known, "manages")
    if info.kind == KIND_SPECIFICATION:
        return _behavior_target_edge(info, Specification, known, "checks")
    return []


def _behavior_target_edge(
    info: ElementInfo,
    base: type,
    known: set[type],
    verb: str,
) -> list[str]:
    target = first_type_arg(info.cls, base)
    if isinstance(target, type) and target in known:
        return [f"{info.name} ..> {target.__name__} : {verb}"]
    return []


def _edge(
    info: ElementInfo,
    referenced: type,
    registry: Registry,
    known: set[type],
) -> str | None:
    kind = getattr(referenced, ATTR_KIND, None)
    if kind == KIND_IDENTIFIER:
        aggregate = registry.aggregate_for_id_type(referenced)
        if aggregate is not None and aggregate is not info.cls:
            return f"{info.name} ..> {aggregate.__name__} : ref"
        return None
    if kind in _COMPOSITION_KINDS and referenced in known:
        return f"{info.name} *-- {referenced.__name__}"
    return None
