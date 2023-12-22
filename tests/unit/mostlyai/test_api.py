import pytest

from mostlyai import MostlyAI
from mostlyai.model import Connector


@pytest.fixture
def mostly_client():
    return MostlyAI()


@pytest.fixture
def connector_id():
    return "0aecf7e5-350b-4e9a-855a-3b5d7863548d"


@pytest.fixture
def new_connector():
    return {
        "name": "Test New Connector",
        "type": "S3_STORAGE",
        "accessType": "SOURCE",
        "config": {
            "accessKey": "value1",
        },
        "secrets": {
            "secretKey": "secretValue",
        },
        "testConnection": False,
    }


class TestMostlyClient:
    def test_temp_get_token(self, mostly_client):
        token = mostly_client._temp_get_token()
        assert len(token) > 20

    def test_connector_list(self, mostly_client):
        for connector in mostly_client.connector.list():
            assert isinstance(connector, Connector)

    def test_connector_create_update_delete(self, mostly_client, new_connector):
        fetched_connector = mostly_client.connector.create(**new_connector)
        assert isinstance(fetched_connector, Connector)
        updated_connector = {
            "name": fetched_connector.name.replace("New", "Updated"),
            "testConnection": False,
        }
        response = mostly_client.connector.update(
            connector_id=fetched_connector.id, **updated_connector
        )
        assert "Updated" in response.name
        mostly_client.connector.delete(fetched_connector.id)

    def test_connector_get(self, mostly_client, connector_id):
        result = mostly_client.connector.get(connector_id)
        assert isinstance(result, Connector)
        assert str(result.id) == connector_id

    def test_connector_locations(self, mostly_client, connector_id):
        result = mostly_client.connector.locations(connector_id=connector_id)
        assert result == ["QA_Automation_Output_2", "information_schema", "public"]
