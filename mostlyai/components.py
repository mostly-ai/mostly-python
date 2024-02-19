from typing import Optional

from pydantic import BaseModel, Field

from mostlyai.model import ConnectorAccessType, ConnectorTestConnection, ConnectorType


class CreateConnectorRequest(BaseModel):
    name: Optional[str] = None
    type: ConnectorType
    access_type: Optional[ConnectorAccessType] = Field(None, alias="accessType")
    config: Optional[dict[str, str]] = None
    secrets: Optional[dict[str, str]] = None
    ssl: Optional[dict[str, str]] = None
    test_connection: Optional[ConnectorTestConnection] = Field(
        None, alias="testConnection"
    )


class PatchConnectorRequest(BaseModel):
    name: Optional[str] = None
    config: Optional[dict[str, str]] = None
    secrets: Optional[dict[str, str]] = None
    ssl: Optional[dict[str, str]] = None
    test_connection: Optional[ConnectorTestConnection] = Field(
        None, alias="testConnection"
    )
