import typing
from ..proto import ProtoSchema, ProtoSerializer


def default_serializer() -> ProtoSerializer:
    from .msgspec_ import MsgspecSerializer

    return MsgspecSerializer()

def default_schema_type() -> typing.Type[ProtoSchema]:
    from .msgspec_ import MsgspecSchema

    return MsgspecSchema
