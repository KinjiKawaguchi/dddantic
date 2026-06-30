"""Ordering bounded context: customers placing orders.

References the catalog context by identity only (`ProductId`), never by importing the
`Product` aggregate itself — the rule dddantic enforces for aggregates.
"""

from __future__ import annotations

from datetime import datetime

from dddantic import (
    AggregateRoot,
    DomainEvent,
    DomainService,
    Factory,
    Identifier,
    Repository,
    Specification,
    ValueObject,
    bounded_context,
)
from examples.shop.catalog import Money, ProductId


@bounded_context("ordering")
class CustomerId(Identifier):
    value: str


@bounded_context("ordering")
class Customer(AggregateRoot[CustomerId]):
    name: str
    email: str


@bounded_context("ordering")
class OrderId(Identifier):
    value: str


@bounded_context("ordering")
class OrderLine(ValueObject):
    product: ProductId  # cross-context identity reference → catalog
    quantity: int
    unit_price: Money


@bounded_context("ordering")
class OrderPlaced(DomainEvent):
    occurred_on: datetime
    order_id: str


@bounded_context("ordering")
class Order(AggregateRoot[OrderId]):
    customer: CustomerId  # same-context identity reference
    lines: tuple[OrderLine, ...]

    @property
    def total(self) -> int:
        return sum(line.quantity * line.unit_price.amount for line in self.lines)


@bounded_context("ordering")
class HighValueOrder(Specification[Order]):
    """Orders whose total is at or above a threshold."""

    def __init__(self, threshold: int) -> None:
        self.threshold = threshold

    def is_satisfied_by(self, candidate: Order) -> bool:
        return candidate.total >= self.threshold


@bounded_context("ordering")
class OrderRepository(Repository[Order]):
    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}

    def add(self, order: Order) -> None:
        self._orders[order.id.value] = order

    def get(self, order_id: OrderId) -> Order:
        return self._orders[order_id.value]


@bounded_context("ordering")
class CustomerRepository(Repository[Customer]):
    def __init__(self) -> None:
        self._customers: dict[str, Customer] = {}

    def add(self, customer: Customer) -> None:
        self._customers[customer.id.value] = customer

    def get(self, customer_id: CustomerId) -> Customer:
        return self._customers[customer_id.value]


@bounded_context("ordering")
class OrderFactory(Factory):
    """Assembles a valid order together with its placed event."""

    def place(
        self,
        order_id: OrderId,
        customer: CustomerId,
        lines: tuple[OrderLine, ...],
        *,
        now: datetime,
    ) -> Order:
        order = Order(id=order_id, customer=customer, lines=lines)
        order.register_event(OrderPlaced(occurred_on=now, order_id=order_id.value))
        return order


@bounded_context("ordering")
class CheckoutService(DomainService):
    """Coordinates the factory and repository to place and persist an order."""

    def __init__(self, orders: OrderRepository, factory: OrderFactory) -> None:
        self._orders = orders
        self._factory = factory

    def checkout(
        self,
        order_id: OrderId,
        customer: CustomerId,
        lines: tuple[OrderLine, ...],
        *,
        now: datetime,
    ) -> Order:
        order = self._factory.place(order_id, customer, lines, now=now)
        self._orders.add(order)
        return order
