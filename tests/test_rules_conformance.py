"""Conformance suite: every rule in the catalog must actually be detected.

This is the quality gate that keeps `dddantic.rules` honest — a rule may not be listed
(and documented in RULES.md) unless a check here proves the library detects its
violation. Run across the whole pydantic v1/v2 CI matrix.
"""

from datetime import datetime, timezone
from pathlib import Path

import pytest

from dddantic import (
    AggregateRoot,
    DomainEvent,
    Identifier,
    Repository,
    ValueObject,
)
from dddantic.rules import RULES, render_rules_md

_FROZEN_VIOLATION = (TypeError, ValueError)


def _entity_identity() -> None:
    class Xid(Identifier):
        value: int

    class E(AggregateRoot[Xid]):
        name: str

    with pytest.raises(_FROZEN_VIOLATION):
        E(name="missing id")  # id is required

    a = E(id=Xid(value=1), name="a")
    b = E(id=Xid(value=1), name="b")
    assert a == b  # equal by identity, not attributes
    assert hash(a) == hash(b)
    assert a != E(id=Xid(value=2), name="a")


def _vo_immutable() -> None:
    class Money(ValueObject):
        amount: int

    assert Money(amount=1) == Money(amount=1)  # value equality
    assert len({Money(amount=1), Money(amount=1)}) == 1  # hashable
    with pytest.raises(_FROZEN_VIOLATION):
        Money(amount=1).amount = 2  # immutable


def _vo_no_mutable_container() -> None:
    with pytest.raises(TypeError):

        class Bad(ValueObject):
            items: list[int]


def _id_single_value() -> None:
    with pytest.raises(TypeError):

        class Bad(Identifier):
            left: int
            right: int

    class Ok(Identifier):
        value: int  # single field is accepted

    assert Ok(value=1) == Ok(value=1)


def _agg_ref_by_id() -> None:
    class Aid(Identifier):
        value: int

    class A(AggregateRoot[Aid]):
        n: int

    with pytest.raises(TypeError):

        class Bad(AggregateRoot[Aid]):
            other: A  # holding another aggregate by instance

    class Ok(AggregateRoot[Aid]):
        ref: Aid  # by identity is accepted

    assert Ok(id=Aid(value=1), ref=Aid(value=2))


def _repo_for_agg_root() -> None:
    class Money(ValueObject):
        amount: int

    with pytest.raises(TypeError):

        class Bad(Repository[Money]):
            pass

    class Aid(Identifier):
        value: int

    class A(AggregateRoot[Aid]):
        n: int

    class Ok(Repository[A]):
        pass

    assert Ok


def _event_immutable_occurred() -> None:
    class Placed(DomainEvent):
        occurred_on: datetime

    event = Placed(occurred_on=datetime(2026, 1, 1, tzinfo=timezone.utc))
    with pytest.raises(_FROZEN_VIOLATION):
        event.occurred_on = datetime(2027, 1, 1, tzinfo=timezone.utc)


CONFORMANCE = {
    "ENTITY-IDENTITY": _entity_identity,
    "VO-IMMUTABLE": _vo_immutable,
    "VO-NO-MUTABLE-CONTAINER": _vo_no_mutable_container,
    "ID-SINGLE-VALUE": _id_single_value,
    "AGG-REF-BY-ID": _agg_ref_by_id,
    "REPO-FOR-AGG-ROOT": _repo_for_agg_root,
    "EVENT-IMMUTABLE-OCCURRED": _event_immutable_occurred,
}


@pytest.mark.parametrize("rule", RULES, ids=lambda rule: rule.id)
def test_rule_is_detected(rule):
    CONFORMANCE[rule.id]()  # KeyError if a catalogued rule has no conformance check


def test_every_catalogued_rule_has_a_conformance_check():
    assert set(CONFORMANCE) == {rule.id for rule in RULES}


def test_rules_md_matches_catalog():
    rules_md = Path(__file__).resolve().parents[1] / "RULES.md"
    committed = rules_md.read_text(encoding="utf-8")
    assert committed == render_rules_md(), (
        "RULES.md is stale; run `python scripts/gen_rules.py --write`"
    )
