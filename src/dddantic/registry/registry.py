"""定義された DDD 要素を収集するレジストリ。

building_blocks には依存しない（依存方向は building_blocks → registry の一方向）。
要素の種別は文字列 kind で持ち、具象クラスを import しないことで循環を避ける。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ElementInfo:
    """登録された 1 要素のメタdata。"""

    cls: type
    kind: str
    name: str
    module: str
    bounded_context: str | None


class Registry:
    """要素と「id 型 → 集約」の対応を保持する。"""

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
        """テスト用にレジストリを空にする。"""
        self._elements.clear()
        self._id_type_to_aggregate.clear()


default_registry = Registry()
