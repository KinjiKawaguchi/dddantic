from dddantic import AggregateRoot, Identifier, bounded_context, default_registry


def test_decorator_sets_context_and_updates_registry():
    class FooId(Identifier):
        value: int

    @bounded_context("ordering")
    class Foo(AggregateRoot[FooId]):
        n: int

    assert Foo.__dddantic_context__ == "ordering"
    info = default_registry.info_for(Foo)
    assert info is not None
    assert info.bounded_context == "ordering"


def test_decorator_on_unregistered_class():
    @bounded_context("ordering")
    class Plain:
        pass

    assert Plain.__dddantic_context__ == "ordering"
    assert default_registry.info_for(Plain) is None
