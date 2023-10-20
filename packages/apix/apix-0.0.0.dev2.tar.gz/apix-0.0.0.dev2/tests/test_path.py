
from apix.model import Response
from apix.serializer.base import build_result

from .models import A, B, GetA

def test_build_result(serializer):
    a_obj = A(b=B(a=1))
    response = Response(status=200, body=serializer.encode(a_obj))
    path = GetA()

    result: A = build_result(response, path, serializer)
    assert result == a_obj
