import pytest

from mostly_python_client.api import MostlyClient


@pytest.fixture
def mostly_client():
    return MostlyClient()


@pytest.fixture
def connector_id():
    return "0aecf7e5-350b-4e9a-855a-3b5d7863548d"


class TestMostlyClient:
    def test_temp_get_token(self, mostly_client):
        token = mostly_client.temp_get_token()
        assert len(token) > 20

    def test_connector_list(self, mostly_client):
        for connector in mostly_client.connector.list():
            connector_props = ["id", "name", "type", "accessType", "metadata"]
            assert all(prop in connector for prop in connector_props)

    def test_connector_get(self, mostly_client, connector_id):
        result = mostly_client.connector.get(connector_id)
        assert isinstance(result, dict)
        assert result["id"] == connector_id

    # def test_connector_locations(self, mostly_client, connector_id):
    #     # TODO check with the app team
    #     result = mostly_client.connector.locations(connector_id=connector_id)
    #     assert result
