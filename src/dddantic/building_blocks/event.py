"""DomainEvent。

集約が発行する、過去に起きた出来事の不変な記録。ValueObject と同じく不変で、
発生時刻 ``occurred_on`` を持つ（Vernon: aggregates publish domain events）。
"""

from datetime import datetime

from dddantic.building_blocks.value_object import ValueObject


class DomainEvent(ValueObject):
    """ドメインで起きた出来事の不変な記録。"""

    __dddantic_base__ = True
    __dddantic_kind__ = "domain_event"

    occurred_on: datetime
