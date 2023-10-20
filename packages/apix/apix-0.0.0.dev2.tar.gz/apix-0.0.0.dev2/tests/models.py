import typing
from apix.serializer.default import default_path_type, default_schema_type
from apix.model import PathInfo
from apix.proto import T

DefPath = default_path_type()
Schema = default_schema_type()

class Path(DefPath, typing.Generic[T]):
    ...


class B(Schema):
    a: int

class A(Schema):
    b: B


class GetA(Path[A]):
    __info__: typing.ClassVar[PathInfo] = PathInfo(method="GET", path="/a", type=A)
