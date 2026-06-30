"""境界づけられたコンテキストのタグ付け。

要素クラスを境界づけられたコンテキストに割り当て、作図でコンテキスト単位に
グルーピングできるようにする。
"""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, TypeVar

from dddantic.building_blocks._kinds import ATTR_CONTEXT
from dddantic.registry import default_registry

if TYPE_CHECKING:
    from collections.abc import Callable

_T = TypeVar("_T", bound=type)


def bounded_context(name: str) -> Callable[[_T], _T]:
    """要素クラスを境界づけられたコンテキスト ``name`` に割り当てるデコレーター。"""

    def decorate(cls: _T) -> _T:
        setattr(cls, ATTR_CONTEXT, name)
        info = default_registry.info_for(cls)
        if info is not None:
            default_registry.register(replace(info, bounded_context=name))
        return cls

    return decorate
