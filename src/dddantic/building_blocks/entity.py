"""Entity.

Identified by identity (thread of continuity). Equality and hash depend only on
identity, not attributes (Evans: an Entity is defined by a thread of continuity
and identity). Use with explicit identity type like ``Entity[TId]``.
"""

from typing import Generic, TypeVar

from dddantic._compat import GenericModelBase
from dddantic.building_blocks._meta import DddanticMeta

TId = TypeVar("TId")


class Entity(GenericModelBase, Generic[TId], metaclass=DddanticMeta):
    """Mutable object with identity.

    To reference identity by an alias, specify ``__identity_alias__``::

        class Book(AggregateRoot[ISBN]):
            __identity_alias__ = "isbn"   # book.isbn returns book.id
    """

    __dddantic_base__ = True
    __dddantic_kind__ = "entity"
    __dddantic_config__ = {"validate_assignment": True}

    id: TId

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Entity) and type(self) is type(other) and self.id == other.id

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.id))
