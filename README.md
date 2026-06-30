# dddantic

> ⚠️ Early development (alpha). The API is not yet stable.

A Pydantic-based library that provides the tactical building blocks of DDD
(Domain-Driven Design) as **typed components**. It enforces DDD invariants on each
element and analyzes the models you define to **generate model diagrams (Mermaid)
and context maps**.

## Features

- **A base for every tactical pattern** — data elements (`ValueObject`, `Identifier`,
  `Entity`, `AggregateRoot`, `DomainEvent`) as Pydantic models, and behavior elements
  (`Specification`, `Repository`, `DomainService`, `Factory`) as plain typed bases.
- **Invariant enforcement at class-definition time** — value objects are immutable
  with value equality, entities use identity-based equality, aggregates reference other
  aggregates by ID only, and a repository's type parameter must be an aggregate root.
- **Analysis and diagramming** — introspects the registered elements and emits their
  composition and reference relationships (including repository → aggregate and
  specification → candidate) as a Mermaid class diagram, optionally per bounded context.
- **Pydantic v1 / v2 dual support** — adopt it against whichever version your existing
  assets use.

## Building blocks

| Pattern | Base | Enforced invariant |
|---|---|---|
| Value Object | `ValueObject` | immutable, value equality, no mutable containers |
| Identifier | `Identifier` | single-field value object |
| Entity | `Entity[TId]` | `id` required; equality/hash by identity |
| Aggregate Root | `AggregateRoot[TId]` | other aggregates by ID only; accumulates events |
| Domain Event | `DomainEvent` | immutable + `occurred_on` |
| Specification | `Specification[T]` | `is_satisfied_by`, composable with `&` `\|` `~` |
| Repository | `Repository[TRoot]` | `TRoot` must be an `AggregateRoot` |
| Domain Service | `DomainService` | marker (registry / diagram participation) |
| Factory | `Factory` | marker (registry / diagram participation) |

## Installation

```bash
pip install dddantic   # once published
```

## Example

```python
from dddantic import AggregateRoot, Identifier, Repository, Specification, ValueObject

class Money(ValueObject):
    amount: int
    currency: str          # immutable, value equality; cannot hold an identifier

class OrderId(Identifier):
    value: str             # single-value identity

class Order(AggregateRoot[OrderId]):
    total: Money           # composes VOs / child entities; other aggregates by ID only

class HighValueOrder(Specification[Order]):
    def is_satisfied_by(self, candidate: Order) -> bool:
        return candidate.total.amount >= 10_000

class OrderRepository(Repository[Order]):   # TRoot must be an AggregateRoot
    ...
```

See [CLAUDE.md](CLAUDE.md) for the detailed design rationale.

## Examples

[`examples/shop`](examples/shop) is a runnable e-commerce domain spanning three bounded
contexts and five aggregate roots that exercises every building block. It prints a
context map and per-context class diagrams (also committed at
[`examples/shop/diagram.md`](examples/shop/diagram.md)):

```bash
python -m examples.shop.render
```

## Development

```bash
uv sync
uv run pytest
uv run ruff check src/ tests/
uv run pyrefly check src/
```

## License

MIT
