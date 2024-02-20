from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from mostlyai.model import ConnectorAccessType, ConnectorTestConnection, ConnectorType, ModelConfiguration, \
    ModelEncodingType


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


class ForeignKey(BaseComponent):
    column: str
    referenced_table: str = Field(..., alias='referencedTable')
    is_context: bool = Field(..., alias='isContext')


class Column(BaseComponent):
    name: str
    included: bool
    model_encoding_type: ModelEncodingType = Field(..., alias='modelEncodingType')


class TableItem(BaseComponent):
    name: str
    source_connector_id: UUID = Field(..., alias='sourceConnectorId')
    location: str
    data: str
    model_configuration: ModelConfiguration = Field(..., alias='modelConfiguration')
    text_model_configuration: ModelConfiguration = Field(..., alias='textModelConfiguration')
    primary_key: str = Field(..., alias='primaryKey')
    foreign_keys: list[ForeignKey] = Field(..., alias='foreignKeys')
    columns: list[Column]


class CreateGeneratorRequest(BaseModel):
    name: str
    description: str | None = None
    tables: list[TableItem] | None = None
