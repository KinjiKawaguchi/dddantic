"""Catalog bounded context: the products a shop sells."""

from __future__ import annotations

from dddantic import AggregateRoot, Identifier, Repository, Specification
from examples.shop.shared import Money

__bounded_context__ = "catalog"


class ProductId(Identifier):
    value: str


class Product(AggregateRoot[ProductId]):
    name: str
    price: Money
    in_stock: bool


class Affordable(Specification[Product]):
    """Products at or below a budget."""

    def __init__(self, budget: int) -> None:
        self.budget = budget

    def is_satisfied_by(self, candidate: Product) -> bool:
        return candidate.price.amount <= self.budget


class ProductRepository(Repository[Product]):
    def __init__(self) -> None:
        self._items: dict[str, Product] = {}

    def add(self, product: Product) -> None:
        self._items[product.id.value] = product

    def get(self, product_id: ProductId) -> Product:
        return self._items[product_id.value]
