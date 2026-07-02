"""The catalog of DDD rules dddantic detects.

This is the single source of truth for the library's "DDD linter" facet: every rule the
library enforces is listed here with the DDD source it derives from. ``RULES.md`` is
generated from this catalog and ``tests/test_rules_conformance.py`` verifies that each
rule is actually detected — so the documented rule set, the enforced rule set, and the
cited sources never drift apart.

Provenance is stated honestly: ``Grounding.STATED`` means the source states the rule;
``Grounding.INTERPRETED`` means the rule is dddantic's enforcement/interpretation of a
cited principle, not a verbatim quote (so it is more open to reasonable disagreement).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

_EVANS = "Evans, Domain-Driven Design (2003)"
_VERNON = "Vernon, Implementing Domain-Driven Design (2013)"


class Grounding(str, Enum):
    """How closely a rule follows its cited source."""

    STATED = "stated"
    INTERPRETED = "interpreted"


@dataclass(frozen=True)
class Rule:
    """A single DDD rule the library detects."""

    id: str
    title: str
    statement: str
    source: str
    grounding: Grounding


RULES: tuple[Rule, ...] = (
    Rule(
        id="ENTITY-IDENTITY",
        title="Entities are defined by identity",
        statement=(
            "An Entity requires an identity field; equality and hashing depend only on "
            "identity, never on attribute values."
        ),
        source=f"{_EVANS}, Ch. 5 — Entities (a thread of continuity and identity).",
        grounding=Grounding.STATED,
    ),
    Rule(
        id="VO-IMMUTABLE",
        title="Value objects are immutable and compared by value",
        statement=(
            "A ValueObject has no conceptual identity: it is immutable and two instances "
            "with equal attributes are equal and hash alike."
        ),
        source=f"{_EVANS}, Ch. 5 — Value Objects (treat as immutable; equality by value).",
        grounding=Grounding.STATED,
    ),
    Rule(
        id="VO-NO-MUTABLE-CONTAINER",
        title="Value objects hold no mutable containers",
        statement=(
            "A ValueObject may not declare list/set/dict fields; use tuple/frozenset so "
            "the object stays immutable and hashable."
        ),
        source=f"{_EVANS}, Ch. 5 — Value Objects (immutability); enforcement is dddantic's.",
        grounding=Grounding.INTERPRETED,
    ),
    Rule(
        id="ID-SINGLE-VALUE",
        title="Identity is modelled as a single-value Value Object",
        statement="An Identifier is a ValueObject that carries exactly one field.",
        source=(
            f"{_VERNON}, Ch. 5 — model identity as a Value Object; "
            "single-field is dddantic's reading."
        ),
        grounding=Grounding.INTERPRETED,
    ),
    Rule(
        id="AGG-REF-BY-ID",
        title="Reference other aggregates by identity",
        statement=(
            "An AggregateRoot must not hold another aggregate as an instance; it may only "
            "reference it by that aggregate's Identifier."
        ),
        source=f"{_VERNON}, Ch. 10 — Reference Other Aggregates by Identity.",
        grounding=Grounding.STATED,
    ),
    Rule(
        id="REPO-FOR-AGG-ROOT",
        title="Repositories are provided only for aggregate roots",
        statement="A Repository's type parameter must be an AggregateRoot subclass.",
        source=f"{_EVANS}, Ch. 6 — provide Repositories only for Aggregate roots.",
        grounding=Grounding.STATED,
    ),
    Rule(
        id="EVENT-IMMUTABLE-OCCURRED",
        title="Domain events are immutable and record when they occurred",
        statement=(
            "A DomainEvent is an immutable value object carrying an occurred_on timestamp."
        ),
        source=f"{_VERNON}, Ch. 8 — Domain Events; Fowler, Domain Event (2005).",
        grounding=Grounding.STATED,
    ),
)


def rules() -> tuple[Rule, ...]:
    """Return the catalog of DDD rules the library detects."""
    return RULES


def render_rules_md() -> str:
    """Render ``RULES.md`` from the catalog. The committed file must equal this output."""
    regen = (
        '`python -c "from dddantic.rules import render_rules_md as r; '
        "open('RULES.md','w').write(r())\"`"
    )
    lines = [
        "# DDD rules dddantic detects",
        "",
        f"Generated from `dddantic.rules`. Do not edit by hand — run {regen}.",
        "",
        "`stated` = the source states the rule; "
        "`interpreted` = dddantic's enforcement of a cited principle.",
        "",
        "| ID | Rule | Grounding | Source |",
        "|---|---|---|---|",
    ]
    lines += [f"| `{r.id}` | {r.title} | {r.grounding.value} | {r.source} |" for r in RULES]
    lines.append("")
    for r in RULES:
        lines += [f"## {r.id} — {r.title}", "", r.statement, "", f"> {r.source}", ""]
    return "\n".join(lines).rstrip() + "\n"
