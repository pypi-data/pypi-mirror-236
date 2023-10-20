from ..proto import ProtoSerializer, T, ProtoPath
from ..model import Response



def build_result(
    response: Response,
    path: ProtoPath[T],
    serializer: ProtoSerializer,
) -> T:
    return serializer.decode(response.body, path.__info__.type)
