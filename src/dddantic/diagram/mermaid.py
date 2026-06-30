"""登録済みの DDD 要素から Mermaid のクラス図を生成する。

関係の規則:
- 集約/エンティティが ValueObject・子エンティティを保持 → composition ``*--``
- 他集約の Identifier 型を保持 → reference ``..>``（identity 参照）
"""

from __future__ import annotations

from dddantic._compat import field_annotations
from dddantic.building_blocks._introspect import referenced_types, type_label
from dddantic.building_blocks._kinds import (
    ATTR_KIND,
    KIND_AGGREGATE,
    KIND_DOMAIN_EVENT,
    KIND_ENTITY,
    KIND_IDENTIFIER,
    KIND_VALUE_OBJECT,
)
from dddantic.registry import ElementInfo, Registry, default_registry

_STEREOTYPE = {
    KIND_VALUE_OBJECT: "ValueObject",
    KIND_IDENTIFIER: "Identifier",
    KIND_ENTITY: "Entity",
    KIND_AGGREGATE: "AggregateRoot",
    KIND_DOMAIN_EVENT: "DomainEvent",
}
_COMPOSITION_KINDS = (KIND_VALUE_OBJECT, KIND_ENTITY, KIND_DOMAIN_EVENT)
_IDENTITY_KINDS = (KIND_ENTITY, KIND_AGGREGATE)


def to_mermaid(registry: Registry | None = None, within: str | None = None) -> str:
    """Mermaid ``classDiagram`` テキストを返す。

    ``within`` を指定すると、その境界づけられたコンテキストの要素だけを描く。
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
    for name, annotation in field_annotations(info.cls).items():
        block.append(f"  +{type_label(annotation)} {name}")
    block.append("}")
    return block


def _edges_for(info: ElementInfo, registry: Registry, known: set[type]) -> list[str]:
    edges: list[str] = []
    for name, annotation in field_annotations(info.cls).items():
        if name == "id" and info.kind in _IDENTITY_KINDS:
            continue
        for referenced in referenced_types(annotation):
            edge = _edge(info, referenced, registry, known)
            if edge is not None:
                edges.append(edge)
    return edges


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
