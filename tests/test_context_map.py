from dddantic import (
    AggregateRoot,
    Identifier,
    Repository,
    ValueObject,
    bounded_context,
    diagram,
)


def _build_two_contexts() -> None:
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
        product: ProductId  # cross-context identity reference

    @bounded_context("ordering")
    class Order(AggregateRoot[OrderId]):
        line: Line

    @bounded_context("ordering")
    class OrderRepository(Repository[Order]):
        pass


def test_context_map_lists_contexts():
    _build_two_contexts()
    out = diagram.to_context_map()
    assert out.startswith("graph LR")
    assert 'catalog["catalog"]' in out
    assert 'ordering["ordering"]' in out


def test_context_map_draws_cross_context_dependency():
    _build_two_contexts()
    out = diagram.to_context_map()
    # ordering references a catalog aggregate by id → ordering depends on catalog.
    assert "ordering --> catalog" in out
    # No spurious reverse edge.
    assert "catalog --> ordering" not in out


def test_context_map_no_self_dependency():
    @bounded_context("solo")
    class ThingId(Identifier):
        value: int

    @bounded_context("solo")
    class Thing(AggregateRoot[ThingId]):
        n: int

    out = diagram.to_context_map()
    assert "solo --> solo" not in out
