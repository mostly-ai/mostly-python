from typing import Optional, Union
from uuid import UUID

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field

from mostlyai.model import (
    ConnectorAccessType,
    ConnectorTestConnection,
    ConnectorType,
    ModelConfiguration,
    ModelEncodingType,
    PermissionLevel,
)


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
    source_connector_id: Optional[UUID] = Field(None, alias="sourceConnectorId")
    location: Optional[str] = None
    data: Union[str, pd.DataFrame]
    model_configuration: Optional[ModelConfiguration] = Field(
        None, alias="modelConfiguration"
    )
    text_model_configuration: Optional[ModelConfiguration] = Field(
        None, alias="textModelConfiguration"
    )
    primary_key: Optional[str] = Field(None, alias="primaryKey")
    foreign_keys: Optional[list[ForeignKey]] = Field(None, alias="foreignKeys")
    columns: Optional[list[Column]] = None


class CreateGeneratorRequest(BaseComponent):
    name: str
    description: Optional[str] = None
    tables: Optional[list[TableItem]] = None


class CreateShareRequest(BaseComponent):
    user_email: str = Field(..., alias="userEmail", description="The email of a user")
    permission_level: PermissionLevel = Field(
        ...,
        alias="permissionLevel",
        description="The permission level of the user or group with respect to this entity",
    )


class DeleteShareRequest(BaseComponent):
    user_email: str = Field(..., alias="userEmail", description="The email of a user")
