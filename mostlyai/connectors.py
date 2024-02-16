from typing import Any, Dict, Iterator, Optional

from mostlyai.base import (
    DELETE,
    PATCH,
    POST,
    Paginator,
    StrUUID,
    _MostlyBaseClient,
    GET,
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
        type: ConnectorType,
        name: Optional[str] = None,
        accessType: Optional[ConnectorAccessType] = None,
        config: Optional[Dict[str, Any]] = None,
        secrets: Optional[Dict[str, str]] = None,
        ssl: Optional[Dict[str, str]] = None,
        testConnection: Optional[bool] = None,
    ) -> Connector:
        """
        Create a connector, and optionally validate the connection before saving.

        If validation fails, a 400 status with an error message will be returned.

        The structures of the config, secrets and ssl parameters depend on the connector type.
        Cloud storage:
        - AZURE_STORAGE
            - config
                - accountName: string
            - secrets
                - accountKey: string
            - location: container/path
        - GOOGLE_CLOUD_STORAGE
            - config
            - secrets
                - keyFile: string
            - location: bucket/path
        - S3_STORAGE
            - config
                - accessKey: string
            - secrets
                - secretKey: string
            - location: bucket/path
        Database:
        - BIGQUERY
            - config
            - secrets
                - keyFile: string
            - location: dataset.table
        - DATABRICKS
            - config
                - host: string
                - httpPath: string
                - catalog: string
            - secrets
                - accessToken: keyFile
            - location: schema.table
        - MARIADB
            - config
                - host: string
                - port: integer, default: 3306
                - username: string
            - secrets
                - password: string
            - location: database.table
        - MSSQL
            - config
                - host: string
                - port: integer, default: 1433
                - username: string
                - database: string
            - secrets
                - password: string
            - location: schema.table
        - MYSQL
            - config
                - host: string
                - port: integer, default: 3306
                - username: string
            - secrets
                - password: string
            - location: database.table
        - ORACLE
            - config
                - host: string
                - port: integer, default: 1521
                - username: string
                - connectionType: enum {SID, SERVICE_NAME}, default: SID
                - database: string, default: ORCL
            - secrets
                - password: string
            - location: schema.table
        - POSTGRES
            - config
                - host: string
                - port: integer, default: 5432
                - username: string
                - database: string
            - secrets
                - password: string
            - ssl
                - rootCertificate: string
                - sslCertificate: string
                - sslCertificateKey: string
            - location: schema.table
        - SNOWFLAKE
            - config
                - account: string
                - username: string
                - warehouse: string, default: COMPUTE_WH
                - database: string
            - secrets
                - password: string
            - location: schema.table

        :param type: The type of connector, i.e. POSTGRES, MYSQL, etc.
        :param name: The name of a connector
        :param accessType: The access type of connector. Possible values: "SOURCE", "DESTINATION"
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
