from pathlib import Path
from typing import Annotated, Any, ClassVar, Literal, Optional, Union

import pandas as pd
from pydantic import Field, field_validator

from mostlyai.client._base_utils import convert_to_base64
from mostlyai.client.model import (
    JobProgress,
    SyntheticDatasetFormat,
    ConnectorPatchConfig,
    GeneratorPatchConfig,
    SyntheticDatasetDelivery,
    SyntheticDatasetPatchConfig,
    SyntheticDatasetConfig,
    GeneratorConfig,
)


class Connector:
    OPEN_URL_PARTS: ClassVar[list] = ["d", "connectors"]

    def update(
        self,
        name: Optional[str] = None,
        config: Optional[dict[str, Any]] = None,
        secrets: Optional[dict[str, str]] = None,
        ssl: Optional[dict[str, str]] = None,
        test_connection: Optional[bool] = None,
    ) -> "Connector":
        """
        Update a connector with specific parameters.

        Args:
            name: The name of the connector.
            config (dict[str, Any], optional): Connector configuration.
            secrets (dict[str, str], optional): Secret values for the connector.
            ssl (dict[str, str], optional): SSL configuration for the connector.
            test_connection: If true, validates the connection before saving.

        Returns:
            Connector: The updated connector object.
        """
        patch_config = ConnectorPatchConfig(
            name=name,
            config=config,
            secrets=secrets,
            ssl=ssl,
            test_connection=test_connection,
        )
        return self.client._update(
            connector_id=self.id, config=patch_config.model_dump(exclude_none=True)
        )

    def delete(self) -> None:
        """
        Delete the connector.

        Returns:
            None
        """
        return self.client._delete(connector_id=self.id)

    def locations(self, prefix: str = "") -> list:
        """
        List connector locations.

        List the available databases, schemas, tables, or folders for a connector.
        For storage connectors, this returns list of folders and files at root, respectively at `prefix` level.
        For DB connectors, this returns list of schemas (or databases for DBs without schema), respectively list of tables if `prefix` is provided.

        The formats of the locations are:

        - Cloud storage:
            - `AZURE_STORAGE`: `container/path`
            - `GOOGLE_CLOUD_STORAGE`: `bucket/path`
            - `S3_STORAGE`: `bucket/path`
        - Database:
            - `BIGQUERY`: `dataset.table`
            - `DATABRICKS`: `schema.table`
            - `HIVE`: `database.table`
            - `MARIADB`: `database.table`
            - `MSSQL`: `schema.table`
            - `MYSQL`: `database.table`
            - `ORACLE`: `schema.table`
            - `POSTGRES`: `schema.table`
            - `SNOWFLAKE`: `schema.table`

        Args:
            prefix: The prefix to filter the results by.

        Returns:
            list: A list of locations (schemas, databases, directories, etc.)."""
        return self.client._locations(connector_id=self.id, prefix=prefix)

    def schema(self, location: str) -> list[dict[str, Any]]:
        """
        Retrieve the schema of the table at a connector location.
        Please refer to `locations()` for the format of the location.

        Args:
            location: The location of the table.

        Returns:
            list[dict[str, Any]]: The retrieved schema.
        """
        return self.client._schema(connector_id=self.id, location=location)

    def shares(self):
        return self.client._shares(resource=self)


class Generator:
    OPEN_URL_PARTS: ClassVar[list] = ["d", "generators"]
    training: Annotated[Optional[Any], Field(exclude=True)] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.training = self.Training(self)

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> "Generator":
        """
        Update a generator with specific parameters.

        Args:
            name: The name of the generator.
            description: The description of the generator.

        Returns:
            Generator: The updated generator object.
        """
        patch_config = GeneratorPatchConfig(
            name=name,
            description=description,
        )
        return self.client._update(
            generator_id=self.id, config=patch_config.model_dump(exclude_none=True)
        )

    def delete(self) -> None:
        """
        Delete the generator.

        Returns:
            None
        """
        return self.client._delete(generator_id=self.id)

    def config(self) -> GeneratorConfig:
        """
        Retrieve writable generator properties.

        Returns:
            GeneratorConfig: The generator properties as a configuration object.
        """
        return self.client._config(generator_id=self.id)

    def shares(self):
        return self.client._shares(resource=self)

    def export_to_file(
        self,
        file_path: Union[str, Path, None] = None,
    ) -> Path:
        """
        Export generator and save to file.

        Args:
            file_path (Union[str, Path, None], optional): The file path to save the generator.

        Returns:
            Path: The path to the saved file.
        """
        bytes, filename = self.client._export_to_file(generator_id=self.id)
        file_path = Path(file_path or ".")
        if file_path.is_dir():
            file_path = file_path / filename
        file_path.write_bytes(bytes)
        return file_path

    def clone(self, training_status: Literal["NEW", "CONTINUE"] = "NEW") -> "Generator":
        """
        Clone the generator.

        Args:
            training_status (Literal["NEW", "CONTINUE"]): The training status of the cloned generator.

        Returns:
            Generator: The cloned generator object.
        """
        return self.client._clone(generator_id=self.id, training_status=training_status)

    class Training:
        def __init__(self, _generator: "Generator"):
            self.generator = _generator

        def start(self) -> None:
            """
            Start training.

            Returns:
                None
            """
            return self.generator.client._training_start(self.generator.id)

        def cancel(self) -> None:
            """
            Cancel training.

            Returns:
                None
            """
            return self.generator.client._training_cancel(self.generator.id)

        def progress(self) -> JobProgress:
            """
            Retrieve job progress of training.

            Returns:
                JobProgress: The job progress of the training process.
            """
            return self.generator.client._training_progress(self.generator.id)

        def wait(self, progress_bar: bool = True, interval: float = 2) -> "Generator":
            """
            Poll training progress and loop until training has completed.

            Args:
                progress_bar: If true, displays the progress bar.
                interval: The interval in seconds to poll the job progress.

            Returns:
                Generator: The generator after training has completed.
            """
            return self.generator.client._training_wait(
                self.generator.id, progress_bar=progress_bar, interval=interval
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


class SourceTableConfig:
    @field_validator("data", mode="before")
    @classmethod
    def validate_data_before(cls, value):
        return convert_to_base64(value) if isinstance(value, pd.DataFrame) else value


class SyntheticTableConfiguration:
    @field_validator("sample_seed_dict", mode="before")
    @classmethod
    def validate_dict_before(cls, value):
        return (
            convert_to_base64(value, format="jsonl")
            if isinstance(value, dict)
            else value
        )

    @field_validator("sample_seed_data", mode="before")
    @classmethod
    def validate_data_before(cls, value):
        return convert_to_base64(value) if isinstance(value, pd.DataFrame) else value


class SyntheticDataset:
    OPEN_URL_PARTS: ClassVar[list] = ["d", "synthetic-datasets"]
    generation: Annotated[Optional[Any], Field(exclude=True)] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generation = self.Generation(self)

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        delivery: Optional[SyntheticDatasetDelivery] = None,
    ) -> "SyntheticDataset":
        """
        Update a synthetic dataset with specific parameters.

        Args:
            name: The name of the synthetic dataset.
            description: The description of the synthetic dataset.
            delivery: The delivery configuration for the synthetic dataset.

        Returns:
            SyntheticDataset: The updated synthetic dataset object.
        """
        patch_config = SyntheticDatasetPatchConfig(
            name=name,
            description=description,
            delivery=delivery,
        )
        return self.client._update(
            synthetic_dataset_id=self.id,
            config=patch_config.model_dump(exclude_none=True),
        )

    def delete(self) -> None:
        """
        Delete the synthetic dataset.

        Returns:
            None
        """
        return self.client._delete(synthetic_dataset_id=self.id)

    def config(self) -> SyntheticDatasetConfig:
        """
        Retrieve writable synthetic dataset properties.

        Returns:
            SyntheticDatasetConfig: The synthetic dataset properties as a configuration object.
        """
        return self.client._config(synthetic_dataset_id=self.id)

    def download(
        self,
        format: SyntheticDatasetFormat = "PARQUET",
        file_path: Union[str, Path, None] = None,
    ) -> Path:
        """
        Download synthetic dataset and save to file.

        Args:
            format: The format of the synthetic dataset.
            file_path (Union[str, Path, None], optional): The file path to save the synthetic dataset.

        Returns:
            Path: The path to the saved file.
        """
        bytes, filename = self.client._download(
            synthetic_dataset_id=self.id,
            ds_format=format,
            short_lived_file_token=self.metadata.short_lived_file_token,
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
        Download synthetic dataset and return as dictionary of pandas DataFrames.

        Args:
            return_type (Literal["auto", "dict"]): The format of the returned data.

        Returns:
            Union[pd.DataFrame, dict[str, pd.DataFrame]]: The synthetic dataset as a dictionary of pandas DataFrames.
        """
        dfs = self.client._data(
            synthetic_dataset_id=self.id,
            short_lived_file_token=self.metadata.short_lived_file_token,
        )
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
            Start the generation process.

            Returns:
                None
            """
            return self.synthetic_dataset.client._generation_start(
                self.synthetic_dataset.id
            )

        def cancel(self) -> None:
            """
            Cancel the generation process.

            Returns:
                None
            """
            return self.synthetic_dataset.client._generation_cancel(
                self.synthetic_dataset.id
            )

        def progress(self) -> JobProgress:
            """
            Retrieve the progress of the generation process.

            Returns:
                JobProgress: The progress of the generation process.
            """
            return self.synthetic_dataset.client._generation_progress(
                self.synthetic_dataset.id
            )

        def wait(
            self, progress_bar: bool = True, interval: float = 2
        ) -> "SyntheticDataset":
            """
            Poll the generation progress and wait until the process is complete.

            Args:
                progress_bar: If true, displays a progress bar.
                interval: Interval in seconds to poll the job progress.

            Returns:
                SyntheticDataset: The synthetic dataset after the generation process is complete.
            """
            return self.synthetic_dataset.client._generation_wait(
                self.synthetic_dataset.id, progress_bar=progress_bar, interval=interval
            )
