import pytest

from apix.proto import ProtoSerializer


@pytest.fixture
def serializer() -> ProtoSerializer:
    from apix.serializer.default import default_serializer

    return default_serializer()
