from typing import Any, Iterator, Optional, Union
from uuid import UUID

from mostlyai.base import DELETE, PATCH, POST, _MostlyBaseClient
from mostlyai.model import Connector, Generator


class _MostlyConnectorClient(_MostlyBaseClient):
    SECTION = ["api", "v2", "connectors"]

    def list(
        self, offset: int = 0, limit: int = 50, access_type: str = None
    ) -> Iterator[Connector]:
        """
        List connectors with pagination and optional access type filtering.

        :param offset: The starting point for listing connectors.
        :param limit: The maximum number of connectors to return per request.
        :param access_type: Filter connectors by access type, defaults to None.
        :return: Yields individual connectors.

        The method uses a while loop to handle pagination and continues to request
        and yield connectors until all available connectors have been listed.
        """
        while True:
            params = {"offset": offset, "limit": limit}
            if access_type:
                params["accessType"] = access_type

            response = self.request(path=[], params=params)

            # Safely handling the case when 'results' or 'totalCount' is not in response
            results = response.get("results", [])
            total_count = response.get("totalCount", 0)

            for connector in results:
                yield Connector(**connector, client=self, by_alias=True)

            offset += limit

            # Correcting the condition to break the loop
            if offset >= total_count:
                break

    def get(self, connector_id: Union[str, UUID]) -> Connector:
        """
        Retrieve a specific connector by its ID.

        :param connector_id: The unique identifier of the connector.
        :return: The retrieved connector.
        """
        response = self.request(path=[connector_id], response_type=Connector)
        return response

    def create(self, **params: dict[str, Any]) -> Connector:
        """
        Create a new connector.

        :param params: A dictionary representing a new connector.
        :return: The created connector.
        """
        new_connector = dict(params)
        response = self.request(
            verb=POST, path=[], json=new_connector, response_type=Connector
        )
        return response

    def update(
        self, connector_id: Union[str, UUID], **params: dict[str, Any]
    ) -> Connector:
        """
        Update an existing connector.

        :param connector_id: Unique ID of the connector to update.
        :param params: A dictionary representing the edited part of the connector.
        :return: The updated connector.
        """
        updated_connector = dict(params)
        response = self.request(
            verb=PATCH,
            path=[connector_id],
            json=updated_connector,
            response_type=Connector,
        )
        return response

    def delete(self, connector_id: Union[str, UUID]) -> None:
        """
        Delete a connector by its ID.

        :param connector_id: The unique identifier of the connector to be deleted.
        :return: Empty, if successfully deleted the connector.
        """
        self.request(verb=DELETE, path=[connector_id])

    def locations(self, connector_id: str, prefix: str = "") -> list:
        """
        Retrieve the locations associated with a specific connector and prefix.

        :param connector_id: The unique identifier of the connector.
        :param prefix: A prefix to filter the locations, defaults to "".
        :return: A list of locations (schemas, databases, directories, etc.) on the given level.
        """
        params = {"prefix": prefix}
        response = self.request(path=[connector_id, "locations"], params=params)
        return response


class _MostlyGeneratorsClient(_MostlyBaseClient):
    SECTION = ["api", "v2", "generators"]

    def list(
        self, offset: int = 0, limit: int = 50, access_type: str = None
    ) -> Iterator[Generator]:
        while True:
            params = {"offset": offset, "limit": limit}
            if access_type:
                params["accessType"] = access_type

            response = self.request(path=[], params=params)

            # Safely handling the case when 'results' or 'totalCount' is not in response
            results = response.get("results", [])
            total_count = response.get("totalCount", 0)

            for generator in results:
                yield Generator(**generator, client=self, by_alias=True)

            offset += limit

            # Correcting the condition to break the loop
            if offset >= total_count:
                break


class MostlyAI(_MostlyBaseClient):
    """
    Client for interacting with the Mostly AI Public API.

    This client serves as the main entry point for accessing various functionalities
    provided. It initializes and holds various specialized clients for
    different sections of the API.

    :param base_url: The base URL. If not provided, a default value is used.
    :param api_key: The API key for authenticating. If not provided, it would rely on env vars.
    """

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__(base_url=base_url, api_key=api_key)
        client_kwargs = {"base_url": self.base_url, "api_key": self.api_key}
        self.connectors = _MostlyConnectorClient(**client_kwargs)
        self.generators = _MostlyGeneratorsClient(**client_kwargs)


# NOTE: the part below part is very hacky! Just for a quick POC
def connector_locations(self, prefix: str = ""):
    if isinstance(self.client, _MostlyConnectorClient):
        return self.client.locations(connector_id=self.id, prefix=prefix)


Connector.locations = connector_locations
