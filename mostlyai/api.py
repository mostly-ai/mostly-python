from pathlib import Path
from typing import Any, Optional, Union, Literal

import pandas as pd
import rich

from mostlyai.base import GET, _MostlyBaseClient
from mostlyai.connectors import _MostlyConnectorsClient
from mostlyai.generators import _MostlyGeneratorsClient
from mostlyai.model import (
    Connector,
    CurrentUser,
    Generator,
    PermissionLevel,
    ProgressStatus,
    SyntheticDataset,
    ModelType,
)
from mostlyai.shares import _MostlySharesClient
from mostlyai.synthetic_datasets import (
    _MostlySyntheticDatasetsClient,
    _MostlySyntheticProbesClient,
)
from mostlyai.utils import (
    ShareableResource,
    _read_table_from_path,
    _harmonize_sd_config,
    Seed,
)


class MostlyAI(_MostlyBaseClient):
    """
    Client for interacting with the Mostly AI Public API.

    :param base_url: The base URL. If not provided, a default value is used.
    :param api_key: The API key for authenticating. If not provided, it would rely on env vars.
    :param timeout: Timeout for HTTPS requests in seconds.
    :param ssl_verify: Whether to verify SSL certificates.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 60.0,
        ssl_verify: bool = True,
    ):
        super().__init__(
            base_url=base_url, api_key=api_key, timeout=timeout, ssl_verify=ssl_verify
        )
        client_kwargs = {
            "base_url": self.base_url,
            "api_key": self.api_key,
            "timeout": self.timeout,
            "ssl_verify": self.ssl_verify,
        }
        self.connectors = _MostlyConnectorsClient(**client_kwargs)
        self.generators = _MostlyGeneratorsClient(**client_kwargs)
        self.synthetic_datasets = _MostlySyntheticDatasetsClient(**client_kwargs)
        self.synthetic_probes = _MostlySyntheticProbesClient(**client_kwargs)
        self.shares = _MostlySharesClient(**client_kwargs)

    def connect(self, config: dict[str, Any]) -> Connector:
        """
        Create a connector, and optionally validate the connection before saving.

        If validation fails, a 400 status with an error message will be returned.

        `config` is a dictionary with the keys `type`, `config`, `secrets`, and `ssl`.
        The structures of the `config`, `secrets` and `ssl` parameters depend on the connector `type`:

        - Cloud storage:
          ```yaml
          - type: AZURE_STORAGE
            config:
              accountName: string
              clientId: string (required for auth via service principal)
              tenantId: string (required for auth via service principal)
            secrets:
              accountKey: string (required for regular auth)
              clientSecret: string (required for auth via service principal)

          - type: GOOGLE_CLOUD_STORAGE
            config:
            secrets:
              keyFile: string

          - type: S3_STORAGE
            config:
              accessKey: string
              endpointUrl: string (only needed for S3-compatible storage services other than AWS)
            secrets:
              secretKey: string
          ```
        - Database:
          ```yaml
          - type: BIGQUERY
            config:
            secrets:
              keyFile: string

          - type: DATABRICKS
            config:
              host: string
              httpPath: string
              catalog: string
              clientId: string (required for auth via service principal)
              tenantId: string (required for auth via service principal)
            secrets:
              accessToken: string (required for regular auth)
              clientSecret: string (required for auth via service principal)

          - type: HIVE
            config:
              host: string
              port: integer, default: 10000
              username: string (required for regular auth)
              kerberosEnabled: boolean, default: false
              kerberosPrincipal: string (required if kerberosEnabled)
              kerberosKrb5Conf: string (required if kerberosEnabled)
              sslEnabled: boolean, default: false
            secrets:
              password: string (required for regular auth)
              kerberosKeytab: base64-encoded string (required if kerberosEnabled)
            ssl:
              caCertificate: base64-encoded string

          - type: MARIADB
            config:
              host: string
              port: integer, default: 3306
              username: string
            secrets:
              password: string

          - type: MSSQL
            config:
              host: string
              port: integer, default: 1433
              username: string
              database: string
            secrets:
             password: string

          - type: MYSQL
            config:
              host: string
              port: integer, default: 3306
              username: string
            secrets:
              password: string

          - type: ORACLE
            config:
              host: string
              port: integer, default: 1521
              username: string
              connectionType: enum {SID, SERVICE_NAME}, default: SID
              database: string, default: ORCL
            secrets:
              password: string

          - type: POSTGRES
            config:
              host: string
              port: integer, default: 5432
              username: string
              database: string
              sslEnabled: boolean, default: false
            secrets:
              password: string
            ssl:
              rootCertificate: base64-encoded string
              sslCertificate: base64-encoded string
              sslCertificateKey: base64-encoded string

          - type: SNOWFLAKE
            config:
              account: string
              username: string
              warehouse: string, default: COMPUTE_WH
              database: string
            secrets:
              password: string
          ```

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
        progress_bar: bool = True,
    ) -> Generator:
        """
        Train a generator

        :param data: Either a single pandas DataFrame data, a path to a CSV or PARQUET file. Note: Either 'data' or 'config' must be provided.
        :param config: The configuration parameters of the generator to be created. See Generator.config for the structure of the parameters. Note: Either 'data' or 'config' must be provided.
        :param name: Optional. The name of the generator.
        :param start: If true, then training is started right away. Default: true.
        :param wait: If true, then the function only returns once training has finished. Default: true.
        :param progress_bar: If true, then the progress bar will be displayed, in case of wait=True
        :return: The created generator.
        """
        if data is not None and config is not None:
            raise ValueError("Either data or config must be provided, but not both")
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
            g = g.training.wait(progress_bar=progress_bar)
            if g.training_status == ProgressStatus.done:
                rich.print(
                    ":tada: [bold green]Your generator is ready![/] "
                    "Use it to create synthetic data. "
                    "Share it so others can do the same."
                )
        return g

    def generate(
        self,
        generator: Union[Generator, str, None] = None,
        size: Union[int, dict[str, int], None] = None,
        seed: Union[Seed, dict[str, Seed], None] = None,
        config: Union[dict, None] = None,
        name: Optional[str] = None,
        start: bool = True,
        wait: bool = True,
        progress_bar: bool = True,
    ) -> SyntheticDataset:
        """
        Generate synthetic data

        :param generator: The generator instance or its UUID, that is to be used for generating synthetic data.
        :param config: The configuration parameters of the synthetic dataset to be created. See SyntheticDataset.config for the structure of the parameters.
        :param size: Optional. Either a single integer, or a dictionary of integers. Used for specifying the sample_size of the subject table(s).
        :param seed: Optional. Either a single pandas DataFrame data, or a path to a CSV or PARQUET file, or a dictionary of those. Used for seeding the subject table(s).
        :param name: Optional. The name of the synthetic dataset.
        :param start: If true, then generation is started right away. Default: true.
        :param wait: If true, then the function only returns once generation has finished. Default: true.
        :param progress_bar: If true, then the progress bar will be displayed, in case of wait=True
        :return: The created synthetic dataset.
        """
        config = _harmonize_sd_config(
            generator,
            get_generator=self.generators.get,
            size=size,
            seed=seed,
            config=config,
            name=name,
        )
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
            sd = sd.generation.wait(progress_bar=progress_bar)
            if sd.generation_status == ProgressStatus.done:
                rich.print(
                    ":tada: [bold green]Your synthetic dataset is ready![/] "
                    "Use it to consume the generated data. "
                    "Share it so others can do the same."
                )
        return sd

    def probe(
        self,
        generator: Union[Generator, str, None] = None,
        size: Union[int, dict[str, int], None] = None,
        seed: Union[Seed, dict[str, Seed], None] = None,
        config: Union[dict, None] = None,
        return_type: Literal["auto", "dict"] = "auto",
    ) -> Union[pd.DataFrame, dict[str, pd.DataFrame]]:
        """
        Probe a generator

        :param generator: The generator instance or its UUID, that is to be used for generating synthetic data.
        :param config: The configuration parameters of the synthetic dataset to be created. See SyntheticDataset.config for the structure of the parameters.
        :param size: Optional. Either a single integer, or a dictionary of integers. Used for specifying the sample_size of the subject table(s).
        :param seed: Optional. Either a single pandas DataFrame data, or a path to a CSV or PARQUET file, or list of samples, or a dictionary of those. Used for seeding the subject table(s).
        :return: The created synthetic probe.
        """
        config = _harmonize_sd_config(
            generator,
            get_generator=self.generators.get,
            size=size,
            seed=seed,
            config=config,
        )
        dfs = self.synthetic_probes.create(config)
        if return_type == "auto" and len(dfs) == 1:
            return list(dfs.values())[0]
        else:
            return dfs

    # SHARES

    def share(
        self,
        resource: ShareableResource,
        user_email: str,
        permission_level: Union[str, PermissionLevel] = PermissionLevel.view,
    ):
        """
        Share a specified resource with a user by granting a specific permission level.

        :param resource: The resource to be shared. This must be an instance of a ShareableResource (Connector, Generator, or SyntheticDataset).
        :param user_email: The email address of the user with whom the resource is to be shared.
        :param permission_level: The level of permission to be granted. This can be a string or an instance of PermissionLevel. Default is PermissionLevel.view, which grants 'view' access.

        :return: None. The function outputs a confirmation message with the details of the sharing action.
        """
        if isinstance(permission_level, PermissionLevel):
            permission_level = permission_level.value
        if permission_level == "ADMIN":
            raise ValueError(
                "ADMIN permission level is not supported. Transfer ownership via the UI."
            )
        self.shares._share(resource, user_email, permission_level)
        rich.print(
            f"Granted [bold]{user_email}[/] [grey]{permission_level}[/] access to resource [bold cyan]{resource.id}[/]"
        )

    def unshare(self, resource: ShareableResource, user_email: str):
        """
        Unshare a specified resource from a user.

        :param resource: The resource from which access is being unshared. This must be an instance of a ShareableResource (Connector, Generator, or SyntheticDataset).
        :param user_email: The email address of the user whose access to the resource is to be unshared.

        :return: None. The function outputs a confirmation message with the details of the revocation action.
        """
        self.shares._unshare(resource, user_email)
        rich.print(
            f"Revoked access of resource [bold cyan]{resource.id}[/] for [bold]{user_email}[/]"
        )

    def me(self) -> CurrentUser:
        """
        Retrieve current user info.
        :return: info about the current user.
        """
        return self.request(verb=GET, path=["users", "me"], response_type=CurrentUser)

    def about(self) -> dict[str, Any]:
        """
        Retrieve about info from the endpoint.
        Supported from release v210 onwards.
        :return: info about the platform.
        """
        return self.request(verb=GET, path=["about"])

    def models(self, model_type: Union[str, ModelType]) -> list[str]:
        if isinstance(model_type, ModelType):
            model_type = model_type.value
        return self.request(verb=GET, path=["models", model_type])

    def computes(self) -> list[dict[str, Any]]:
        return self.request(verb=GET, path=["computes"])
