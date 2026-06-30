import pytest

from dddantic import default_registry


@pytest.fixture(autouse=True)
def _clean_registry():
    """各テストの前後でグローバルレジストリを空にし、テスト間を隔離する。"""
    default_registry.clear()
    yield
    default_registry.clear()
