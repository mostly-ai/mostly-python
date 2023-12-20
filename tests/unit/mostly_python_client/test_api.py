import uuid

import pytest

from mostly_python_client.api import MostlyClient


@pytest.fixture
def mostly_client():
    return MostlyClient()


@pytest.fixture
def connector_id():
    return "0aecf7e5-350b-4e9a-855a-3b5d7863548d"


@pytest.fixture
def new_connector():
    return {
        "name": f"Test New Connector {str(uuid.uuid4())[:8]}",
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
            connector_props = ["id", "name", "type", "accessType", "metadata"]
            assert all(prop in connector for prop in connector_props)

    def test_connector_create_and_update(self, mostly_client, new_connector):
        fetched_connector = mostly_client.connector.create(new_connector)
        assert isinstance(fetched_connector, dict)
        assert "id" in fetched_connector
        updated_connector = fetched_connector.copy()
        updated_connector["name"] = updated_connector["name"].replace("New", "Updated")
        updated_connector["testConnection"] = False
        response = mostly_client.connector.update(updated_connector)
        assert "Updated" in response["name"]

    def test_connector_get(self, mostly_client, connector_id):
        result = mostly_client.connector.get(connector_id)
        assert isinstance(result, dict)
        assert result["id"] == connector_id

    def test_connector_locations(self, mostly_client, connector_id):
        result = mostly_client.connector.locations(connector_id=connector_id)
        assert result == ["QA_Automation_Output_2", "information_schema", "public"]
