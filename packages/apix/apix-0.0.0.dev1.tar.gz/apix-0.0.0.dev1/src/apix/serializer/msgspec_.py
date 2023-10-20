import typing
import msgspec

T = typing.TypeVar("T")

class MsgspecSchema(msgspec.Struct): ...


class MsgspecSerializer:
    def __init__(self) -> None:
        self.__encoder = msgspec.json.Encoder()
    
    def encode(self, obj) -> bytes:
        return self.__encoder.encode(obj)

    def decode(self, data, type: typing.Type[T]) -> T:
        return msgspec.json.decode(data, type=type)
