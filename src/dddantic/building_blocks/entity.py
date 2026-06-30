"""Entity。

identity（連続性の糸）で同一視される。等価性とハッシュは identity のみで決まり、
属性では決まらない（Evans: an Entity is defined by a thread of continuity and identity）。
``Entity[TId]`` のように identity の型を指定して使う。
"""

from typing import Generic, TypeVar

from dddantic._compat import GenericModelBase
from dddantic.building_blocks._meta import DddanticMeta

TId = TypeVar("TId")


class Entity(GenericModelBase, Generic[TId], metaclass=DddanticMeta):
    """identity を持つ可変オブジェクト。

    identity を別名で参照したい場合は ``__identity_alias__`` を指定する::

        class Book(AggregateRoot[ISBN]):
            __identity_alias__ = "isbn"   # book.isbn が book.id を返す
    """

    __dddantic_base__ = True
    __dddantic_kind__ = "entity"
    __dddantic_config__ = {"validate_assignment": True}

    id: TId

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Entity) and type(self) is type(other) and self.id == other.id

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.id))
