"""Repository.

Provides collection-like access to aggregates, mediating between the domain and
persistence (Evans). A repository targets exactly one aggregate root; this constraint
is enforced at class-definition time — the type parameter must be an ``AggregateRoot``
subclass (Vernon: a repository per aggregate).
"""

from __future__ import annotations

from typing import Generic, TypeVar

from dddantic._compat import is_unresolved
from dddantic.building_blocks._behavior import BehaviorBlock
from dddantic.building_blocks._introspect import first_type_arg
from dddantic.building_blocks.aggregate import AggregateRoot

TRoot = TypeVar("TRoot", bound=AggregateRoot)


class Repository(BehaviorBlock, Generic[TRoot]):
    """Collection-like interface for a single aggregate root ``TRoot``.

    Subclasses bind the aggregate via the type parameter and add their own methods::

        class OrderRepository(Repository[Order]):
            def get(self, order_id: OrderId) -> Order: ...
            def add(self, order: Order) -> None: ...
    """

    __dddantic_base__ = True
    __dddantic_kind__ = "repository"

    @classmethod
    def __dddantic_validate__(cls) -> None:
        root = first_type_arg(cls, Repository)
        if root is None or is_unresolved(root):
            return
        if not (isinstance(root, type) and issubclass(root, AggregateRoot)):
            root_name = getattr(root, "__name__", repr(root))
            raise TypeError(
                f"{cls.__name__}: Repository targets an AggregateRoot; "
                f"{root_name} is not an AggregateRoot subclass."
            )
