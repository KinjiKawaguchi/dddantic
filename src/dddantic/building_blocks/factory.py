"""Factory.

Encapsulates the creation of a complex aggregate or value object, keeping
construction invariants in one place (Evans). Provided as a marker base so factories
appear in the registry, diagrams, and context maps; the creation logic is defined by
subclasses.
"""

from __future__ import annotations

from dddantic.building_blocks._behavior import BehaviorBlock


class Factory(BehaviorBlock):
    """Encapsulates construction of a complex domain object.

    Subclasses expose creation methods that assemble a fully valid object::

        class OrderFactory(Factory):
            def create(self, customer_id: CustomerId, lines: tuple[OrderLine, ...]) -> Order: ...
    """

    __dddantic_base__ = True
    __dddantic_kind__ = "factory"
