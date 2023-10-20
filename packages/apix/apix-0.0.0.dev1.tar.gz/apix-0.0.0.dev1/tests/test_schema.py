from apix.serializer import default_serializer, default_schema_type

Schema = default_schema_type()
Serializer = default_serializer()

class B(Schema):
    a: int


class A(Schema):
    b: B


def test_encode_schema():
    obj = A(b=B(a=1))
    data = Serializer.encode(obj)
    assert data == b'{"b":{"a":1}}'

def test_decode_schema():
    data = b'{"b":{"a":1}}'
    obj = Serializer.decode(data, type=A)
    assert obj == A(b=B(a=1))

