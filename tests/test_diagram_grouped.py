from dddantic import AggregateRoot, Identifier, ValueObject, bounded_context, diagram


def _build() -> None:
    @bounded_context("catalog")
    class ProductId(Identifier):
        value: int

    @bounded_context("catalog")
    class Product(AggregateRoot[ProductId]):
        name: str

    @bounded_context("ordering")
    class OrderId(Identifier):
        value: int

    @bounded_context("ordering")
    class Line(ValueObject):
        product: ProductId

    @bounded_context("ordering")
    class Order(AggregateRoot[OrderId]):
        line: Line


def test_grouped_overview_wraps_contexts_in_namespaces():
    _build()
    out = diagram.to_mermaid(group_by_context=True)
    assert out.startswith("classDiagram")
    assert "namespace catalog {" in out
    assert "namespace ordering {" in out
    # Classes still present, and the cross-context edge is drawn at top level.
    assert "class Product {" in out
    assert "Line ..> Product : ref" in out


def test_default_is_flat():
    _build()
    out = diagram.to_mermaid()
    assert "namespace" not in out


def test_within_ignores_grouping():
    _build()
    out = diagram.to_mermaid(within="catalog", group_by_context=True)
    assert "namespace" not in out
    assert "class Product {" in out
    assert "class Order {" not in out
