import pytest

from mostlyai import MostlyAI


@pytest.fixture
def mostly_client():
    return MostlyAI()


@pytest.fixture
def local_connector(mostly_client):
    return mostly_client.connectors.create(name="Local Connector", type="LOCAL_STORAGE")