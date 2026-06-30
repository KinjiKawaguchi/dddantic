"""AggregateRoot。

整合性の境界。外部からはルート経由でのみアクセスし、他の集約は identity で参照する
（Evans: consistency boundary / Vernon: reference other aggregates by identity）。
発生したドメインイベントを蓄積し、コミット境界で取り出せる。
"""

from typing import Generic

from dddantic._compat import PrivateAttr
from dddantic.building_blocks.entity import Entity, TId
from dddantic.building_blocks.event import DomainEvent


class AggregateRoot(Entity[TId], Generic[TId]):
    """集約の境界を成すルートエンティティ。"""

    __dddantic_base__ = True
    __dddantic_kind__ = "aggregate"

    _events: list[DomainEvent] = PrivateAttr(default_factory=list)

    def register_event(self, event: DomainEvent) -> None:
        """発生したドメインイベントを記録する。"""
        self._events.append(event)

    def collect_events(self) -> tuple[DomainEvent, ...]:
        """蓄積したイベントを取り出し、内部キューを空にする。"""
        drained = tuple(self._events)
        self._events.clear()
        return drained

    @property
    def pending_events(self) -> tuple[DomainEvent, ...]:
        """未取得のイベントを読み取り専用で覗く。"""
        return tuple(self._events)
