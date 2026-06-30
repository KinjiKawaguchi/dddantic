"""DDD 要素の不変条件をクラス定義時に検査する。

各検査は違反時に ``TypeError`` を送出する（早期失敗）。原理の根拠は
docstring とエラーメッセージに記す。
"""

from __future__ import annotations

from dddantic._compat import field_annotations, is_unresolved
from dddantic.building_blocks._introspect import (
    has_mutable_container,
    referenced_types,
)
from dddantic.building_blocks._kinds import ATTR_KIND, KIND_AGGREGATE


def check_value_object(cls: type) -> None:
    """ValueObject は不変かつ hashable。可変コンテナを持てない。"""
    for name, annotation in field_annotations(cls).items():
        if has_mutable_container(annotation):
            raise TypeError(
                f"{cls.__name__}.{name}: ValueObject は不変・hashable である必要があり、"
                "可変コンテナ(list/set/dict)を持てません。tuple/frozenset を使ってください。"
            )


def check_identifier(cls: type) -> None:
    """Identifier は単一の値からなる ValueObject。"""
    check_value_object(cls)
    fields = field_annotations(cls)
    if len(fields) != 1:
        raise TypeError(
            f"{cls.__name__}: Identifier は単一の値を表すため、フィールドは1つにしてください"
            f"（現在 {len(fields)} 個）。"
        )


def check_entity(cls: type) -> None:
    """Entity は identity の型が束縛されていなければならない。"""
    id_type = field_annotations(cls).get("id")
    if id_type is None:
        raise TypeError(
            f"{cls.__name__}: Entity は identity フィールド 'id' を持つ必要があります。"
        )
    if is_unresolved(id_type):
        raise TypeError(
            f"{cls.__name__}: identity の型を指定してください。"
            f"例: class {cls.__name__}(AggregateRoot[{cls.__name__}Id])。"
        )


def check_aggregate(cls: type) -> None:
    """集約は他の集約をインスタンスで保持できない（identity 参照のみ）。"""
    check_entity(cls)
    for name, annotation in field_annotations(cls).items():
        if name == "id":
            continue
        for referenced in referenced_types(annotation):
            if getattr(referenced, ATTR_KIND, None) == KIND_AGGREGATE:
                raise TypeError(
                    f"{cls.__name__}.{name}: 他の集約 {referenced.__name__} を"
                    "インスタンスで保持できません。Identifier（id）で参照してください"
                    "（Vernon: Reference Other Aggregates by Identity）。"
                )
