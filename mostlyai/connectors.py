from typing import Any, Dict, Iterator, Optional

from mostlyai.base import (
    DELETE,
    GET,
    PATCH,
    POST,
    Paginator,
    StrUUID,
    _MostlyBaseClient,
)
from mostlyai.model import Connector, ConnectorAccessType, ConnectorType


class _MostlyConnectorsClient(_MostlyBaseClient):
    SECTION = ["connectors"]

    ## PUBLIC METHODS ##

    def list(
        self,
        offset: int = 0,
        limit: int = 50,
        access_type: Optional[str] = None,
    ) -> Iterator[Connector]:
        """
        List connectors.

        Paginate through all connectors that the user has access to.
        Only connectors, that are independent of a table, will be returned.

        :param offset: Offset the entities in the response. Optional. Default: 0
        :param limit: Limit the number of entities in the response. Optional. Default: 50
        :param access_type: Filter by access type. Possible values: "SOURCE", "DESTINATION"
        :return: Iterator over connectors.
        """
        with Paginator(
            self, Connector, offset=offset, limit=limit, access_type=access_type
        ) as paginator:
            for item in paginator:
                yield item

    def get(self, connector_id: StrUUID) -> Connector:
        """
        Retrieve connector

        :param connector_id: The unique identifier of a connector
        :return: The retrieved connector
        """
        response = self.request(path=[connector_id], response_type=Connector)
        return response

    def create(
        self,
        config: Dict[str, Any],
    ) -> Connector:
        """
        Create a connector, and optionally validate the connection before saving.

        See `mostly.connect` for more details.
        """
        response = self.request(
            verb=POST, path=[], json=config, response_type=Connector
        )
        return response

    ## PRIVATE METHODS ##

    def _update(
        self,
        connector_id: StrUUID,
        name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        secrets: Optional[Dict[str, str]] = None,
        ssl: Optional[Dict[str, str]] = None,
        testConnection: Optional[bool] = None,
    ) -> Connector:
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

    def _delete(self, connector_id: StrUUID) -> None:
        self.request(verb=DELETE, path=[connector_id])

    def _to_dict(self, connector_id: StrUUID):
        response = self.request(verb=GET, path=[connector_id, "config"])
        return response

    def _locations(self, connector_id: str, prefix: str = "") -> list:
        response = self.request(
            path=[connector_id, "locations"], params={"prefix": prefix}
        )
        return response
