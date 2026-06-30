from dddantic import DomainService, Factory, default_registry


def test_domain_service_registered():
    class Pricing(DomainService):
        def total(self, *amounts: int) -> int:
            return sum(amounts)

    info = default_registry.info_for(Pricing)
    assert info is not None
    assert info.kind == "domain_service"
    assert Pricing().total(1, 2, 3) == 6


def test_factory_registered():
    class WidgetFactory(Factory):
        def create(self) -> str:
            return "widget"

    info = default_registry.info_for(WidgetFactory)
    assert info is not None
    assert info.kind == "factory"
    assert WidgetFactory().create() == "widget"
