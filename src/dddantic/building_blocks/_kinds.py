"""Constants for element types and internal marker attributes.

Avoids circular dependency between registry and building_blocks by using string
kind rather than importing concrete classes.
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
