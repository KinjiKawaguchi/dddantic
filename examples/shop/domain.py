"""Shop domain aggregator.

Importing this module loads every bounded context, so all elements register with the
default registry (used by the diagram and context-map generators).
"""

from __future__ import annotations

from examples.shop import catalog, fulfillment, ordering  # noqa: F401  registers elements

CONTEXTS = ("catalog", "ordering", "fulfillment")
