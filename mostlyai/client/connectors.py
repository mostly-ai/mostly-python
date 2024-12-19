# Copyright 2024 MOSTLY AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Iterator, Optional, List, Dict, Union

from mostlyai.client.base import DELETE, GET, PATCH, POST, Paginator, _MostlyBaseClient
from mostlyai.client.domain import (
    Connector,
    ConnectorListItem,
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

        Example for listing all connectors:
            ```python
            from mostlyai import MostlyAI
            mostly = MostlyAI()
            for c in mostly.connectors.list():
                print(f"Connector `{c.name}` ({c.access_type}, {c.type}, {c.id})")
            ```

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

        Example for retrieving a connector:
            ```python
            from mostlyai import MostlyAI
            mostly = MostlyAI()
            c = mostly.connectors.get('INSERT_YOUR_CONNECTOR_ID')
            c
            ```

        Args:
            connector_id: The unique identifier of the connector.

        Returns:
            Connector: The retrieved connector object.
        """
        response = self.request(verb=GET, path=[connector_id], response_type=Connector)
        return response

    def create(
        self,
        config: Union[ConnectorConfig, dict[str, Any]],
        test_connection: Optional[bool] = True,
    ) -> Connector:
        """
        Create a connector and optionally validate the connection before saving.

        See [`mostly.connect`](api_client.md#mostlyai.client.api.MostlyAI.connect) for more details.

        Args:
            config: Configuration for the connector.
            test_connection: Whether to test the connection before saving the connector

        Returns:
            The created connector object.
        """
        response = self.request(
            verb=POST,
            path=[],
            json=config,
            params={"test_connection": test_connection},
            response_type=Connector,
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
