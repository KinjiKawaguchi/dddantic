"""What dddantic enforces — run it to feel the guardrails and the semantics.

The shop example shows how to *define* a model. This shows what the library *rejects*
and how its building blocks *behave* — the reasons to reach for it.

    python -m examples.guardrails
"""

from collections.abc import Callable
from datetime import datetime, timezone

from dddantic import (
    AggregateRoot,
    DomainEvent,
    Identifier,
    Repository,
    ValueObject,
)


class AccountId(Identifier):
    value: int


def _rejected(label: str, define: Callable[[], None]) -> None:
    try:
        define()
    except (TypeError, ValueError) as exc:
        parts = [
            line.strip()
            for line in str(exc).splitlines()
            if line.strip() and not line.strip().startswith("For further information")
        ]
        print(f"  rejected: {label}")
        print(f"      {type(exc).__name__}: {' — '.join(parts[:3])}")
    else:
        print(f"  NOT rejected (unexpected): {label}")


def definition_time_guardrails() -> None:
    """Each of these fails the moment the class is defined, not at runtime."""
    print("Rejected at class-definition time:")

    def mutable_value_object() -> None:
        class Tags(ValueObject):
            items: list[str]

    def multi_field_identifier() -> None:
        class CompositeId(Identifier):
            left: int
            right: int

    def aggregate_held_by_instance() -> None:
        class Account(AggregateRoot[AccountId]):
            balance: int

        class Transfer(AggregateRoot[AccountId]):
            counterparty: Account  # must be referenced by id, not held

    def repository_of_non_aggregate() -> None:
        class Money(ValueObject):
            amount: int

        class MoneyRepository(Repository[Money]):
            pass

    _rejected("ValueObject with a mutable container", mutable_value_object)
    _rejected("Identifier with more than one field", multi_field_identifier)
    _rejected("Aggregate holding another aggregate by instance", aggregate_held_by_instance)
    _rejected(
        "Repository whose type parameter is not an AggregateRoot",
        repository_of_non_aggregate,
    )


def runtime_semantics() -> None:
    """How the building blocks behave once defined."""
    print("\nRuntime semantics:")

    class Money(ValueObject):
        amount: int
        currency: str

    first = Money(amount=100, currency="USD")
    second = Money(amount=100, currency="USD")
    print(f"  value equality: Money(100, USD) == Money(100, USD) -> {first == second}")
    print(f"  hashable: a set of the two equal values has {len({first, second})} element")

    def mutate_frozen() -> None:
        first.amount = 200

    _rejected("immutability: assigning to a field of a frozen ValueObject", mutate_frozen)

    class Account(AggregateRoot[AccountId]):
        owner: str

    same_id_a = Account(id=AccountId(value=1), owner="Alice")
    same_id_b = Account(id=AccountId(value=1), owner="Bob")
    print(f"  identity equality: same id, different fields -> equal? {same_id_a == same_id_b}")

    class Withdrawn(DomainEvent):
        occurred_on: datetime

    same_id_a.register_event(Withdrawn(occurred_on=datetime(2026, 6, 30, tzinfo=timezone.utc)))
    drained = same_id_a.collect_events()
    pending = len(same_id_a.pending_events)
    print(f"  events: collected {len(drained)}, pending after draining {pending}")


def main() -> None:
    definition_time_guardrails()
    runtime_semantics()


if __name__ == "__main__":
    main()
