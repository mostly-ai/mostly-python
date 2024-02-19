import pytest

from mostlyai.components import CreateConnectorRequest, PatchConnectorRequest
from mostlyai.exceptions import APIStatusError
from mostlyai.model import Connector


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


class TestConnectors:
    def test_list(self, mostly_client):
        for connector in mostly_client.connectors.list():
            assert isinstance(connector, Connector)

    def test_create_update_delete(self, mostly_client, new_connector):
        fetched_connector = mostly_client.connectors.create(new_connector)
        assert isinstance(fetched_connector, Connector)
        updated_connector = PatchConnectorRequest(
            name=fetched_connector.name.replace("New", "Updated"),
            test_connection=False,
        )
        response = fetched_connector.update(updated_connector)
        assert "Updated" in response.name
        fetched_connector.delete()

    def test_get(self, mostly_client, connector_id):
        result = mostly_client.connectors.get(connector_id)
        assert isinstance(result, Connector)
        assert str(result.id) == connector_id

    def test_locations(self, mostly_client, connector_id):
        result = mostly_client.connectors.locations(connector_id=connector_id)
        assert result == ["QA_Automation_Output_2", "information_schema", "public"]

    def test_not_found(self, mostly_client):
        with pytest.raises(APIStatusError) as err:
            mostly_client.connectors.get("does_not_exist")

        assert str(400) in err.value.message
