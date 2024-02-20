from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from mostlyai.model import ConnectorAccessType, ConnectorTestConnection, ConnectorType


class BaseComponent(BaseModel):
    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)


class CreateConnectorRequest(BaseComponent):
    name: Optional[str] = None
    type: ConnectorType
    access_type: Optional[ConnectorAccessType] = Field(None, alias="accessType")
    config: Optional[dict[str, str]] = None
    secrets: Optional[dict[str, str]] = None
    ssl: Optional[dict[str, str]] = None
    test_connection: Optional[ConnectorTestConnection] = Field(
        None, alias="testConnection"
    )


class PatchConnectorRequest(BaseComponent):
    name: Optional[str] = None
    config: Optional[dict[str, str]] = None
    secrets: Optional[dict[str, str]] = None
    ssl: Optional[dict[str, str]] = None
    test_connection: Optional[ConnectorTestConnection] = Field(
        None, alias="testConnection"
    )
