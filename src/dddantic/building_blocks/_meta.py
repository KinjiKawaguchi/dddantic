"""Foundation metaclass for building_blocks.

Inherits from pydantic's ModelMetaclass to (1) inject semantic config based on version,
(2) check invariants after field construction, (3) register with registry.
Metaclass is needed instead of ``__init_subclass__`` because fields are not yet built.
"""

from __future__ import annotations

from typing import Any

from dddantic._compat import (
    PYDANTIC_V1,
    ModelMetaclass,
    field_annotations,
    is_unresolved,
    translate_config,
)
from dddantic.building_blocks import _checks
from dddantic.building_blocks._kinds import (
    ATTR_BASE,
    ATTR_CONFIG,
    ATTR_CONTEXT,
    ATTR_IDENTITY_ALIAS,
    ATTR_KIND,
    KIND_AGGREGATE,
    KIND_DOMAIN_EVENT,
    KIND_ENTITY,
    KIND_IDENTIFIER,
    KIND_VALUE_OBJECT,
)
from dddantic.registry import ElementInfo, default_registry


class DddanticMeta(ModelMetaclass):
    """Metaclass responsible for config injection, constraint checking, and registration."""

    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> type:
        semantic = namespace.pop(ATTR_CONFIG, None)
        if semantic:
            _inject_config(namespace, semantic)
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        _process_class(cls, is_base=bool(namespace.get(ATTR_BASE)))
        return cls


def _inject_config(namespace: dict[str, Any], semantic: dict[str, Any]) -> None:
    translated = translate_config(semantic)
    if PYDANTIC_V1:
        existing = namespace.get("Config")
        parents = (existing,) if existing is not None else ()
        namespace["Config"] = type("Config", parents, dict(translated))
    else:
        existing = dict(namespace.get("model_config") or {})
        existing.update(translated)
        namespace["model_config"] = existing


def _process_class(cls: type, *, is_base: bool) -> None:
    if is_base or "[" in cls.__name__:
        return  # Base classes themselves and generic intermediate artifacts are excluded
    kind = getattr(cls, ATTR_KIND, None)
    if kind is None:
        return
    _run_checks(cls, kind)
    _maybe_add_identity_alias(cls, kind)
    _register(cls, kind)


def _run_checks(cls: type, kind: str) -> None:
    if kind == KIND_IDENTIFIER:
        _checks.check_identifier(cls)
    elif kind in (KIND_VALUE_OBJECT, KIND_DOMAIN_EVENT):
        _checks.check_value_object(cls)
    elif kind == KIND_AGGREGATE:
        _checks.check_aggregate(cls)
    elif kind == KIND_ENTITY:
        _checks.check_entity(cls)


def _maybe_add_identity_alias(cls: type, kind: str) -> None:
    if kind not in (KIND_ENTITY, KIND_AGGREGATE):
        return
    alias = cls.__dict__.get(ATTR_IDENTITY_ALIAS)
    if not alias:
        return
    setattr(cls, alias, property(lambda self: self.id))


def _register(cls: type, kind: str) -> None:
    info = ElementInfo(
        cls=cls,
        kind=kind,
        name=cls.__name__,
        module=cls.__module__,
        bounded_context=getattr(cls, ATTR_CONTEXT, None),
    )
    default_registry.register(info)
    if kind == KIND_AGGREGATE:
        id_type = field_annotations(cls).get("id")
        if id_type is not None and not is_unresolved(id_type):
            default_registry.register_id_type(id_type, cls)
