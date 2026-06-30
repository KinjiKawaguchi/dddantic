"""要素種別と内部マーカー属性の定数。

具象クラスを import せず文字列 kind で種別を扱うことで、registry と
building_blocks の循環依存を避ける。
"""

KIND_VALUE_OBJECT = "value_object"
KIND_IDENTIFIER = "identifier"
KIND_ENTITY = "entity"
KIND_AGGREGATE = "aggregate"
KIND_DOMAIN_EVENT = "domain_event"

ATTR_KIND = "__dddantic_kind__"
ATTR_BASE = "__dddantic_base__"
ATTR_CONFIG = "__dddantic_config__"
ATTR_CONTEXT = "__dddantic_context__"
ATTR_IDENTITY_ALIAS = "__identity_alias__"
