from pathlib import Path
from typing import Any, Optional
from uuid import UUID

import pandas as pd

from mostlyai.base import _MostlyBaseClient
from mostlyai.connectors import _MostlyConnectorsClient
from mostlyai.generators import _MostlyGeneratorsClient
from mostlyai.model import Connector, Generator
from mostlyai.synthetic_datasets import _MostlySyntheticDatasetsClient
from mostlyai.utils import _convert_df_to_base64


class MostlyAI(_MostlyBaseClient):
    """
    Client for interacting with the Mostly AI Public API.

    :param base_url: The base URL. If not provided, a default value is used.
    :param api_key: The API key for authenticating. If not provided, it would rely on env vars.
    """

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__(base_url=base_url, api_key=api_key)
        client_kwargs = {"base_url": self.base_url, "api_key": self.api_key}
        self.connectors = _MostlyConnectorsClient(**client_kwargs)
        self.generators = _MostlyGeneratorsClient(**client_kwargs)
        self.synthetic_datasets = _MostlySyntheticDatasetsClient(**client_kwargs)

    def connect(self, config: dict[str, Any]) -> Connector:
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

        :return: The created connector.
        """
        return self.connectors.create(config)

    def train(
        self,
        data_or_config: pd.DataFrame | str | Path | dict[str, Any],
        start: bool = True,
        wait: bool = True,
    ):
        """
        Train a generator

        :param data_or_config: Either a single pandas DataFrame data, a path to a CSV or PARQUET file, or a dictionary with the configuration parameters of the generator to be created. See Generator.config for the structure of the parameters.
        :param start: If true, then training is started right away. Default: true.
        :param wait: If true, then the function only returns once training has finished. Default: true.
        :return: The created generator.
        """
        if isinstance(data_or_config, (str, Path)):
            # read data from file
            fn = str(data_or_config)
            if fn.lower().endswith((".pqt", ".parquet")):
                df = pd.read_parquet(fn)
            else:
                df = pd.read_csv(fn)
            name = Path(fn).stem
            config = {"name": name, "tables": [{"data": df, "name": name}]}
        elif isinstance(data_or_config, pd.DataFrame):
            df = data_or_config
            config = {
                "name": f"DataFrame {df.shape}",
                "tables": [{"data": df, "name": "data"}],
            }
        elif isinstance(data_or_config, dict):
            config = data_or_config
        else:
            raise ValueError(
                "data_or_config must be a DataFrame, a file path or a dictionary"
            )

        g = self.generators.create(config)
        print(f"generator {g.id} created")
        if start:
            print(f"start training")
            g.training.start()
        if start and wait:
            print(f"wait for training to finish")
            g = g.training.wait()
            print(f"finished training")
        return g

    def generate(
        self,
        generator: Generator | str | UUID | None,
        config: dict | None = None,
        size: int | dict[str, int] | None = None,  # TODO
        seed: pd.DataFrame
        | str
        | Path
        | dict[str, pd.DataFrame | str | Path]
        | None = None,  # TODO
        start: bool = True,
        wait: bool = True,
    ):
        """
        Train a generator

        :param generator: The generator instance or its UUID, that is to be used for generating synthetic data.
        :param config: The configuration parameters of the synthetic dataset to be created. See SyntheticDataset.config for the structure of the parameters.
        :param seed: Either a single pandas DataFrame data, or a path to a CSV or PARQUET file. Used for seeding the subject table.
        :param start: If true, then generation is started right away. Default: true.
        :param wait: If true, then the function only returns once generation has finished. Default: true.
        :return: The created synthetic dataset.
        """
        if config is None:
            config = {}
        if isinstance(generator, Generator):
            config["generatorId"] = str(generator.id)
        elif generator is not None:
            config["generatorId"] = str(generator)
        elif "generatorId" not in config:
            raise ValueError(
                "Either a generator or a configuration with a generatorId must be provided."
            )
        if seed is not None:
            if isinstance(seed, (str, Path)):
                fn = str(seed)
                if fn.lower().endswith((".pqt", ".parquet")):
                    seed_df = pd.read_parquet(fn)
                else:
                    seed_df = pd.read_csv(fn)
            elif isinstance(seed, pd.DataFrame):
                seed_df = seed
            else:
                raise ValueError("seed must be a DataFrame or a file path")
            config["tables"][0]["sampleSeedData"] = seed_df

        sd = self.synthetic_datasets.create(config)
        print(f"synthetic dataset {sd.id} created")
        if start:
            print(f"start generation")
            sd.generation.start()
        if start and wait:
            print(f"wait for generation to finish")
            sd = sd.generation.wait()
            print(f"finished generation")
        return sd
