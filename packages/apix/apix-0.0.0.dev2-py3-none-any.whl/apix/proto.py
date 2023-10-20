from __future__ import annotations

import typing

from .model import PathInfo


T = typing.TypeVar("T")
T_co = typing.TypeVar("T_co", covariant=True)
OP = typing.TypeVar("OP")
OP_co = typing.TypeVar("OP_co", covariant=True)


class ProtoSerializer(typing.Protocol):
    def encode(self, obj: typing.Any) -> bytes: ...
    def decode(self, data: bytes, type: typing.Type[T]) -> T: ...


class ProtoSchema(typing.Protocol): ...


class ProtoPath(typing.Protocol[T_co]):
    __info__: typing.ClassVar[PathInfo]
