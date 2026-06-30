"""Run the shop domain end-to-end and print its diagrams.

Run from the repository root:

    python -m examples.shop.render
"""

from __future__ import annotations

from datetime import datetime, timezone

from dddantic import diagram
from examples.shop import domain  # noqa: F401  registers every context
from examples.shop.catalog import Money, Product, ProductId, ProductRepository
from examples.shop.fulfillment import StockItem, StockItemId, StockItemRepository
from examples.shop.ordering import (
    CheckoutService,
    CustomerId,
    HighValueOrder,
    OrderFactory,
    OrderId,
    OrderLine,
    OrderRepository,
)


def main() -> None:
    products = ProductRepository()
    book = Product(
        id=ProductId(value="BOOK-1"),
        name="Domain-Driven Design",
        price=Money(amount=5000, currency="JPY"),
        in_stock=True,
    )
    products.add(book)

    stock = StockItemRepository()
    stock.add(StockItem(id=StockItemId(value="STK-1"), product=book.id, on_hand=12))

    orders = OrderRepository()
    checkout = CheckoutService(orders, OrderFactory())
    line = OrderLine(product=book.id, quantity=2, unit_price=book.price)
    order = checkout.checkout(
        OrderId(value="ORD-1"),
        CustomerId(value="CUST-1"),
        (line,),
        now=datetime(2026, 6, 30, tzinfo=timezone.utc),
    )

    print(f"placed order {order.id.value}, total={order.total}")
    print(f"pending events: {[type(e).__name__ for e in order.pending_events]}")
    print(f"high-value (>= 8000)? {HighValueOrder(8000).is_satisfied_by(order)}")
    print(f"persisted: {orders.get(order.id) is order}")

    print("\n--- Context map ---")
    print(diagram.to_context_map())
    print("\n--- Overview (all contexts) ---")
    print(diagram.to_mermaid(group_by_context=True))


if __name__ == "__main__":
    main()
