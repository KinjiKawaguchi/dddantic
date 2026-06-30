import pytest

from dddantic import Identifier, ValueObject
from dddantic._compat import FROZEN_VIOLATION_ERRORS


class Money(ValueObject):
    amount: int
    currency: str


def test_value_equality():
    assert Money(amount=1, currency="JPY") == Money(amount=1, currency="JPY")


def test_value_inequality():
    assert Money(amount=1, currency="JPY") != Money(amount=2, currency="JPY")


def test_hashable_dedup():
    pair = {Money(amount=1, currency="JPY"), Money(amount=1, currency="JPY")}
    assert len(pair) == 1


def test_frozen():
    money = Money(amount=1, currency="JPY")
    with pytest.raises(FROZEN_VIOLATION_ERRORS):
        money.amount = 2


def test_mutable_list_field_rejected():
    with pytest.raises(TypeError):

        class BadList(ValueObject):
            items: list


def test_mutable_dict_field_rejected():
    with pytest.raises(TypeError):

        class BadDict(ValueObject):
            mapping: dict


def test_parameterized_mutable_field_rejected():
    with pytest.raises(TypeError):

        class BadParam(ValueObject):
            items: list[int]


def test_identifier_single_field():
    class UserId(Identifier):
        value: int

    assert UserId(value=1) == UserId(value=1)


def test_identifier_multi_field_rejected():
    with pytest.raises(TypeError):

        class BadId(Identifier):
            left: int
            right: int
