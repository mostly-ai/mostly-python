from typing import Any, Iterator, Optional, List, Dict, Union

from mostlyai.client.base import DELETE, GET, PATCH, POST, Paginator, _MostlyBaseClient
from mostlyai.client.model import (
    Connector,
    ConnectorListItem,
    SyntheticDatasetConfig,
    ConnectorPatchConfig,
    ConnectorConfig,
)


class _MostlyConnectorsClient(_MostlyBaseClient):
    SECTION = ["connectors"]

    # PUBLIC METHODS #

    def list(
        self,
        offset: int = 0,
        limit: int = 50,
        access_type: Optional[str] = None,
        search_term: Optional[str] = None,
    ) -> Iterator[ConnectorListItem]:
        """
        List connectors.

        Paginate through all connectors accessible by the user. Only connectors that are independent of a table will be returned.

        Args:
            offset: Offset for entities in the response.
            limit: Limit for the number of entities in the response.
            access_type: Filter by access type (e.g., "SOURCE" or "DESTINATION").
            search_term: Filter by string in the connector name.

        Returns:
            Iterator[ConnectorListItem]: An iterator over connector list items.
        """
        with Paginator(
            self,
            ConnectorListItem,
            offset=offset,
            limit=limit,
            access_type=access_type,
            search_term=search_term,
        ) as paginator:
            for item in paginator:
                yield item

    def get(self, connector_id: str) -> Connector:
        """
        Retrieve a connector by its ID.

        Args:
            connector_id: The unique identifier of the connector.

        Returns:
            Connector: The retrieved connector object.
        """
        response = self.request(verb=GET, path=[connector_id], response_type=Connector)
        return response

    def create(
        self,
        config: Union[SyntheticDatasetConfig, dict[str, Any]],
    ) -> Connector:
        """
        Create a connector and optionally validate the connection before saving.

        See `mostly.connect` for more details.

        Args:
            config: Configuration for the connector.

        Returns:
            The created connector object.
        """
        response = self.request(
            verb=POST, path=[], json=config, response_type=Connector
        )
        return response

    # PRIVATE METHODS #

    def _update(
        self,
        connector_id: str,
        config: Union[ConnectorPatchConfig, dict[str, Any]],
    ) -> Connector:
        response = self.request(
            verb=PATCH,
            path=[connector_id],
            json=config,
            response_type=Connector,
        )
        return response

    def _delete(self, connector_id: str) -> None:
        self.request(verb=DELETE, path=[connector_id])

    def _config(self, connector_id: str) -> ConnectorConfig:
        response = self.request(
            verb=GET, path=[connector_id, "config"], response_type=ConnectorConfig
        )
        return response

    def _locations(self, connector_id: str, prefix: str = "") -> list:
        response = self.request(
            verb=GET, path=[connector_id, "locations"], params={"prefix": prefix}
        )
        return response

    def _schema(self, connector_id: str, location: str) -> List[Dict[str, Any]]:
        response = self.request(
            verb=GET, path=[connector_id, "schema"], params={"location": location}
        )
        return response
