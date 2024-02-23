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
from mostlyai.components import CreateConnectorRequest, PatchConnectorRequest
from mostlyai.model import Connector, ConnectorAccessType, ConnectorType
from mostlyai.shares import _MostlySharesMixin
from mostlyai.utils import _as_dict


class _MostlyConnectorsClient(_MostlyBaseClient, _MostlySharesMixin):
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
        response = self.request(verb=GET, path=[connector_id], response_type=Connector)
        return response

    def create(
        self,
        config: CreateConnectorRequest | dict[str, Any],
    ) -> Connector:
        """
        Create a connector, and optionally validate the connection before saving.

        See `mostly.connect` for more details.
        """
        config = _as_dict(config)
        response = self.request(
            verb=POST, path=[], json=config, response_type=Connector
        )
        return response

    ## PRIVATE METHODS ##

    def _update(
        self,
        connector_id: StrUUID,
        config: PatchConnectorRequest | dict[str, Any],
    ) -> Connector:
        config = _as_dict(config)
        response = self.request(
            verb=PATCH,
            path=[connector_id],
            json=config,
            response_type=Connector,
        )
        return response

    def _delete(self, connector_id: StrUUID) -> None:
        self.request(verb=DELETE, path=[connector_id])

    def _config(self, connector_id: StrUUID):
        response = self.request(verb=GET, path=[connector_id, "config"])
        return response

    def _locations(self, connector_id: str, prefix: str = "") -> list:
        response = self.request(
            verb=GET, path=[connector_id, "locations"], params={"prefix": prefix}
        )
        return response
