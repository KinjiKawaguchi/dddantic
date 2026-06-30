import pytest

from dddantic import default_registry


@pytest.fixture(autouse=True)
def _clean_registry():
    """Clear global registry before and after each test to isolate tests."""
    default_registry.clear()
    yield
    default_registry.clear()
