from typing import TypeVar

from dddantic.building_blocks import _introspect


class _Sample:
    pass


def test_referenced_types_bare_class():
    assert _introspect.referenced_types(_Sample) == (_Sample,)


def test_referenced_types_optional():
    assert _introspect.referenced_types(_Sample | None) == (_Sample,)


def test_referenced_types_list():
    assert _introspect.referenced_types(list[_Sample]) == (_Sample,)


def test_referenced_types_dict():
    assert set(_introspect.referenced_types(dict[str, _Sample])) == {str, _Sample}


def test_referenced_types_non_type_returns_empty():
    t = TypeVar("t")
    assert _introspect.referenced_types(t) == ()


def test_has_mutable_container_bare():
    assert _introspect.has_mutable_container(list)
    assert _introspect.has_mutable_container(set)
    assert _introspect.has_mutable_container(dict)


def test_has_mutable_container_parameterized():
    assert _introspect.has_mutable_container(list[int])


def test_has_mutable_container_immutable():
    assert not _introspect.has_mutable_container(tuple)
    assert not _introspect.has_mutable_container(int)


def test_type_label_class():
    assert _introspect.type_label(int) == "int"


def test_type_label_generic():
    assert _introspect.type_label(list[int]) == "list~int~"
