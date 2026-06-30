# dddantic — Project Instructions

A library that provides the tactical design building blocks of DDD
(Entity / ValueObject / AggregateRoot / DomainEvent ...) as typed components built on
Pydantic. It enforces DDD invariants on each element and analyzes the defined models to
generate model diagrams (Mermaid) and context maps.

This document records **design decisions** and **intent that cannot be recovered from
code alone**. For usage instructions aimed at users, see [README.md](README.md).

> Status: v0.1 implemented — all tactical building blocks (ValueObject, Identifier, Entity, AggregateRoot, DomainEvent, Specification, Repository, DomainService, Factory), the registry, and Mermaid diagramming. Module is intentionally not a class (covered by package layout + `@bounded_context`). The following are the finalized design decisions behind the implementation.

## Finalized Design Decisions

### Dual Pydantic v1 / v2 Support

We value being able to adopt this library even in legacy assets (projects still on v1).
The v1/v2 API differences (`model_config`/`Config`, `model_fields`/`__fields__`,
`frozen`/`allow_mutation`, etc.) are **confined to a thin compatibility shim
`_compat.py`**, and the core logic stays unified. Version branching is driven by
`pydantic.VERSION`.

Supported Python is 3.10–3.14. CI continuously validates both lineages with a matrix of
python × pydantic{v1,v2} (`.github/workflows/ci.yml`). However, since pydantic v1 does
not support 3.13+, the v1 legs are limited to 3.12 (3.13/3.14 run v2 only).

### Constraint Violations Raise at Class-Definition Time

Each element's invariants are checked in `__init_subclass__`, and a violation raises
`TypeError` **immediately at class-definition time**. We choose fail-fast over lint-like
deferred reporting, so that incorrect model definitions are never left in the repository.

### Base Classes Primary, Decorators Secondary

Behavior, constraints, and IDE completion are provided by base classes (`ValueObject`,
etc.). Elements are **implicitly registered** in the registry via `__init_subclass__`, so
you do not have to sprinkle explicit decorators around for diagramming. Decorators only
supplement grouping concerns such as `@bounded_context`.

### Data Blocks Are Pydantic, Behavior Blocks Are Plain Classes

The tactical patterns split in two. **Data** blocks (ValueObject, Identifier, Entity,
AggregateRoot, DomainEvent) are Pydantic models, built through `DddanticMeta` (a
`ModelMetaclass` subclass) because their invariants depend on the constructed fields.
**Behavior** blocks (Specification, Repository, DomainService, Factory) are interfaces
and operations with no data shape, so forcing them into `BaseModel` would be a poor fit;
they are plain classes that self-register and run their checks via `__init_subclass__`
on `BehaviorBlock`. Both kinds populate the same `registry`, so diagramming and context
maps treat every element uniformly. This works cleanly because `registry` is
pydantic-agnostic (dependency direction is building_blocks → registry, never the reverse).

### Separation of Concerns

"Constraint enforcement" and "metadata collection / analysis" are kept as independent
concerns, including internally.

```
building_blocks/  data blocks (value_object, entity, aggregate, event) + behavior blocks
                  (specification, repository, service, factory); _meta/_behavior wire
                  registration, _checks holds invariants, _introspect/_kinds are helpers
registry/         Element registration and lookup (pydantic-agnostic leaf)
diagram/          Mermaid output (PlantUML in the future)
_compat.py        Absorbs pydantic v1/v2 differences (leaf module)
```

## Per-Element Constraints (Implementation Policy)

- **ValueObject**: Immutable, value equality, hashable (v2 `frozen=True` / v1 `allow_mutation=False`). Identifier fields forbidden.
- **Entity**: `id` field required. Equality and hashing by id only (identity, not value).
- **AggregateRoot**: Aggregate boundary. References to other aggregates by ID only (cannot hold fields of another Entity type). Accumulates domain events.
- **DomainEvent**: Immutable + `occurred_on`. Treated as a value object.
- **Specification**: `is_satisfied_by` + composition via `&` / `|` / `~`. Internal combinators (`_And`/`_Or`/`_Not`) are not registered.
- **Repository**: Type parameter must be an AggregateRoot subclass, enforced at definition time. One repository per aggregate.
- **DomainService**: Stateless operation spanning multiple objects. Marker base; participates in registry/diagram.
- **Factory**: Encapsulates construction of a complex object. Marker base; participates in registry/diagram.
- **Module**: Not modeled as a class — package layout plus `@bounded_context` grouping covers it.

## Coding Principles (Project-Specific)

Only items that tools cannot enforce, or that override the global conventions, are listed
here. See `pyproject.toml` for the ruff / pyrefly configuration.

- **`Any` forbidden**: use `object` or a Protocol.
- **`# noqa` / `type: ignore` are a last resort**: resolve warnings by design. If you must use one, state the reason in the PR.
- v1/v2 branching must not leak outside `_compat.py`. Do not write `pydantic.VERSION` directly in the core code.

## Git / Release

- Conventional Commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`
- Direct push to main is forbidden.
- SemVer: before v1.0.0, `feat:` → minor, `fix:` → patch.
- Releases are automated via Release Please + PyPI Trusted Publisher (`.github/workflows/release.yml`).
