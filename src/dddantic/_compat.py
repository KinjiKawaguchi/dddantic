"""Sole compatibility layer absorbing pydantic v1/v2 differences.

Core logic does not directly reference `pydantic.VERSION` but depends only on
the abstractions exposed by this module.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

import pydantic
from pydantic import BaseModel, PrivateAttr

PYDANTIC_V1 = pydantic.VERSION.startswith("1")

if PYDANTIC_V1:
    from pydantic.generics import GenericModel as _GenericModelBase
    from pydantic.main import ModelMetaclass as _ModelMetaclass
else:
    from pydantic._internal._model_construction import (
        ModelMetaclass as _ModelMetaclass,
    )

    _GenericModelBase = BaseModel

if TYPE_CHECKING:  # Stable aliases for type annotations
    from pydantic._internal._model_construction import ModelMetaclass

    GenericModelBase = BaseModel
else:
    GenericModelBase = _GenericModelBase
    ModelMetaclass = _ModelMetaclass

__all__ = [
    "FROZEN_VIOLATION_ERRORS",
    "PYDANTIC_V1",
    "BaseModel",
    "GenericModelBase",
    "ModelMetaclass",
    "PrivateAttr",
    "field_annotations",
    "is_unresolved",
    "translate_config",
]

# Frozen violations raise different exceptions: v2=ValidationError / v1=TypeError
FROZEN_VIOLATION_ERRORS: tuple[type[Exception], ...] = (
    TypeError,
    pydantic.ValidationError,
)


def field_annotations(cls: type) -> dict[str, Any]:
    """Return model's field names mapped to resolved types."""
    if PYDANTIC_V1:
        return {name: field.outer_type_ for name, field in cls.__fields__.items()}
    return {name: field.annotation for name, field in cls.model_fields.items()}


def is_unresolved(annotation: Any) -> bool:
    """Check if type is unbound (generic not yet specified)."""
    if isinstance(annotation, TypeVar):
        return True
    # pydantic v1 unresolved marker attached to generic intermediate classes
    return type(annotation).__name__ == "DeferredType"


def translate_config(semantic: dict[str, Any]) -> dict[str, Any]:
    """Translate semantic config keys to running pydantic version's config.

    semantic is in the form ``{"frozen": True, "validate_assignment": True}``.
    """
    config: dict[str, Any] = {}
    if semantic.get("frozen"):
        config["frozen"] = True
        if PYDANTIC_V1:
            config["allow_mutation"] = False
    if semantic.get("validate_assignment"):
        config["validate_assignment"] = True
    return config
