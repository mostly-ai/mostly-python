from typing import Any, Iterator, Optional, List, Dict

from mostlyai.base import DELETE, GET, PATCH, POST, Paginator, _MostlyBaseClient
from mostlyai.model import Connector, ConnectorListItem
from mostlyai.shares import _MostlySharesMixin


class _MostlyConnectorsClient(_MostlyBaseClient, _MostlySharesMixin):
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

        Paginate through all connectors that the user has access to.
        Only connectors, that are independent of a table, will be returned.

        :param offset: Offset the entities in the response. Optional. Default: 0
        :param limit: Limit the number of entities in the response. Optional. Default: 50
        :param access_type: Filter by access type. Possible values: "SOURCE", "DESTINATION"
        :param search_term: Filter by string in name. Optional
        :return: Iterator over connectors.
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
        Retrieve a connector.

        :param connector_id: The unique identifier of a connector
        :return: The retrieved connector
        """
        response = self.request(verb=GET, path=[connector_id], response_type=Connector)
        return response

    def create(
        self,
        config: dict[str, Any],
    ) -> Connector:
        """
        Create a connector, and optionally validate the connection before saving.

        See `mostly.connect` for more details.
        """
        response = self.request(
            verb=POST, path=[], json=config, response_type=Connector
        )
        return response

    # PRIVATE METHODS #

    def _update(
        self,
        connector_id: str,
        config: dict[str, Any],
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

    def _config(self, connector_id: str):
        response = self.request(verb=GET, path=[connector_id, "config"])
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
