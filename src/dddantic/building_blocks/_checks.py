"""Check DDD element invariants at class-definition time.

Each check raises ``TypeError`` on violation (fail fast). Rationale for principles
is documented in docstrings and error messages.
"""

from __future__ import annotations

from dddantic._compat import field_annotations, is_unresolved
from dddantic.building_blocks._introspect import (
    has_mutable_container,
    referenced_types,
)
from dddantic.building_blocks._kinds import ATTR_KIND, KIND_AGGREGATE


def check_value_object(cls: type) -> None:
    """ValueObject must be immutable and hashable. Cannot contain mutable containers."""
    for name, annotation in field_annotations(cls).items():
        if has_mutable_container(annotation):
            raise TypeError(
                f"{cls.__name__}.{name}: ValueObject must be immutable and hashable; "
                "cannot contain mutable containers (list/set/dict). Use tuple/frozenset instead."
            )


def check_identifier(cls: type) -> None:
    """Identifier is a ValueObject representing a single value."""
    check_value_object(cls)
    fields = field_annotations(cls)
    if len(fields) != 1:
        raise TypeError(
            f"{cls.__name__}: Identifier represents a single value; "
            f"must have exactly 1 field (currently {len(fields)})."
        )


def check_entity(cls: type) -> None:
    """Entity identity type must be bound (not unresolved)."""
    id_type = field_annotations(cls).get("id")
    if id_type is None:
        raise TypeError(f"{cls.__name__}: Entity must have an identity field 'id'.")
    if is_unresolved(id_type):
        raise TypeError(
            f"{cls.__name__}: specify identity type. "
            f"Example: class {cls.__name__}(AggregateRoot[{cls.__name__}Id])."
        )


def check_aggregate(cls: type) -> None:
    """Aggregate cannot hold other aggregates as instances (identity reference only)."""
    check_entity(cls)
    for name, annotation in field_annotations(cls).items():
        if name == "id":
            continue
        for referenced in referenced_types(annotation):
            if getattr(referenced, ATTR_KIND, None) == KIND_AGGREGATE:
                raise TypeError(
                    f"{cls.__name__}.{name}: cannot hold other aggregate "
                    f"{referenced.__name__} as instance. Reference by Identifier (id) instead "
                    "(Vernon: Reference Other Aggregates by Identity)."
                )
