"""ValueObject and Identifier.

ValueObject is immutable, value-equal, and hashable (Evans: immutable / equality
by attributes). Identifier is a single-value ValueObject representing identity
(Vernon: model identity as a VO).
"""

from dddantic._compat import BaseModel
from dddantic.building_blocks._meta import DddanticMeta


class ValueObject(BaseModel, metaclass=DddanticMeta):
    """Immutable object identified by its attribute values."""

    __dddantic_base__ = True
    __dddantic_kind__ = "value_object"
    __dddantic_config__ = {"frozen": True}


class Identifier(ValueObject):
    """Single-value ValueObject representing identity.

    Concrete identities inherit from this and declare a single ``value``::

        class OrderId(Identifier):
            value: UUID
    """

    __dddantic_base__ = True
    __dddantic_kind__ = "identifier"
