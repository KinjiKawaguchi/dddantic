"""ValueObject と Identifier。

ValueObject は不変・値等価・hashable（Evans: immutable / equality by attributes）。
Identifier は identity を表す単一値の ValueObject（Vernon: model identity as a VO）。
"""

from dddantic._compat import BaseModel
from dddantic.building_blocks._meta import DddanticMeta


class ValueObject(BaseModel, metaclass=DddanticMeta):
    """属性の値で同一視される不変オブジェクト。"""

    __dddantic_base__ = True
    __dddantic_kind__ = "value_object"
    __dddantic_config__ = {"frozen": True}


class Identifier(ValueObject):
    """identity を表す単一値の ValueObject。

    具象 identity はこれを継承し ``value`` を1つ宣言する::

        class OrderId(Identifier):
            value: UUID
    """

    __dddantic_base__ = True
    __dddantic_kind__ = "identifier"
