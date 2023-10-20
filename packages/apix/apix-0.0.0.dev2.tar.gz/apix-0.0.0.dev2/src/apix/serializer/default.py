import typing
from ..proto import ProtoPath, ProtoSchema, ProtoSerializer, T


def default_serializer() -> ProtoSerializer:
    from .msgspec_ import MsgspecSerializer

    return MsgspecSerializer()


def default_schema_type() -> typing.Type[ProtoSchema]:
    from .msgspec_ import MsgspecSchema

    return MsgspecSchema


def default_path_type() -> typing.Type[ProtoPath[T]]:
    from .msgspec_ import MsgspecPath

    return MsgspecPath[T]
