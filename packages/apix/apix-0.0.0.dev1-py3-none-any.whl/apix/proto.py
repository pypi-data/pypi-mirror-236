from __future__ import annotations

import typing

T = typing.TypeVar("T")
OP = typing.TypeVar("OP")
OP_co = typing.TypeVar("OP_co", covariant=True)


class ProtoSerializer(typing.Protocol):
    def encode(self, obj: typing.Any) -> bytes: ...
    def decode(self, data: bytes, type: typing.Type[T]) -> T: ...


class ProtoSchema(typing.Protocol):
    ...

