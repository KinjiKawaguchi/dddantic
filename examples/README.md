# Examples

## shop

An e-commerce domain spanning **three bounded contexts** and **five aggregate roots**,
exercising every dddantic building block. Each context is its own module that declares
its context once at the top with `__bounded_context__ = "..."` — every element in the
module joins it, no per-class decorators:

| Context | File | Aggregate roots | Notable elements |
|---|---|---|---|
| `catalog` | [`shop/catalog.py`](shop/catalog.py) | `Product` | `Money`, `Affordable` (spec) |
| `ordering` | [`shop/ordering.py`](shop/ordering.py) | `Customer`, `Order` | `OrderPlaced` (event), `HighValueOrder` (spec), `OrderFactory`, `CheckoutService` |
| `fulfillment` | [`shop/fulfillment.py`](shop/fulfillment.py) | `StockItem`, `Shipment` | `ShipmentDispatched` (event) |
| _(shared kernel)_ | [`shop/shared.py`](shop/shared.py) | — | `Money` — used by `catalog` and `ordering` |

`shop/shared.py` declares no `__bounded_context__`, so `Money` belongs to no single
context: the diagram draws it outside every namespace with composition edges crossing in
from each context that uses it.

Cross-context links are by identity only, which is what makes the context map
meaningful:

- `ordering` → `catalog` (`OrderLine.product: ProductId`)
- `fulfillment` → `catalog` (`StockItem.product: ProductId`)
- `fulfillment` → `ordering` (`Shipment.order: OrderId`)

Run it to place an order and print the context map and a per-context class diagram:

```bash
python -m examples.shop.render
```

The diagrams are also committed at [`shop/diagram.md`](shop/diagram.md) (rendered by
GitHub): a context map, a single grouped overview of the whole model (one Mermaid
`namespace` per context), and one class diagram per context. Regenerate after changing
the domain, or CI will fail:

```bash
python -m examples.shop.diagram --write   # update shop/diagram.md
python -m examples.shop.diagram --check   # what CI runs
```
