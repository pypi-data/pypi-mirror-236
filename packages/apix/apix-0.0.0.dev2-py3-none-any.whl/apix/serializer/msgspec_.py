import typing
import msgspec

from ..proto import T
from ..model import PathInfo


class MsgspecSchema(msgspec.Struct): ...


class MsgspecPath(msgspec.Struct, typing.Generic[T]):
    __info__: typing.ClassVar[PathInfo] = PathInfo()


class MsgspecSerializer:
    def __init__(self) -> None:
        self.__encoder = msgspec.json.Encoder()
    
    def encode(self, obj) -> bytes:
        return self.__encoder.encode(obj)

    def decode(self, data, type: typing.Type[T]) -> T:
        return msgspec.json.decode(data, type=type)
