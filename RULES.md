# DDD rules dddantic detects

Generated from `dddantic.rules`. Do not edit by hand — run `python -c "from dddantic.rules import render_rules_md as r; open('RULES.md','w').write(r())"`.

`stated` = the source states the rule; `interpreted` = dddantic's enforcement of a cited principle.

| ID | Rule | Grounding | Source |
|---|---|---|---|
| `ENTITY-IDENTITY` | Entities are defined by identity | stated | Evans, Domain-Driven Design (2003), Ch. 5 — Entities (a thread of continuity and identity). |
| `VO-IMMUTABLE` | Value objects are immutable and compared by value | stated | Evans, Domain-Driven Design (2003), Ch. 5 — Value Objects (treat as immutable; equality by value). |
| `VO-NO-MUTABLE-CONTAINER` | Value objects hold no mutable containers | interpreted | Evans, Domain-Driven Design (2003), Ch. 5 — Value Objects (immutability); enforcement is dddantic's. |
| `ID-SINGLE-VALUE` | Identity is modelled as a single-value Value Object | interpreted | Vernon, Implementing Domain-Driven Design (2013), Ch. 5 — model identity as a Value Object; single-field is dddantic's reading. |
| `AGG-REF-BY-ID` | Reference other aggregates by identity | stated | Vernon, Implementing Domain-Driven Design (2013), Ch. 10 — Reference Other Aggregates by Identity. |
| `REPO-FOR-AGG-ROOT` | Repositories are provided only for aggregate roots | stated | Evans, Domain-Driven Design (2003), Ch. 6 — provide Repositories only for Aggregate roots. |
| `EVENT-IMMUTABLE-OCCURRED` | Domain events are immutable and record when they occurred | stated | Vernon, Implementing Domain-Driven Design (2013), Ch. 8 — Domain Events; Fowler, Domain Event (2005). |

## ENTITY-IDENTITY — Entities are defined by identity

An Entity requires an identity field; equality and hashing depend only on identity, never on attribute values.

> Evans, Domain-Driven Design (2003), Ch. 5 — Entities (a thread of continuity and identity).

## VO-IMMUTABLE — Value objects are immutable and compared by value

A ValueObject has no conceptual identity: it is immutable and two instances with equal attributes are equal and hash alike.

> Evans, Domain-Driven Design (2003), Ch. 5 — Value Objects (treat as immutable; equality by value).

## VO-NO-MUTABLE-CONTAINER — Value objects hold no mutable containers

A ValueObject may not declare list/set/dict fields; use tuple/frozenset so the object stays immutable and hashable.

> Evans, Domain-Driven Design (2003), Ch. 5 — Value Objects (immutability); enforcement is dddantic's.

## ID-SINGLE-VALUE — Identity is modelled as a single-value Value Object

An Identifier is a ValueObject that carries exactly one field.

> Vernon, Implementing Domain-Driven Design (2013), Ch. 5 — model identity as a Value Object; single-field is dddantic's reading.

## AGG-REF-BY-ID — Reference other aggregates by identity

An AggregateRoot must not hold another aggregate as an instance; it may only reference it by that aggregate's Identifier.

> Vernon, Implementing Domain-Driven Design (2013), Ch. 10 — Reference Other Aggregates by Identity.

## REPO-FOR-AGG-ROOT — Repositories are provided only for aggregate roots

A Repository's type parameter must be an AggregateRoot subclass.

> Evans, Domain-Driven Design (2003), Ch. 6 — provide Repositories only for Aggregate roots.

## EVENT-IMMUTABLE-OCCURRED — Domain events are immutable and record when they occurred

A DomainEvent is an immutable value object carrying an occurred_on timestamp.

> Vernon, Implementing Domain-Driven Design (2013), Ch. 8 — Domain Events; Fowler, Domain Event (2005).
