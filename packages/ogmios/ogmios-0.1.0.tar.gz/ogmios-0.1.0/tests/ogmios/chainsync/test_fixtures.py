import pytest

from ogmios.client import Client


@pytest.fixture
def client():
    with Client() as client:
        yield client
