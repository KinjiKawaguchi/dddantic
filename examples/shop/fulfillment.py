"""Fulfillment bounded context: stock levels and shipments.

Depends on both catalog (`ProductId`) and ordering (`OrderId`), referenced by identity
only — making fulfillment downstream of both in the context map.
"""

from __future__ import annotations

from datetime import datetime

from dddantic import (
    AggregateRoot,
    DomainEvent,
    Identifier,
    Repository,
    bounded_context,
)
from examples.shop.catalog import ProductId
from examples.shop.ordering import OrderId


@bounded_context("fulfillment")
class StockItemId(Identifier):
    value: str


@bounded_context("fulfillment")
class StockItem(AggregateRoot[StockItemId]):
    product: ProductId  # cross-context identity reference → catalog
    on_hand: int


@bounded_context("fulfillment")
class ShipmentId(Identifier):
    value: str


@bounded_context("fulfillment")
class ShipmentDispatched(DomainEvent):
    occurred_on: datetime
    shipment_id: str


@bounded_context("fulfillment")
class Shipment(AggregateRoot[ShipmentId]):
    order: OrderId  # cross-context identity reference → ordering
    dispatched: bool


@bounded_context("fulfillment")
class StockItemRepository(Repository[StockItem]):
    def __init__(self) -> None:
        self._items: dict[str, StockItem] = {}

    def add(self, item: StockItem) -> None:
        self._items[item.id.value] = item

    def get(self, item_id: StockItemId) -> StockItem:
        return self._items[item_id.value]


@bounded_context("fulfillment")
class ShipmentRepository(Repository[Shipment]):
    def __init__(self) -> None:
        self._shipments: dict[str, Shipment] = {}

    def add(self, shipment: Shipment) -> None:
        self._shipments[shipment.id.value] = shipment

    def get(self, shipment_id: ShipmentId) -> Shipment:
        return self._shipments[shipment_id.value]
