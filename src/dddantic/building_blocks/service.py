"""Domain Service.

A stateless operation that does not naturally belong to any single Entity or
ValueObject (Evans). Provided as a marker base so services participate in the
registry, diagrams, and context maps; the operations themselves are defined by
subclasses.
"""

from __future__ import annotations

from dddantic.building_blocks._behavior import BehaviorBlock


class DomainService(BehaviorBlock):
    """Stateless domain operation spanning multiple objects.

    Keep instances stateless — hold no entity or value-object state between calls::

        class TransferFunds(DomainService):
            def transfer(self, source: Account, target: Account, amount: Money) -> None: ...
    """

    __dddantic_base__ = True
    __dddantic_kind__ = "domain_service"
