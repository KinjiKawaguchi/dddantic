from typing import TypeVar

from dddantic import _compat


def test_pydantic_v1_flag_is_bool():
    assert isinstance(_compat.PYDANTIC_V1, bool)


def test_is_unresolved_typevar():
    t = TypeVar("t")
    assert _compat.is_unresolved(t) is True


def test_is_unresolved_concrete():
    assert _compat.is_unresolved(int) is False


def test_translate_config_frozen():
    cfg = _compat.translate_config({"frozen": True})
    assert cfg["frozen"] is True


def test_translate_config_validate_assignment():
    cfg = _compat.translate_config({"validate_assignment": True})
    assert cfg["validate_assignment"] is True


def test_translate_config_empty():
    assert _compat.translate_config({}) == {}


def test_frozen_violation_errors_is_tuple():
    assert isinstance(_compat.FROZEN_VIOLATION_ERRORS, tuple)
    assert all(issubclass(e, Exception) for e in _compat.FROZEN_VIOLATION_ERRORS)
