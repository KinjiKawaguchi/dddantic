import pytest

from dddantic import AggregateRoot, Entity, Identifier


class UserId(Identifier):
    value: int


class User(Entity[UserId]):
    name: str


def test_identity_equality_ignores_attributes():
    uid = UserId(value=1)
    assert User(id=uid, name="a") == User(id=uid, name="b")


def test_identity_inequality():
    assert User(id=UserId(value=1), name="a") != User(id=UserId(value=2), name="a")


def test_hashable_by_identity():
    uid = UserId(value=1)
    assert len({User(id=uid, name="a"), User(id=uid, name="b")}) == 1


def test_entity_is_mutable():
    user = User(id=UserId(value=1), name="a")
    user.name = "b"
    assert user.name == "b"


def test_not_equal_to_other_entity_type():
    class OtherId(Identifier):
        value: int

    class Other(Entity[OtherId]):
        pass

    assert User(id=UserId(value=1), name="a") != Other(id=OtherId(value=1))


def test_not_equal_to_non_entity():
    assert User(id=UserId(value=1), name="a") != 42


def test_unparameterized_entity_rejected():
    with pytest.raises(TypeError):

        class Loose(Entity):
            x: int


def test_identity_alias():
    class BookId(Identifier):
        value: str

    class Book(AggregateRoot[BookId]):
        __identity_alias__ = "isbn"
        title: str

    book = Book(id=BookId(value="978"), title="t")
    assert book.isbn == book.id
