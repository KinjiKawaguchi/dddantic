"""フィールドの型注釈から、参照している具象クラスを取り出すヘルパ。

``list[Money]`` や ``Optional[CustomerId]`` のような合成型を展開し、
制約検査と作図の双方が同じ規則で関係を判定できるようにする。
"""

from __future__ import annotations

import typing
from typing import Any

_MUTABLE_CONTAINER_ORIGINS = (list, set, dict, bytearray)


def referenced_types(annotation: Any) -> tuple[type, ...]:
    """注釈に現れる具象クラスを再帰的に集めて返す。

    ``Optional[X]`` の ``None`` は除外する。型でないもの（TypeVar 等）は無視。
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
    """注釈の最外殻が可変コンテナ（list/set/dict 等）かを判定する。

    素の ``list`` と パラメータ付き ``list[X]`` の双方を検出する。
    """
    if annotation in _MUTABLE_CONTAINER_ORIGINS:
        return True
    return typing.get_origin(annotation) in _MUTABLE_CONTAINER_ORIGINS


def type_label(annotation: Any) -> str:
    """Mermaid 表示用に注釈を読みやすい文字列へ整形する。"""
    origin = typing.get_origin(annotation)
    if origin is None:
        return getattr(annotation, "__name__", str(annotation))
    args = ", ".join(
        type_label(arg) for arg in typing.get_args(annotation) if arg is not type(None)
    )
    origin_name = getattr(origin, "__name__", str(origin))
    return f"{origin_name}~{args}~" if args else origin_name
