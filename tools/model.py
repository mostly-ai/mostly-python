from typing import Optional, Annotated, Any

import pandas as pd
from pydantic import Field

from mostlyai.model import JobProgress


class Connector:
    def update(self, **kwargs) -> "Connector":
        """
        Update a connector, and optionally validate the connection before saving.

        If validation fails, a 400 status with an error message will be returned.

        For the structure of the config, secrets and ssl parameters, see the CREATE method.

        :param name: The name of a connector
        :param config: The config parameter contains any configuration of the connector
        :param secrets: The secrets parameter contains any sensitive credentials of the connector
        :param ssl: The ssl parameter contains any SSL related configurations of the connector
        :param testConnection: If true, the connection will be tested before saving
        :return: The updated connector
        """
        return self.client._update(connector_id=self.id, **kwargs)

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

    def to_dict(self) -> dict[str, Any]:
        """
        Retrieve writeable generator properties

        :return: The generator properties as dictionary
        """
        return self.client._to_dict(connector_id=self.id)


class Generator:
    training: Annotated[Optional[Any], Field(exclude=True)] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.training = self.Training(self)

    def update(self, **kwargs) -> "Generator":
        """
        Update generator

        See to_dict for the structure of the parameters.

        :return: The updated generator
        """
        return self.client._update(generator_id=self.id, **kwargs)

    def delete(self):
        """
        Delete generator
        """
        return self.client._delete(generator_id=self.id)

    def to_dict(self) -> dict[str, Any]:
        """
        Retrieve writeable generator properties

        :return: The generator properties as dictionary
        """
        return self.client.to_dict(generator_id=self.id)

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

        def wait(self, interval: float = 5) -> "Generator":
            """
            Poll training progress and loop until training has completed

            :param interval: The interval in seconds to poll the job progress
            """
            return self.generator.client._training_wait(
                self.generator.id, interval=interval
            )

        def generate(
            self, start: bool = True, wait: bool = True, **kwargs: dict[str, Any]
        ):
            """
            Generate a synthetic dataset based on this generator

            :param kwargs: The configuration parameters of the synthetic dataset to be created.
            :return: The synthetic dataset
            """
            raise "Not implemented yet. Call the client.synthetic_datasets.create method instead."
            # FIXME @michdr: how can we access the synthetic dataset client here?
            # return self.synthetic_datasets.create(generator_id=self.generator.id, start=start, wait=wait, **kwargs)
            pass

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

    def update(self, **kwargs) -> "SyntheticDataset":
        """
        Update synthetic dataset

        See to_dict for the structure of the parameters.

        :return: The updated synthetic dataset
        """
        return self.client._update(synthetic_dataset_id=self.id, **kwargs)

    def delete(self):
        """
        Delete synthetic dataset
        """
        return self.client._delete(synthetic_dataset_id=self.id)

    def to_dict(self) -> dict[str, Any]:
        """
        Retrieve writeable synthetic dataset properties

        :return: The synthetic dataset properties as dictionary
        """
        return self.client._to_dict(synthetic_dataset_id=self.id)

    def data(self) -> dict[str, pd.DataFrame]:
        """
        Download synthetic dataset and return as dictionary of pandas DataFrames

        :return: The synthetic dataset as dictionary of pandas DataFrames
        """
        return self.client._data(synthetic_dataset_id=self.id)

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

        def wait(self, interval: float = 5) -> "SyntheticDataset":
            """
            Poll generation progress and loop until generation has completed

            :param interval: The interval in seconds to poll the job progress
            """
            return self.synthetic_dataset.client._generation_wait(
                self.synthetic_dataset.id, interval=interval
            )
