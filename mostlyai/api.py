from pathlib import Path
from typing import Any, Optional, Union

import pandas as pd
import rich

from mostlyai.base import _MostlyBaseClient
from mostlyai.connectors import _MostlyConnectorsClient
from mostlyai.generators import _MostlyGeneratorsClient
from mostlyai.model import (
    Connector,
    Generator,
    PermissionLevel,
    ProgressStatus,
    SyntheticDataset,
)
from mostlyai.shares import _MostlySharesClient
from mostlyai.synthetic_datasets import _MostlySyntheticDatasetsClient
from mostlyai.utils import (
    ShareableResource,
    _get_subject_table_names,
    _read_table_from_path,
)


class MostlyAI(_MostlyBaseClient):
    """
    Client for interacting with the Mostly AI Public API.

    :param base_url: The base URL. If not provided, a default value is used.
    :param api_key: The API key for authenticating. If not provided, it would rely on env vars.
    :param timeout: Timeout for HTTPS requests in seconds.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 60.0,
    ):
        super().__init__(base_url=base_url, api_key=api_key, timeout=timeout)
        client_kwargs = {
            "base_url": self.base_url,
            "api_key": self.api_key,
            "timeout": self.timeout,
        }
        self.connectors = _MostlyConnectorsClient(**client_kwargs)
        self.generators = _MostlyGeneratorsClient(**client_kwargs)
        self.synthetic_datasets = _MostlySyntheticDatasetsClient(**client_kwargs)
        self.shares = _MostlySharesClient(**client_kwargs)

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
        c = self.connectors.create(config)
        rich.print(
            f"Created connector [link={self.base_url}/d/connectors/{c.id} blue underline]{c.id}[/]"
        )
        return c

    def train(
        self,
        data: Union[pd.DataFrame, str, Path, None] = None,
        config: Union[dict, None] = None,
        name: Optional[str] = None,
        start: bool = True,
        wait: bool = True,
    ):
        """
        Train a generator

        :param data: Either a single pandas DataFrame data, a path to a CSV or PARQUET file. Note: Either 'data' or 'config' must be provided.
        :param config: The configuration parameters of the generator to be created. See Generator.config for the structure of the parameters. Note: Either 'data' or 'config' must be provided.
        :param name: Optional. The name of the generator.
        :param start: If true, then training is started right away. Default: true.
        :param wait: If true, then the function only returns once training has finished. Default: true.
        :return: The created generator.
        """
        if isinstance(data, (str, Path)):
            name, df = _read_table_from_path(data)
            config = {"name": name, "tables": [{"data": df, "name": name}]}
        elif isinstance(data, pd.DataFrame):
            df = data
            config = {
                "name": f"DataFrame {df.shape}",
                "tables": [{"data": df, "name": "data"}],
            }
        elif config is None:
            raise ValueError("Either data or config must be provided")
        if name is not None:
            config |= {"name": name}
        g = self.generators.create(config)
        rich.print(
            f"Created generator [link={self.base_url}/d/generators/{g.id} blue underline]{g.id}[/]"
        )
        if start:
            g.training.start()
            rich.print("Started generator training")
        if start and wait:
            g = g.training.wait()
            if g.training_status == ProgressStatus.done:
                rich.print(
                    ":tada: [bold green]Your generator is ready![/] "
                    "Use it to create synthetic data. "
                    "Share it so others can do the same."
                )
        return g

    def generate(
        self,
        generator: Union[Generator, str, None],
        size: Union[int, dict[str, int], None] = None,
        seed: Union[
            pd.DataFrame, str, Path, dict[str, Union[pd.DataFrame, str, Path]], None
        ] = None,
        config: Union[dict, None] = None,
        name: Optional[str] = None,
        start: bool = True,
        wait: bool = True,
    ):
        """
        Train a generator

        :param generator: The generator instance or its UUID, that is to be used for generating synthetic data.
        :param config: The configuration parameters of the synthetic dataset to be created. See SyntheticDataset.config for the structure of the parameters.
        :param size: Optional. Either a single integer, or a dictionary of integers. Used for specifying the sample_size of the subject table(s).
        :param seed: Optional. Either a single pandas DataFrame data, or a path to a CSV or PARQUET file, or a dictionary of those. Used for seeding the subject table(s).
        :param name: Optional. The name of the synthetic dataset.
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

        if "tables" not in config:
            g = self.generators.get(config["generatorId"])
            subject_tables = _get_subject_table_names(g.config())
            config["tables"] = [
                {
                    "name": table,
                    "configuration": {
                        "sampleSize": size.get(table)
                        if isinstance(size, dict)
                        else size,
                        "sampleSeedData": seed.get(table)
                        if isinstance(seed, dict)
                        else seed,
                    },
                }
                for table in subject_tables
            ]

        if name is not None:
            config |= {"name": name}

        sd = self.synthetic_datasets.create(config)
        rich.print(
            f"Created synthetic dataset "
            f"[link={self.base_url}/d/synthetic-datasets/{sd.id} blue underline]{sd.id}[/] "
            f"with generator "
            f"[link={self.base_url}/d/generators/{sd.generator.id} blue underline]{sd.generator.id}[/]"
        )
        if start:
            sd.generation.start()
            rich.print("Started synthetic dataset generation")
        if start and wait:
            sd = sd.generation.wait()
            if sd.generation_status == ProgressStatus.done:
                rich.print(
                    ":tada: [bold green]Your synthetic dataset is ready![/] "
                    "Use it to consume the generated data. "
                    "Share it so others can do the same."
                )
        return sd

    # SHARES

    def share(
        self,
        resource: Union[str, ShareableResource],
        user_email: str,
        permission_level: Union[str, PermissionLevel] = PermissionLevel.view,
    ):
        """
        Share a specified resource with a user by granting a specific permission level.

        :param resource: The resource to be shared. This can either be the resource ID as a string or an instance of a ShareableResource (Connector, Generator, or SyntheticDataset).
        :param user_email: The email address of the user with whom the resource is to be shared.
        :param permission_level: The level of permission to be granted. This can be a string or an instance of PermissionLevel. Default is PermissionLevel.view, which grants 'view' access.

        :return: None. The function outputs a confirmation message with the details of the sharing action.
        """
        if isinstance(resource, (Connector, Generator, SyntheticDataset)):
            resource_id = resource.id
        else:
            resource_id = str(resource)
        if isinstance(permission_level, PermissionLevel):
            permission_level = permission_level.value
        if permission_level == "ADMIN":
            raise ValueError(
                "ADMIN permission level is not supported. Transfer ownership via the UI."
            )
        self.shares._share(resource_id, user_email, permission_level)
        rich.print(
            f"Granted [bold]{user_email}[/] [grey]{permission_level}[/] access to resource [bold cyan]{resource_id}[/]"
        )

    def unshare(self, resource: Union[str, ShareableResource], user_email: str):
        """
        Unshare a specified resource from a user.

        :param resource: The resource from which access is being unshared. This can be the resource ID as a string or an instance of a ShareableResource (Connector, Generator, or SyntheticDataset).
        :param user_email: The email address of the user whose access to the resource is to be unshared.

        :return: None. The function outputs a confirmation message with the details of the revocation action.
        """
        if isinstance(resource, (Connector, Generator, SyntheticDataset)):
            resource_id = resource.id
        else:
            resource_id = str(resource)
        self.shares._unshare(resource, user_email)
        rich.print(
            f"Revoked access of resource [bold cyan]{resource_id}[/] for [bold]{user_email}[/]"
        )
