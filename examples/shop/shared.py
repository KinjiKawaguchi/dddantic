"""Shared kernel: value objects used across more than one bounded context.

This module deliberately declares no ``__bounded_context__``. Elements here belong to
no single context, so the diagram renders them outside every context namespace with
edges crossing in from each context that uses them — the shared-kernel picture.
"""

from __future__ import annotations

from dddantic import ValueObject


class Money(ValueObject):
    amount: int
    currency: str
