"""Catalog bounded context: the products a shop sells."""

from __future__ import annotations

from dddantic import (
    AggregateRoot,
    Identifier,
    Repository,
    Specification,
    ValueObject,
    bounded_context,
)


@bounded_context("catalog")
class Money(ValueObject):
    amount: int
    currency: str


@bounded_context("catalog")
class ProductId(Identifier):
    value: str


@bounded_context("catalog")
class Product(AggregateRoot[ProductId]):
    name: str
    price: Money
    in_stock: bool


@bounded_context("catalog")
class Affordable(Specification[Product]):
    """Products at or below a budget."""

    def __init__(self, budget: int) -> None:
        self.budget = budget

    def is_satisfied_by(self, candidate: Product) -> bool:
        return candidate.price.amount <= self.budget


@bounded_context("catalog")
class ProductRepository(Repository[Product]):
    def __init__(self) -> None:
        self._items: dict[str, Product] = {}

    def add(self, product: Product) -> None:
        self._items[product.id.value] = product

    def get(self, product_id: ProductId) -> Product:
        return self._items[product_id.value]
