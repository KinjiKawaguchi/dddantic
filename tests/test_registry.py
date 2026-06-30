from dddantic.registry import ElementInfo, Registry


def _info(cls: type, kind: str = "entity") -> ElementInfo:
    return ElementInfo(cls=cls, kind=kind, name=cls.__name__, module="m", bounded_context=None)


def test_register_and_query():
    registry = Registry()
    info = _info(int)
    registry.register(info)
    assert registry.elements() == (info,)
    assert registry.info_for(int) is info


def test_info_for_missing():
    assert Registry().info_for(int) is None


def test_id_type_mapping():
    registry = Registry()
    registry.register_id_type(str, list)
    assert registry.aggregate_for_id_type(str) is list
    assert registry.aggregate_for_id_type(int) is None


def test_clear():
    registry = Registry()
    registry.register(_info(int))
    registry.register_id_type(str, list)
    registry.clear()
    assert registry.elements() == ()
    assert registry.aggregate_for_id_type(str) is None
