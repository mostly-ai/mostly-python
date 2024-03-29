# generated by datamodel-codegen:
#   timestamp: 2024-03-18T16:27:33+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Annotated, Any, ClassVar, Dict, List, Literal, Optional, Union

import pandas as pd
from pydantic import Field, RootModel

from mostlyai.base import CustomBaseModel


class PermissionLevel(str, Enum):
    """
    The permission level of the user or group with respect to this entity
    - VIEW: The user can view and use the entity
    - EDIT: The user can edit and share the entity
    - ADMIN: The user can edit, share and delete the entity
    There is only a single user per entity with ADMIN rights, and that user is the owner of the entity.

    """

    view = "VIEW"
    edit = "EDIT"
    admin = "ADMIN"


class Credits(CustomBaseModel):
    current: Annotated[
        Optional[float],
        Field(description="The credit balance for the current time period"),
    ] = None
    limit: Annotated[
        Optional[float],
        Field(
            description="The credit limit for the current time period. If empty, then there is no limit."
        ),
    ] = None
    period_start: Annotated[
        Optional[datetime],
        Field(
            alias="periodStart",
            description="The UTC date and time when the current time period started",
        ),
    ] = None
    period_end: Annotated[
        Optional[datetime],
        Field(
            alias="periodEnd",
            description="The UTC date and time when the current time period ends",
        ),
    ] = None


class ParallelTrainingJobs(CustomBaseModel):
    current: Annotated[
        Optional[int],
        Field(description="The number of currently running training jobs"),
    ] = None
    limit: Annotated[
        Optional[int],
        Field(
            description="The maximum number of running training jobs at any time. If empty, then there is no limit."
        ),
    ] = None


class ParallelGenerationJobs(CustomBaseModel):
    current: Annotated[
        Optional[int],
        Field(description="The number of currently running generation jobs"),
    ] = None
    limit: Annotated[
        Optional[int],
        Field(
            description="The maximum number of running generation jobs at any time. If empty, then there is no limit."
        ),
    ] = None


class UserUsage(CustomBaseModel):
    credits: Optional[Credits] = None
    parallel_training_jobs: Annotated[
        Optional[ParallelTrainingJobs], Field(alias="parallelTrainingJobs")
    ] = None
    parallel_generation_jobs: Annotated[
        Optional[ParallelGenerationJobs], Field(alias="parallelGenerationJobs")
    ] = None


class Metadata(CustomBaseModel):
    created_at: Annotated[
        Optional[datetime],
        Field(
            alias="createdAt",
            description="The UTC date and time when the resource has been created.\n",
            example="2023‐09‐07T18:40:39Z",
        ),
    ] = None
    owner_id: Annotated[
        Optional[str],
        Field(
            alias="ownerId",
            description="The unique identifier of the owner of the entity",
        ),
    ] = None
    owner_name: Annotated[
        Optional[str],
        Field(alias="ownerName", description="The name of the owner of the entity"),
    ] = None
    current_user_permission_level: Annotated[
        Optional[PermissionLevel], Field(alias="currentUserPermissionLevel")
    ] = None


class PaginatedTotalCount(RootModel[int]):
    root: Annotated[
        int, Field(description="The total number of entities within the list")
    ]


class ModelEncodingType(str, Enum):
    """
    The encoding type used for model training and data generation.
    This property is only relevant if generation method is AI_MODEL.
    - CATEGORICAL: Model samples from existing (non-rare) categories.
    - NUMERIC_AUTO: Model chooses among 3 numeric encoding types based on the values.
    - NUMERIC_DISCRETE: Model samples from existing discrete numerical values.
    - NUMERIC_BINNED: Model samples from binned buckets, to then sample randomly within a bucket.
    - NUMERIC_DIGIT: Model samples each digit of a numerical value.
    - CHARACTER: Model samples each character of a string value.
    - DATETIME: Model samples each part of a datetime value.
    - DATETIME_RELATIVE: Model samples the relative difference between datetimes within a sequence.
    - LAT_LONG: Model samples a latitude-longitude column. The format is "latitude,longitude".
    - TEXT_MODEL: Model will train a distinct TEXT model for this column.

    """

    categorical = "CATEGORICAL"
    numeric_auto = "NUMERIC_AUTO"
    numeric_discrete = "NUMERIC_DISCRETE"
    numeric_binned = "NUMERIC_BINNED"
    numeric_digit = "NUMERIC_DIGIT"
    character = "CHARACTER"
    datetime = "DATETIME"
    datetime_relative = "DATETIME_RELATIVE"
    lat_long = "LAT_LONG"
    text_model = "TEXT_MODEL"


class ConnectorAccessType(str, Enum):
    source = "SOURCE"
    destination = "DESTINATION"


class ConnectorType(str, Enum):
    mysql = "MYSQL"
    postgres = "POSTGRES"
    mssql = "MSSQL"
    oracle = "ORACLE"
    mariadb = "MARIADB"
    snowflake = "SNOWFLAKE"
    bigquery = "BIGQUERY"
    databricks = "DATABRICKS"
    azure_storage = "AZURE_STORAGE"
    google_cloud_storage = "GOOGLE_CLOUD_STORAGE"
    s3_storage = "S3_STORAGE"
    file_upload = "FILE_UPLOAD"
    hive = "HIVE"


class ConnectorTestConnection(RootModel[bool]):
    root: Annotated[
        bool,
        Field(
            description="If true, the connection will be tested before saving. In case of error, the connector will not be saved.\nIf false, the connection will not be tested.\n"
        ),
    ]


class ConnectorListItem(CustomBaseModel):
    id: Annotated[str, Field(description="The unique identifier of a connector")]
    name: Annotated[str, Field(description="The name of a connector")]
    type: ConnectorType
    access_type: Annotated[ConnectorAccessType, Field(alias="accessType")]
    metadata: Metadata


class Connector(CustomBaseModel):
    id: Annotated[str, Field(description="The unique identifier of a connector")]
    name: Annotated[str, Field(description="The name of a connector")]
    type: ConnectorType
    access_type: Annotated[ConnectorAccessType, Field(alias="accessType")]
    config: Optional[Dict[str, Any]] = None
    secrets: Optional[Dict[str, str]] = None
    ssl: Optional[Dict[str, str]] = None
    metadata: Optional[Metadata] = None
    table_id: Annotated[
        Optional[str],
        Field(
            alias="tableId",
            description="Optional. ID of a source table or a synthetic table, that this connector belongs to.\nIf not set, then this connector is managed independently of any generator or synthetic dataset.\n",
        ),
    ] = None
    OPEN_URL_PARTS: ClassVar[list] = ["d", "connectors"]

    def update(self, config) -> "Connector":
        """
        Update a connector, and optionally validate the connection before saving.

        If validation fails, a 400 status with an error message will be returned.

        For the structure of the config, secrets and ssl parameters, see the CREATE method.

        :return: The updated connector
        """
        return self.client._update(connector_id=self.id, config=config)

    def delete(self):
        """
        Delete connector
        """
        return self.client._delete(connector_id=self.id)

    def locations(self, prefix: str = "") -> list:
        """
        List connector locations

        List the available databases, schemas, tables or folders for a connector.
        For storage connectors, this returns list of folders and files at root, respectively at `prefix` level.
        For DB connectors, this returns list of schemas (or databases for DBs without schema), respectively list of tables if `prefix` is provided.

        :param prefix: The prefix to filter the results by.
        :return: A list of locations (schemas, databases, directories, etc.) on the given level.
        """
        return self.client._locations(connector_id=self.id, prefix=prefix)

    def config(self) -> dict[str, Any]:
        """
        Retrieve writeable generator properties

        :return: The generator properties as dictionary
        """
        return self.client._config(connector_id=self.id)

    def shares(self):
        return self.client._shares(resource=self)


class GeneratorUsage(CustomBaseModel):
    total_datapoints: Annotated[
        Optional[int],
        Field(
            alias="totalDatapoints",
            description="The total number of datapoints generated by this generator.",
        ),
    ] = None
    total_compute_time: Annotated[
        Optional[int],
        Field(
            alias="totalComputeTime",
            description="The total compute time in seconds used for training this generator. \nThis is the sum of the compute time of all trained tasks.\n",
        ),
    ] = None


class SourceTableData(RootModel[str]):
    root: Annotated[
        str,
        Field(
            description="The base64-encoded string derived from a Parquet file containing the specified source table.\n"
        ),
    ]


class SourceTableIncludeChildren(RootModel[bool]):
    root: Annotated[
        bool,
        Field(
            description="If true, all tables that are referenced by foreign keys will\nbe included. If false, only the selected table will be included.\n"
        ),
    ]


class SourceColumn(CustomBaseModel):
    id: Annotated[str, Field(description="The unique identifier of a source column")]
    name: Annotated[str, Field(description="The name of a source column")]
    included: Annotated[
        bool,
        Field(
            description="If true, the column will be included in the training.\nIf false, the column will be excluded from the training.\n"
        ),
    ]
    model_encoding_type: Annotated[ModelEncodingType, Field(alias="modelEncodingType")]


class SourceForeignKey(CustomBaseModel):
    id: Annotated[str, Field(description="The unique identifier of a foreign key")]
    column: Annotated[
        Optional[str], Field(description="The column name of a foreign key.")
    ] = None
    referenced_table: Annotated[
        str,
        Field(
            alias="referencedTable",
            description="The table name of the referenced table. That table must have a primary key already defined.",
        ),
    ]
    is_context: Annotated[
        bool,
        Field(
            alias="isContext",
            description="If true, then the foreign key will be considered as a context relation.\nNote, that only one foreign key relation per table can be a context relation.\n",
        ),
    ]


class ModelSize(str, Enum):
    """
    The size of the model, with the default being M(edium).
    Choose S(mall) for faster training, or L(arge) for better results for large dataset.
    Note, that larger model sizes will require more memory and more compute.

    """

    s = "S"
    m = "M"
    l = "L"


class RareCategoryReplacementMethod(str, Enum):
    """
    Specifies, if the rare categories for categoricals will be replaced by a constant
    _RARE_ or by a sample from non-rare categories.

    """

    constant = "CONSTANT"
    sample = "SAMPLE"


class ModelConfiguration(CustomBaseModel):
    """
    The training configuration for a AI model
    """

    max_sample_size: Annotated[
        Optional[int],
        Field(
            alias="maxSampleSize",
            description="The maximum number of samples to consider for training.\nIf not provided, then all available samples will be taken.\n",
            ge=1,
            le=1000000000,
        ),
    ] = None
    batch_size: Annotated[
        Optional[int],
        Field(
            alias="batchSize",
            description="The batch size used for training the model.\nIf not provided, batchSize will be chosen automatically.\n",
            ge=1,
            le=1000000,
        ),
    ] = None
    model_size: Annotated[
        Optional[ModelSize],
        Field(
            alias="modelSize",
            description="The size of the model, with the default being M(edium).\nChoose S(mall) for faster training, or L(arge) for better results for large dataset.\nNote, that larger model sizes will require more memory and more compute.\n",
        ),
    ] = "M"
    max_training_time: Annotated[
        Optional[int],
        Field(
            alias="maxTrainingTime",
            description="The maximum number of minutes to train the model.",
            ge=0,
            le=100000,
        ),
    ] = 10
    max_epochs: Annotated[
        Optional[int],
        Field(
            alias="maxEpochs",
            description="The maximum number of epochs to train the model.",
            ge=0,
            le=100000,
        ),
    ] = 100
    max_sequence_window: Annotated[
        Optional[int],
        Field(
            alias="maxSequenceWindow",
            description="The maximum sequence window to consider for training.",
            ge=1,
            le=100000,
        ),
    ] = 100
    enable_flexible_generation: Annotated[
        Optional[bool],
        Field(
            alias="enableFlexibleGeneration",
            description="If true, then the trained generator can be used for rebalancing and imputation.\n",
        ),
    ] = True
    value_protection: Annotated[
        Optional[bool],
        Field(
            alias="valueProtection",
            description="Defines if Rare Category, Extreme value, or Sequence length protection will be applied.\n",
        ),
    ] = True
    rare_category_replacement_method: Annotated[
        Optional[RareCategoryReplacementMethod],
        Field(
            alias="rareCategoryReplacementMethod",
            description="Specifies, if the rare categories for categoricals will be replaced by a constant \n_RARE_ or by a sample from non-rare categories.\n",
        ),
    ] = "CONSTANT"


class Accuracy(CustomBaseModel):
    overall: Annotated[
        Optional[float],
        Field(description="The overall accuracy of the model.", ge=0.0, le=1.0),
    ] = None
    univariate: Annotated[
        Optional[float],
        Field(description="The univariate accuracy of the model.", ge=0.0, le=1.0),
    ] = None
    bivariate: Annotated[
        Optional[float],
        Field(description="The bivariate accuracy of the model.", ge=0.0, le=1.0),
    ] = None
    coherence: Annotated[
        Optional[float],
        Field(
            description="The coherence accuracy of the model, in case of sequential data.",
            ge=0.0,
            le=1.0,
        ),
    ] = None
    overall_max: Annotated[
        Optional[float],
        Field(
            alias="overallMax",
            description="The overall accuracy for an actual holdout dataset.\nThis serves as a reference for the overall accuracy of the trained generator.\n",
            ge=0.0,
            le=1.0,
        ),
    ] = None


class Distances(CustomBaseModel):
    dcr_original: Annotated[
        Optional[float],
        Field(
            alias="dcrOriginal",
            description="The average DCR between the original records.",
        ),
    ] = None
    dcr_synthetic: Annotated[
        Optional[float],
        Field(
            alias="dcrSynthetic",
            description="The average DCR between the synthetic and the original records.",
        ),
    ] = None


class ModelMetrics(CustomBaseModel):
    accuracy: Optional[Accuracy] = None
    distances: Optional[Distances] = None


class StepCode(str, Enum):
    pull_training_data = "PULL_TRAINING_DATA"
    analyze_training_data = "ANALYZE_TRAINING_DATA"
    encode_training_data = "ENCODE_TRAINING_DATA"
    train_model = "TRAIN_MODEL"
    generate_model_report_data = "GENERATE_MODEL_REPORT_DATA"
    create_model_report = "CREATE_MODEL_REPORT"
    finalize_training = "FINALIZE_TRAINING"
    pull_context_data = "PULL_CONTEXT_DATA"
    generate_data = "GENERATE_DATA"
    create_data_report = "CREATE_DATA_REPORT"
    finalize_generation = "FINALIZE_GENERATION"
    deliver_data = "DELIVER_DATA"


class ProgressValue(CustomBaseModel):
    value: Optional[int] = None
    max: Optional[int] = None


class ProgressStatus(str, Enum):
    """
    The status of a job or a step.
    NEW: The job/step is being configured, and has not started yet
    ON_HOLD: The job/step has been started, but is kept on hold
    QUEUED: The job/step has been started, and is awaiting for resources to execute
    IN_PROGRESS: The job/step is currently running
    DONE: The job/step has finished successfully
    FAILED: The job/step has failed
    CANCELED: The job/step has been canceled

    """

    new = "NEW"
    on_hold = "ON_HOLD"
    queued = "QUEUED"
    in_progress = "IN_PROGRESS"
    done = "DONE"
    failed = "FAILED"
    canceled = "CANCELED"


class SyntheticDatasetUsage(CustomBaseModel):
    total_datapoints: Annotated[
        Optional[int],
        Field(
            alias="totalDatapoints",
            description="The number of datapoints in the synthetic dataset",
        ),
    ] = None
    total_credits: Annotated[
        Optional[float],
        Field(
            alias="totalCredits",
            description="The number of credits used for the synthetic dataset",
        ),
    ] = None
    total_compute_time: Annotated[
        Optional[int],
        Field(
            alias="totalComputeTime",
            description="The total compute time in seconds used for generating this synthetic dataset. \nThis is the sum of the compute time of all trained tasks.\n",
        ),
    ] = None


class SyntheticDatasetListItem(CustomBaseModel):
    id: Annotated[
        str, Field(description="The unique identifier of a synthetic dataset")
    ]
    metadata: Metadata
    name: Annotated[str, Field(description="The name of a synthetic dataset")]
    description: Annotated[
        Optional[str], Field(description="The description of a synthetic dataset")
    ] = None
    generation_status: Annotated[ProgressStatus, Field(alias="generationStatus")]
    generation_time: Annotated[
        Optional[datetime],
        Field(
            alias="generationTime",
            description="The UTC date and time when the generation has finished.",
        ),
    ] = None
    usage: Optional[SyntheticDatasetUsage] = None


class SyntheticDatasetFormat(str, Enum):
    csv = "CSV"
    parquet = "PARQUET"
    xlsx = "XLSX"


class SyntheticDatasetReportType(str, Enum):
    model = "MODEL"
    data = "DATA"


class SyntheticTableRebalancing(CustomBaseModel):
    """
    Configure rebalancing of the table.
    Only applicable for categorical columns of a subject table.

    """

    column: Annotated[
        Optional[str],
        Field(
            description="The name of the column to be rebalanced.\nThat column must be of modelEncodingType CATEGORICAL.\n"
        ),
    ] = None
    probabilities: Annotated[
        Optional[Dict[str, float]],
        Field(
            description="The target distribution of samples values. \nThe keys are the categorical values, and the values are the probabilities.\n",
            example=[{"US": 0.8}, {"male": 0.5, "female": 0.5}],
        ),
    ] = None


class SyntheticTableConfiguration(CustomBaseModel):
    """
    The sample configuration for a synthetic table
    """

    sample_size: Annotated[
        Optional[int],
        Field(
            alias="sampleSize",
            description="Number of generated samples. Only applicable for subject tables.\n",
            ge=1,
        ),
    ] = None
    sample_seed_connector_id: Annotated[
        Optional[str],
        Field(
            alias="sampleSeedConnectorId",
            description="The connector id of the seed data for conditional generation. \nOnly applicable for subject tables.\n",
        ),
    ] = None
    sample_seed_data: Annotated[
        Optional[str],
        Field(
            alias="sampleSeedData",
            description="The base64-encoded string derived from a Parquet file containing the specified sample seed data.\n",
        ),
    ] = None
    sampling_temperature: Annotated[
        Optional[float],
        Field(
            alias="samplingTemperature",
            description="temperature for sampling",
            ge=0.0,
            le=10.0,
        ),
    ] = None
    sampling_top_p: Annotated[
        Optional[float],
        Field(alias="samplingTopP", description="topP for sampling", ge=0.0, le=1.0),
    ] = None
    rebalancing: Optional[SyntheticTableRebalancing] = None
    imputation: Annotated[
        Optional[List[str]],
        Field(
            description="Specify a list of column names that are to be imputed.\nImputed columns will suppress the sampling of NULL values.\n"
        ),
    ] = None


class SyntheticTableName(RootModel[str]):
    root: Annotated[
        str,
        Field(
            description="The name of a synthetic table. This matches the name of a corresponding SourceTable."
        ),
    ]


class ForeignKey(CustomBaseModel):
    column: Annotated[str, Field(description="The column name of a foreign key.")]
    referenced_table: Annotated[
        str,
        Field(
            alias="referencedTable",
            description="The table name of the referenced table. That table must have a primary key already defined.",
        ),
    ]
    is_context: Annotated[
        bool,
        Field(
            alias="isContext",
            description="If true, then the foreign key will be considered as a context relation.\nNote, that only one foreign key relation per table can be a context relation.\n",
        ),
    ]


class SyntheticTable(CustomBaseModel):
    id: Annotated[
        Optional[str], Field(description="The unique identifier of a synthetic table")
    ] = None
    name: Annotated[
        Optional[str],
        Field(
            description="The name of a source table. It must be unique within a generator."
        ),
    ] = None
    configuration: Optional[SyntheticTableConfiguration] = None
    model_metrics: Annotated[Optional[ModelMetrics], Field(alias="modelMetrics")] = None
    foreign_keys: Annotated[
        Optional[List[ForeignKey]],
        Field(alias="foreignKeys", description="The foreign keys of this table."),
    ] = None


class SyntheticDatasetDelivery(CustomBaseModel):
    overwrite_tables: Annotated[
        bool,
        Field(
            alias="overwriteTables",
            description="If true, tables in the destination will be overwritten.\nIf false, any tables exist, the delivery will fail.\n",
        ),
    ]
    destination_connector_id: Annotated[
        str,
        Field(
            alias="destinationConnectorId",
            description="The unique identifier of a connector",
        ),
    ]
    location: Annotated[
        str, Field(description="The location for the destination connector.")
    ]


class BaseResource(CustomBaseModel):
    id: Annotated[
        Optional[str], Field(description="The unique identifier of the entity")
    ] = None
    name: Annotated[Optional[str], Field(description="The name of the entity")] = None
    uri: Annotated[
        Optional[str],
        Field(
            description="The API service endpoint of the entity",
            example="/generators/94c77249-42bf-443a-8e17-6e18a19d60b8",
        ),
    ] = None
    current_user_permission_level: Annotated[
        Optional[PermissionLevel], Field(alias="currentUserPermissionLevel")
    ] = None


class User(CustomBaseModel):
    id: Annotated[
        Optional[str], Field(description="The unique identifier of a user")
    ] = None
    name: Annotated[Optional[str], Field(description="The name of a user")] = None
    email: Annotated[Optional[str], Field(description="The email of a user")] = None


class CurrentUser(CustomBaseModel):
    id: Annotated[
        Optional[str], Field(description="The unique identifier of a user")
    ] = None
    name: Annotated[Optional[str], Field(description="The name of a user")] = None
    email: Annotated[Optional[str], Field(description="The email of a user")] = None
    settings: Optional[Dict[str, Any]] = None
    usage: Optional[UserUsage] = None


class GeneratorListItem(CustomBaseModel):
    id: Annotated[str, Field(description="The unique identifier of a generator")]
    name: Annotated[Optional[str], Field(description="The name of a generator")] = None
    description: Annotated[
        Optional[str], Field(description="The description of a generator")
    ] = None
    training_status: Annotated[ProgressStatus, Field(alias="trainingStatus")]
    training_time: Annotated[
        Optional[datetime],
        Field(
            alias="trainingTime",
            description="The UTC date and time when the training has finished.",
        ),
    ] = None
    usage: Optional[GeneratorUsage] = None
    metadata: Metadata
    accuracy: Annotated[
        Optional[float],
        Field(
            description="The overall accuracy of the trained generator.\nThis is the average of the overall accuracy scores of all trained models.\n"
        ),
    ] = None


class SourceTable(CustomBaseModel):
    id: Annotated[str, Field(description="The unique identifier of a source table")]
    source_connector: Annotated[
        Optional[BaseResource], Field(alias="sourceConnector")
    ] = None
    location: Annotated[
        Optional[str],
        Field(
            description="The location of a source table. Together with the source connector it uniquely\nidentifies a source, and samples data from there.\n"
        ),
    ] = None
    name: Annotated[
        str,
        Field(
            description="The name of a source table. It must be unique within a generator."
        ),
    ]
    primary_key: Annotated[
        Optional[str],
        Field(alias="primaryKey", description="The column name of the primary key"),
    ] = None
    columns: Annotated[
        List[SourceColumn], Field(description="The columns of this generator table.")
    ]
    foreign_keys: Annotated[
        Optional[List[SourceForeignKey]],
        Field(alias="foreignKeys", description="The foreign keys of a table."),
    ] = None
    model_metrics: Annotated[Optional[ModelMetrics], Field(alias="modelMetrics")] = None
    model_configuration: Annotated[
        Optional[ModelConfiguration], Field(alias="modelConfiguration")
    ] = None
    text_model_configuration: Annotated[
        Optional[ModelConfiguration], Field(alias="textModelConfiguration")
    ] = None
    total_rows: Annotated[
        Optional[int],
        Field(
            alias="totalRows",
            description="The total number of rows in the source table while fetching data for training.\n",
        ),
    ] = None

    def model_qa_report(self):
        if self.client and hasattr(self.client, "model_qa_report"):
            return self.client.model_qa_report(
                generator_id=self.extra_key_values["generator_id"], table_id=self.id
            )

    def model_samples(self, **kwargs):
        if self.client and hasattr(self.client, "model_samples"):
            return self.client.model_qa_report(
                generator_id=self.extra_key_values["generator_id"],
                table_id=self.id,
                **kwargs,
            )

    def get_column(self, column_id: str):
        if self.client and hasattr(self.client, "get_column"):
            return self.client.get_column(
                generator_id=self.extra_key_values["generator_id"],
                table_id=self.id,
                column_id=column_id,
            )

    def create_foreign_key(self, **kwargs):
        if self.client and hasattr(self.client, "create_foreign_key"):
            return self.client.create_foreign_key(
                generator_id=self.extra_key_values["generator_id"],
                table_id=self.id,
                **kwargs,
            )

    def update_foreign_key(self, **kwargs):
        if self.client and hasattr(self.client, "update_foreign_key"):
            return self.client.update_foreign_key(
                generator_id=self.extra_key_values["generator_id"],
                table_id=self.id,
                **kwargs,
            )

    def delete_foreign_key(self, **kwargs):
        if self.client and hasattr(self.client, "delete_foreign_key"):
            return self.client.delete_foreign_key(
                generator_id=self.extra_key_values["generator_id"],
                table_id=self.id,
                **kwargs,
            )


class ProgressStep(CustomBaseModel):
    id: Optional[str] = None
    model_label: Annotated[
        Optional[str],
        Field(
            alias="modelLabel",
            description="The unique label for the model, consisting of table name and an optional suffix for text model.\nThis will be empty for steps that are not related to a model.\n",
            example=["census", "census:text"],
        ),
    ] = None
    step_code: Annotated[Optional[StepCode], Field(alias="stepCode")] = None
    start_date: Annotated[
        Optional[datetime],
        Field(
            alias="startDate",
            description="The UTC date and time when the job has started.\nIf the job has not started yet, then this is None.\n",
            example="2024-01-25T12:34:56Z",
        ),
    ] = None
    end_date: Annotated[
        Optional[datetime],
        Field(
            alias="endDate",
            description="The UTC date and time when the job has ended. \nIf the job is still, then this is None.\n",
            example="2024-01-25T12:34:56Z",
        ),
    ] = None
    messages: Optional[List[Dict[str, Any]]] = None
    progress: Optional[ProgressValue] = None
    status: Optional[ProgressStatus] = None


class SyntheticDataset(CustomBaseModel):
    id: Annotated[
        str, Field(description="The unique identifier of a synthetic dataset")
    ]
    generator: Optional[BaseResource] = None
    metadata: Metadata
    name: Annotated[str, Field(description="The name of a synthetic dataset")]
    description: Annotated[
        Optional[str], Field(description="The description of a synthetic dataset")
    ] = None
    generation_status: Annotated[ProgressStatus, Field(alias="generationStatus")]
    generation_time: Annotated[
        Optional[datetime],
        Field(
            alias="generationTime",
            description="The UTC date and time when the generation has finished.",
        ),
    ] = None
    tables: Annotated[
        Optional[List[SyntheticTable]],
        Field(description="The tables of this synthetic dataset."),
    ] = None
    delivery: Optional[SyntheticDatasetDelivery] = None
    accuracy: Annotated[
        Optional[float],
        Field(
            description="The overall accuracy of the trained generator.\nThis is the average of the overall accuracy scores of all trained models.\n"
        ),
    ] = None
    usage: Optional[SyntheticDatasetUsage] = None
    OPEN_URL_PARTS: ClassVar[list] = ["d", "synthetic-datasets"]
    generation: Annotated[Optional[Any], Field(exclude=True)] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generation = self.Generation(self)

    def update(self, config) -> "SyntheticDataset":
        """
        Update synthetic dataset

        See config for the structure of the parameters.

        :return: The updated synthetic dataset
        """
        return self.client._update(synthetic_dataset_id=self.id, config=config)

    def delete(self):
        """
        Delete synthetic dataset
        """
        return self.client._delete(synthetic_dataset_id=self.id)

    def config(self) -> dict[str, Any]:
        """
        Retrieve writeable synthetic dataset properties

        :return: The synthetic dataset properties as dictionary
        """
        return self.client._config(synthetic_dataset_id=self.id)

    def download(
        self,
        format: SyntheticDatasetFormat = "PARQUET",
        file_path: Union[str, Path, None] = None,
    ) -> Path:
        """
        Download synthetic dataset and save to file

        :param format: The format of the synthetic dataset
        :param file_path: The file path to save the synthetic dataset
        """
        bytes, filename = self.client._download(
            synthetic_dataset_id=self.id, ds_format=format
        )
        file_path = Path(file_path or ".")
        if file_path.is_dir():
            file_path = file_path / filename
        file_path.write_bytes(bytes)
        return file_path

    def data(
        self, return_type: Literal["auto", "dict"] = "auto"
    ) -> Union[pd.DataFrame, dict[str, pd.DataFrame]]:
        """
        Download synthetic dataset and return as dictionary of pandas DataFrames

        :return: The synthetic dataset as dictionary of pandas DataFrames
        """
        dfs = self.client._data(synthetic_dataset_id=self.id)
        if return_type == "auto" and len(dfs) == 1:
            return list(dfs.values())[0]
        else:
            return dfs

    def shares(self):
        return self.client._shares(resource=self)

    class Generation:
        def __init__(self, _synthetic_dataset: "SyntheticDataset"):
            self.synthetic_dataset = _synthetic_dataset

        def start(self) -> None:
            """
            Start generation
            """
            return self.synthetic_dataset.client._generation_start(
                self.synthetic_dataset.id
            )

        def cancel(self) -> None:
            """
            Cancel generation
            """
            return self.synthetic_dataset.client._generation_cancel(
                self.synthetic_dataset.id
            )

        def progress(self) -> JobProgress:
            """
            Retrieve job progress of generation
            """
            return self.synthetic_dataset.client._generation_progress(
                self.synthetic_dataset.id
            )

        def wait(self, interval: float = 2) -> "SyntheticDataset":
            """
            Poll generation progress and loop until generation has completed

            :param interval: The interval in seconds to poll the job progress
            """
            return self.synthetic_dataset.client._generation_wait(
                self.synthetic_dataset.id, interval=interval
            )


class Share(User):
    permission_level: Annotated[
        Optional[PermissionLevel], Field(alias="permissionLevel")
    ] = None


class Generator(CustomBaseModel):
    id: Annotated[str, Field(description="The unique identifier of a generator")]
    name: Annotated[Optional[str], Field(description="The name of a generator")] = None
    description: Annotated[
        Optional[str], Field(description="The description of a generator")
    ] = None
    training_status: Annotated[ProgressStatus, Field(alias="trainingStatus")]
    training_time: Annotated[
        Optional[datetime],
        Field(
            alias="trainingTime",
            description="The UTC date and time when the training has finished.",
        ),
    ] = None
    usage: Optional[GeneratorUsage] = None
    metadata: Metadata
    accuracy: Annotated[
        Optional[float],
        Field(
            description="The overall accuracy of the trained generator.\nThis is the average of the overall accuracy scores of all trained models.\n"
        ),
    ] = None
    tables: Annotated[
        Optional[List[SourceTable]], Field(description="The tables of this generator")
    ] = None
    OPEN_URL_PARTS: ClassVar[list] = ["d", "generators"]
    training: Annotated[Optional[Any], Field(exclude=True)] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.training = self.Training(self)

    def update(self, config) -> "Generator":
        """
        Update generator

        See config for the structure of the parameters.

        :return: The updated generator
        """
        return self.client._update(generator_id=self.id, config=config)

    def delete(self):
        """
        Delete generator
        """
        return self.client._delete(generator_id=self.id)

    def config(self) -> dict[str, Any]:
        """
        Retrieve writeable generator properties

        :return: The generator properties as dictionary
        """
        return self.client._config(generator_id=self.id)

    def shares(self):
        return self.client._shares(resource=self)

    class Training:
        def __init__(self, _generator: "Generator"):
            self.generator = _generator

        def start(self) -> None:
            """
            Start training
            """
            return self.generator.client._training_start(self.generator.id)

        def cancel(self) -> None:
            """
            Cancel training
            """
            return self.generator.client._training_cancel(self.generator.id)

        def progress(self) -> JobProgress:
            """
            Retrieve job progress of training
            """
            return self.generator.client._training_progress(self.generator.id)

        def wait(self, interval: float = 2) -> "Generator":
            """
            Poll training progress and loop until training has completed

            :param interval: The interval in seconds to poll the job progress
            """
            return self.generator.client._training_wait(
                self.generator.id, interval=interval
            )

        def list_synthetic_dataset(self) -> list["SyntheticDataset"]:
            """
            List synthetic datasets

            List the synthetic datasets that were created based on this generator.

            :return: A list of synthetic datasets
            """
            raise "Not implemented yet."
            # return self.generator.client._list_synthetic_datasets(self.generator.id)
            pass


class JobProgress(CustomBaseModel):
    id: Optional[str] = None
    start_date: Annotated[
        Optional[datetime],
        Field(
            alias="startDate",
            description="The UTC date and time when the job has started.\nIf the job has not started yet, then this is None.\n",
            example="2024-01-25T12:34:56Z",
        ),
    ] = None
    end_date: Annotated[
        Optional[datetime],
        Field(
            alias="endDate",
            description="The UTC date and time when the job has ended. \nIf the job is still, then this is None.\n",
            example="2024-01-25T12:34:56Z",
        ),
    ] = None
    progress: Optional[ProgressValue] = None
    status: Optional[ProgressStatus] = None
    steps: Optional[List[ProgressStep]] = None
