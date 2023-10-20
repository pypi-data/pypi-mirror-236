from .models import A, B


def test_encode_schema(serializer):
    obj = A(b=B(a=1))
    data = serializer.encode(obj)
    assert data == b'{"b":{"a":1}}'


def test_decode_schema(serializer):
    data = b'{"b":{"a":1}}'
    obj = serializer.decode(data, type=A)
    assert obj == A(b=B(a=1))

