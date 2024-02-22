from enum import Enum
from typing import Optional
from uuid import UUID

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field

from mostlyai.model import (
    Connector,
    ConnectorAccessType,
    ConnectorTestConnection,
    ConnectorType,
    Generator,
    ModelConfiguration,
    ModelEncodingType,
    PermissionLevel,
    SyntheticDataset,
)

ShareableResource = Connector | Generator | SyntheticDataset


class BaseComponent(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        protected_namespaces=(),
        arbitrary_types_allowed=True,
    )


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


class ForeignKey(BaseComponent):
    column: str
    referenced_table: str = Field(..., alias="referencedTable")
    is_context: bool = Field(..., alias="isContext")


class Column(BaseComponent):
    name: str
    included: bool
    model_encoding_type: ModelEncodingType = Field(..., alias="modelEncodingType")


class TableItem(BaseComponent):
    name: str
    source_connector_id: UUID | None = Field(None, alias="sourceConnectorId")
    location: str | None = None
    data: str | pd.DataFrame
    model_configuration: ModelConfiguration | None = Field(
        None, alias="modelConfiguration"
    )
    text_model_configuration: ModelConfiguration | None = Field(
        None, alias="textModelConfiguration"
    )
    primary_key: str | None = Field(None, alias="primaryKey")
    foreign_keys: list[ForeignKey] | None = Field(None, alias="foreignKeys")
    columns: list[Column] | None = None


class CreateGeneratorRequest(BaseComponent):
    name: str
    description: str | None = None
    tables: list[TableItem] | None = None


class CreateShareRequest(BaseComponent):
    user_email: str = Field(..., alias="userEmail", description="The email of a user")
    permission_level: PermissionLevel = Field(
        ...,
        alias="permissionLevel",
        description="The permission level of the user or group with respect to this entity",
    )


class DeleteShareRequest(BaseComponent):
    user_email: str = Field(..., alias="userEmail", description="The email of a user")
