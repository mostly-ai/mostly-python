from typing import Any, Dict, Iterator, Optional

from mostlyai.base import DELETE, PATCH, POST, Paginator, StrUUID, _MostlyBaseClient
from mostlyai.model import Connector, ConnectorAccessType, ConnectorType


class _MostlyConnectorsClient(_MostlyBaseClient):
    SECTION = ["connectors"]

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
        with Paginator(
            self, Connector, offset=offset, limit=limit, access_type=access_type
        ) as paginator:
            for item in paginator:
                yield item

    def get(self, connector_id: StrUUID) -> Connector:
        """
        Retrieve a specific connector by its ID.

        :param connector_id: The unique identifier of the connector.
        :return: The retrieved connector.
        """
        response = self.request(path=[connector_id], response_type=Connector)
        return response

    def get_config(self, connector_id: StrUUID) -> dict:
        """
        Retrieve the configuration of a specific connector.

        :param connector_id: The unique identifier of the connector.
        :return: The configuration of the connector.
        """
        response = self.request(path=[connector_id, "config"])
        return response

    def create(
        self,
        type: ConnectorType,
        name: Optional[str] = None,
        accessType: Optional[ConnectorAccessType] = None,
        config: Optional[Dict[str, Any]] = None,
        secrets: Optional[Dict[str, str]] = None,
        ssl: Optional[Dict[str, str]] = None,
        testConnection: Optional[bool] = None,
    ) -> Connector:
        """
        Create a new connector.

        :param type: The type of connector
        :param name: The name of a connector
        :param accessType: The access type of connector
        :param config: The config parameter contains any configuration of the connector
        :param secrets: The secrets parameter contains any sensitive credentials of the connector
        :param ssl: The ssl parameter contains any SSL related configurations of the connector
        :param testConnection: If true, the connection will be tested before saving
        :return: The created connector.
        """
        new_connector = {
            "type": type,
            "name": name,
            "accessType": accessType,
            "config": config,
            "secrets": secrets,
            "ssl": ssl,
            "testConnection": testConnection,
        }

        response = self.request(
            verb=POST, path=[], json=new_connector, response_type=Connector
        )
        return response

    def update(
        self,
        connector_id: StrUUID,
        name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        secrets: Optional[Dict[str, str]] = None,
        ssl: Optional[Dict[str, str]] = None,
        testConnection: Optional[bool] = None,
    ) -> Connector:
        """
        Update an existing connector.

        :param connector_id: Unique ID of the connector to update.
        :param name: The name of a connector
        :param config: The config parameter contains any configuration of the connector
        :param secrets: The secrets parameter contains any sensitive credentials of the connector
        :param ssl: The ssl parameter contains any SSL related configurations of the connector
        :param testConnection: If true, the connection will be tested before saving
        :return: The updated connector.
        """
        updated_connector = {
            "name": name,
            "config": config,
            "secrets": secrets,
            "ssl": ssl,
            "testConnection": testConnection,
        }
        response = self.request(
            verb=PATCH,
            path=[connector_id],
            json=updated_connector,
            response_type=Connector,
        )
        return response

    def delete(self, connector_id: StrUUID) -> None:
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
