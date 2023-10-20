import typing
import dataclasses


@dataclasses.dataclass
class Response:
    status: int
    body: bytes


@dataclasses.dataclass
class PathInfo:
    method: str = "GET"
    path: str = "/"
    type: typing.Type = bool
