from pathlib import Path
from typing import Annotated, Any, Literal, Optional, Union

import pandas as pd
from pydantic import Field

from mostlyai.model import JobProgress, SyntheticDatasetFormat


class Connector:
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
        return self.client._shares(resource_id=self.id)


class Generator:
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
        return self.client._shares(resource_id=self.id)

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

        def wait(self, interval: float = 1) -> "Generator":
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


class SyntheticDataset:
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
        file_path: Union[str, Path, None] = None,
        format: Union[str, SyntheticDatasetFormat] = SyntheticDatasetFormat.parquet,
    ) -> Path:
        """
        Download synthetic dataset and save to file

        :param file_path: The file path to save the synthetic dataset
        :param format: The format of the synthetic dataset
        """
        bytes, filename = self.client._download(
            synthetic_dataset_id=self.id, format=format
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
        return self.client._shares(resource_id=self.id)

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

        def wait(self, interval: float = 1) -> "SyntheticDataset":
            """
            Poll generation progress and loop until generation has completed

            :param interval: The interval in seconds to poll the job progress
            """
            return self.synthetic_dataset.client._generation_wait(
                self.synthetic_dataset.id, interval=interval
            )
