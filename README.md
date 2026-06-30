# dddantic

> ⚠️ Early development (alpha). The API is not yet stable.

A Pydantic-based library that provides the tactical building blocks of DDD
(Domain-Driven Design) as **typed components**. It enforces DDD invariants on each
element and analyzes the models you define to **generate model diagrams (Mermaid)
and context maps**.

## Features

- **Base models for DDD elements** — `Entity` / `ValueObject` / `AggregateRoot` /
  `DomainEvent` and more, provided as Pydantic models.
- **Invariant enforcement** — DDD constraints are checked at class-definition time:
  value objects are immutable with value equality, entities use identity-based
  equality, and aggregates may reference other aggregates by ID only.
- **Analysis and diagramming** — introspects the defined elements and emits their
  composition and reference relationships as a Mermaid class diagram.
- **Pydantic v1 / v2 dual support** — adopt it against whichever version your
  existing assets use.

## Installation

```bash
pip install dddantic   # once published
```

## Example (planned API)

```python
from dddantic import ValueObject, Entity, AggregateRoot

class Money(ValueObject):
    amount: int
    currency: str          # immutable, value equality; cannot hold an identifier

class OrderId(ValueObject):
    value: str

class Order(AggregateRoot):
    id: OrderId            # equality by identity
    total: Money           # an aggregate composes VOs / child entities; other aggregates by ID only
```

See [CLAUDE.md](CLAUDE.md) for the detailed design rationale.

## Development

```bash
uv sync
uv run pytest
uv run ruff check src/ tests/
uv run pyrefly check src/
```

## License

MIT
