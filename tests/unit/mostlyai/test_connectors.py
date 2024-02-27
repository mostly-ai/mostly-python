import pytest

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
    def test_list(self, mostly):
        for connector in mostly.connectors.list():
            assert isinstance(connector, Connector)

    def test_create_update_delete(self, mostly, new_connector):
        fetched_connector = mostly.connectors.create(new_connector)
        assert isinstance(fetched_connector, Connector)
        updated_connector = {
            "name": fetched_connector.name.replace("New", "Updated"),
            "testConnection": False,
        }
        response = fetched_connector.update(updated_connector)
        assert "Updated" in response.name
        fetched_connector.delete()

    def test_get_and_locations(self, mostly, connector_id):
        connector = mostly.connectors.get(connector_id)
        assert isinstance(connector, Connector)
        assert str(connector.id) == connector_id
        locations = connector.locations()
        assert locations == [
            "Berka_Demo",
            "QA_Automation_Output_2",
            "information_schema",
            "public",
        ]

    def test_not_found(self, mostly):
        with pytest.raises(APIStatusError) as err:
            mostly.connectors.get("does_not_exist")

        assert str(400) in err.value.message
