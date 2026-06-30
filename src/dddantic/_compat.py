"""pydantic v1/v2 の差異を吸収する唯一の層。

本体ロジックは `pydantic.VERSION` を直接参照せず、このモジュールが公開する
抽象だけに依存する。
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

if TYPE_CHECKING:  # 型注釈用の安定したエイリアス
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

# 凍結違反時の例外は v2=ValidationError / v1=TypeError と割れる。
FROZEN_VIOLATION_ERRORS: tuple[type[Exception], ...] = (
    TypeError,
    pydantic.ValidationError,
)


def field_annotations(cls: type) -> dict[str, Any]:
    """モデルの「フィールド名 → 解決済みの型」を返す。"""
    if PYDANTIC_V1:
        return {name: field.outer_type_ for name, field in cls.__fields__.items()}
    return {name: field.annotation for name, field in cls.model_fields.items()}


def is_unresolved(annotation: Any) -> bool:
    """型がまだ束縛されていない（generic 未指定）かを判定する。"""
    if isinstance(annotation, TypeVar):
        return True
    # pydantic v1 が generic 中間クラスに付ける未解決マーカー
    return type(annotation).__name__ == "DeferredType"


def translate_config(semantic: dict[str, Any]) -> dict[str, Any]:
    """意味的な設定キーを、稼働中の pydantic 版の設定へ翻訳する。

    semantic は ``{"frozen": True, "validate_assignment": True}`` の形。
    """
    config: dict[str, Any] = {}
    if semantic.get("frozen"):
        config["frozen"] = True
        if PYDANTIC_V1:
            config["allow_mutation"] = False
    if semantic.get("validate_assignment"):
        config["validate_assignment"] = True
    return config
