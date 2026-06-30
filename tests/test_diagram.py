from dddantic import (
    AggregateRoot,
    Identifier,
    ValueObject,
    bounded_context,
    default_registry,
    diagram,
)


def _build_domain():
    class Money(ValueObject):
        amount: int
        currency: str

    class CustomerId(Identifier):
        value: int

    class OrderId(Identifier):
        value: int

    class Customer(AggregateRoot[CustomerId]):
        name: str

    class Order(AggregateRoot[OrderId]):
        customer_id: CustomerId
        total: Money

    return {"Customer": Customer, "Order": Order}


def test_mermaid_header_and_stereotypes():
    _build_domain()
    out = diagram.to_mermaid()
    assert out.startswith("classDiagram")
    assert "<<AggregateRoot>>" in out
    assert "<<ValueObject>>" in out
    assert "<<Identifier>>" in out


def test_mermaid_composition_edge():
    _build_domain()
    assert "Order *-- Money" in diagram.to_mermaid()


def test_mermaid_reference_edge():
    _build_domain()
    assert "Order ..> Customer : ref" in diagram.to_mermaid()


def test_within_filters_by_context():
    domain = _build_domain()
    bounded_context("sales")(domain["Order"])
    out = diagram.to_mermaid(within="sales")
    assert "class Order {" in out
    assert "class Customer {" not in out


def test_explicit_registry_argument():
    _build_domain()
    out = diagram.to_mermaid(registry=default_registry)
    assert "class Order {" in out
