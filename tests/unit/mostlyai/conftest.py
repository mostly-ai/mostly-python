import pytest

from mostlyai import MostlyAI


@pytest.fixture
def mostly():
    return MostlyAI()


@pytest.fixture
def local_connector(mostly):
    return mostly.connectors.create(name="Local Connector", type="LOCAL_STORAGE")
