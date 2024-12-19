# Copyright 2024 MOSTLY AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
from typing import Any, Optional, Union, Literal

import pandas as pd
import rich

from mostlyai.client.base import GET, _MostlyBaseClient
from mostlyai.client.connectors import _MostlyConnectorsClient
from mostlyai.client.generators import _MostlyGeneratorsClient
from mostlyai.domain import (
    Connector,
    CurrentUser,
    Generator,
    ProgressStatus,
    SyntheticDataset,
    ModelType,
    ConnectorConfig,
    GeneratorConfig,
    SourceTableConfig,
    SyntheticDatasetConfig,
    SyntheticProbeConfig,
    AboutService,
)
from mostlyai.client.synthetic_datasets import (
    _MostlySyntheticDatasetsClient,
    _MostlySyntheticProbesClient,
)
from mostlyai.client._base_utils import convert_to_base64
from mostlyai.client._mostly_utils import (
    read_table_from_path,
    harmonize_sd_config,
    Seed,
)


class MostlyAI(_MostlyBaseClient):
    """
    Instantiate a client for interacting with the MOSTLY AI platform via its [Public API](https://github.com/mostly-ai/mostly-openapi/blob/main/public-api.yaml).

    Example for instantiating the client with explicit arguments:
        ```python
        from mostlyai import MostlyAI
        mostly = MostlyAI(
            api_key='INSERT_YOUR_API_KEY',
            base_url='https://app.mostly.ai',
        )
        mostly
        # MostlyAI(base_url='https://app.mostly.ai', api_key='***')
        ```

    Example for instantiating the client with environment variables:
        ```python
        import os
        from mostlyai import MostlyAI
        os.environ["MOSTLYAI_API_KEY"] = "INSERT_YOUR_API_KEY"
        os.environ["MOSTLYAI_BASE_URL"] = "https://app.mostly.ai"
        mostly = MostlyAI()
        mostly
        # MostlyAI(base_url='https://app.mostly.ai', api_key='***')
        ```

    Args:
        base_url: The base URL. If not provided, a default value is used.
        api_key: The API key for authenticating. If not provided, it would rely on environment variables.
        timeout: Timeout for HTTPS requests in seconds.
        ssl_verify: Whether to verify SSL certificates.
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
        try:
            version = self.about().version
            email = self.me().email
            rich.print(
                f"Connected to {self.base_url} ({version}) as [bold]{email}[/bold]"
            )
        except Exception as e:
            rich.print(f"Failed to connect to {self.base_url}: {e}")

    def __repr__(self) -> str:
        api_key = "'***'" if self.api_key else "None"
        return f"MostlyAI(base_url='{self.base_url}', api_key={api_key})"

    def connect(
        self,
        config: Union[ConnectorConfig, dict[str, Any]],
        test_connection: Optional[bool] = True,
    ) -> Connector:
        """
        Create a connector and optionally validate the connection before saving.

        See [ConnectorConfig](api_domain.md#mostlyai.domain.ConnectorConfig) for more information on the available configuration parameters.

        Example for creating a connector to a AWS S3 storage:
            ```python
            from mostlyai import MostlyAI
            mostly = MostlyAI()
            c = mostly.connect(
                config={
                    'type': 'S3_STORAGE',
                    'config': {
                        'accessKey': '...',
                    },
                    'secrets': {
                        'secretKey': '...'
                    }
                }
            )
            ```

        Args:
            config: Configuration for the connector. Can be either a ConnectorConfig object or an equivalent dictionary.
            test_connection: Whether to validate the connection before saving.

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

        Returns:
            Connector: The created connector.
        """
        c = self.connectors.create(config=config, test_connection=test_connection)
        rich.print(
            f"Created connector [link={self.base_url}/d/connectors/{c.id} blue underline]{c.id}[/]"
        )
        return c

    def train(
        self,
        config: Union[GeneratorConfig, dict, None] = None,
        data: Union[pd.DataFrame, str, Path, None] = None,
        name: Optional[str] = None,
        start: bool = True,
        wait: bool = True,
        progress_bar: bool = True,
    ) -> Generator:
        """
        Train a generator.

        See [GeneratorConfig](api_domain.md#mostlyai.domain.GeneratorConfig) for more information on the available configuration parameters.

        Example configuration using short-hand notation:
            ```python
            from mostlyai import MostlyAI
            mostly = MostlyAI()
            g = mostly.train(
                name='census',
                data=df_original
            )
            ```

        Example configuration using GeneratorConfig:
            ```python
            from mostlyai import MostlyAI
            mostly = MostlyAI()
            g = mostly.train(
                config=GeneratorConfig(
                    name='census',
                    tables=[
                        SourceTableConfig(
                            name='data',
                            data=df_original
                        )
                    ]
                )
            )
            ```

        Example configuration using a dictionary:
            ```python
            from mostlyai import MostlyAI
            mostly = MostlyAI()
            g = mostly.train(
                config={
                    'name': 'census',
                    'tables': [
                        {
                            'name': 'data',
                            'data': df_original
                        }
                    ]
                }
            )
            ```

        Args:
            config: The configuration parameters of the generator to be created. Either `config` or `data` must be provided.
            data: A single pandas DataFrame, or a path to a CSV or PARQUET file. Either `config` or `data` must be provided.
            name: Name of the generator.
            start: Whether to start training immediately.
            wait: Whether to wait for training to finish.
            progress_bar: Whether to display a progress bar during training.

        Returns:
            Generator: The created generator.
        """
        if data is None and config is None:
            raise ValueError("Either config or data must be provided")
        if data is not None and config is not None:
            raise ValueError("Either config or data must be provided, but not both")
        if config is not None and isinstance(config, (pd.DataFrame, str, Path)) is None:
            # map config to data, in case user incorrectly provided data as first argument
            data = config
        if isinstance(data, (str, Path)):
            name, df = read_table_from_path(data)
            config = GeneratorConfig(
                name=name,
                tables=[SourceTableConfig(data=convert_to_base64(df), name=name)],
            )
        elif isinstance(data, pd.DataFrame):
            df = data
            config = GeneratorConfig(
                name=f"DataFrame {df.shape}",
                tables=[SourceTableConfig(data=convert_to_base64(df), name="data")],
            )
        if isinstance(config, dict):
            config = GeneratorConfig(**config)
        if name is not None:
            config.name = name
        g = self.generators.create(config)
        rich.print(
            f"Created generator [link={self.base_url}/d/generators/{g.id} blue underline]{g.id}[/]"
        )
        if start:
            g.training.start()
            rich.print("Started generator training")
        if start and wait:
            g.training.wait(progress_bar=progress_bar)
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
        config: Union[SyntheticDatasetConfig, dict, None] = None,
        size: Union[int, dict[str, int], None] = None,
        seed: Union[Seed, dict[str, Seed], None] = None,
        name: Optional[str] = None,
        start: bool = True,
        wait: bool = True,
        progress_bar: bool = True,
    ) -> SyntheticDataset:
        """
        Generate synthetic data.

        See [SyntheticDatasetConfig](api_domain.md#mostlyai.domain.SyntheticDatasetConfig) for more information on the available configuration parameters.

        Example configuration using short-hand notation:
            ```python
            from mostlyai import MostlyAI
            mostly = MostlyAI()
            sd = mostly.generate(generator=g, size=1000)
            ```

        Example configuration using SyntheticDatasetConfig:
            ```python
            from mostlyai import MostlyAI
            mostly = MostlyAI()
            sd = mostly.generate(
                config=SyntheticDatasetConfig(
                    generator=g,
                    tables=[
                        SyntheticTableConfig(
                            name="data",
                            configuration=SyntheticTableConfiguration(
                                sample_size=1000,
                                sampling_temperature=0.9,
                            )
                        )
                    ]
                )
            )
            ```

        Example configuration using a dictionary:
            ```python
            from mostlyai import MostlyAI
            mostly = MostlyAI()
            sd = mostly.generate(
                config={
                    'generator': g,
                    'tables': [
                        {
                            'name': 'data',
                            'configuration': {
                                'sample_size': 1000,
                                'sampling_temperature': 0.9,
                            }
                        }
                    ]
                }
            )
            ```

        Args:
            generator: The generator instance or its UUID.
            config: Configuration for the synthetic dataset.
            size : Sample size(s) for the subject table(s).
            seed: Seed data for the subject table(s).
            name: Name of the synthetic dataset.
            start: Whether to start generation immediately.
            wait: Whether to wait for generation to finish.
            progress_bar: Whether to display a progress bar during generation.

        Returns:
            SyntheticDataset: The created synthetic dataset.
        """
        config = harmonize_sd_config(
            generator,
            get_generator=self.generators.get,
            size=size,
            seed=seed,
            config=config,
            config_type=SyntheticDatasetConfig,
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
            sd.generation.wait(progress_bar=progress_bar)
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
        config: Union[SyntheticProbeConfig, dict, None] = None,
        return_type: Literal["auto", "dict"] = "auto",
    ) -> Union[pd.DataFrame, dict[str, pd.DataFrame]]:
        """
        Probe a generator.

        See [SyntheticProbeConfig](api_domain.md#mostlyai.domain.SyntheticProbeConfig) for more information on the available configuration parameters.

        Example for probing a generator for 10 synthetic samples:
            ```python
            from mostlyai import MostlyAI
            mostly = MostlyAI()
            probe = mostly.probe(
                generator='INSERT_YOUR_GENERATOR_ID',
                size=10
            )
            ```

        Example for conditional probing a generator for 10 synthetic samples:
            ```python
            import pandas as pd
            from mostlyai import MostlyAI
            mostly = MostlyAI()
            g = mostly.generators.get('INSERT_YOUR_GENERATOR_ID')
            print('columns:', [c.name for c in g.tables[0].columns])
            # columns: ['age', 'workclass', 'fnlwgt', ...]
            col = g.tables[0].columns[1]
            print(col.name, col.value_range.values)
            # workclass: ['Federal-gov', 'Local-gov', 'Never-worked', ...]
            mostly.probe(
                generator=g,
                seed=pd.DataFrame({
                    'age': [63, 45],
                    'sex': ['Female', 'Male'],
                    'workclass': ['Sales', 'Tech-support'],
                }),
            )
            ```

        Args:
            generator: The generator instance or its UUID.
            size: Sample size(s) for the subject table(s).
            seed: Seed data for the subject table(s).
            config: Configuration for the probe.
            return_type: Format of the return value. "auto" for pandas DataFrame if a single table, otherwise a dictionary.

        Returns:
            The created synthetic probe.
        """
        config = harmonize_sd_config(
            generator,
            get_generator=self.generators.get,
            size=size,
            seed=seed,
            config=config,
            config_type=SyntheticProbeConfig,
        )
        dfs = self.synthetic_probes.create(config)
        if return_type == "auto" and len(dfs) == 1:
            return list(dfs.values())[0]
        else:
            return dfs

    def me(self) -> CurrentUser:
        """
        Retrieve information about the current user.

        Example for retrieving information about the current user:
            ```python
            from mostlyai import MostlyAI
            mostly = MostlyAI()
            mostly.me()
            # {'id': '488f2f26-...', 'first_name': 'Tom', ...}
            ```

        Returns:
            Information about the current user.
        """
        return self.request(verb=GET, path=["users", "me"], response_type=CurrentUser)

    def about(self) -> AboutService:
        """
        Retrieve information about the platform.

        Example for retrieving information about the platform:
            ```python
            from mostlyai import MostlyAI
            mostly = MostlyAI()
            mostly.about()
            # {'version': 'v316', 'assistant': True}
            ```

        Returns:
            Information about the platform.
        """
        return self.request(verb=GET, path=["about"], response_type=AboutService)

    def models(self, model_type: Union[str, ModelType]) -> list[str]:
        """
        Retrieve a list of available models of a specific type.

        Example for retrieving available models:
            ```python
            from mostlyai import MostlyAI
            mostly = MostlyAI()
            mostly.models("LANGUAGE")
            # ['MOSTLY_AI/LSTMFromScratch-3m', 'microsoft/phi-1_5', ..]
            mostly.models("TABULAR")
            # ['MOSTLY_AI/Small', 'MOSTLY_AI/Medium', 'MOSTLY_AI/Large']
            ```

        Args:
            model_type: The type of model to retrieve. Can be a string or a ModelType enum.

        Returns:
            A list of available models of the specified type.
        """
        if isinstance(model_type, ModelType):
            model_type = model_type.value
        return self.request(verb=GET, path=["models", model_type])

    def computes(self) -> list[dict[str, Any]]:
        """
        Retrieve a list of available compute resources, that can be used for executing tasks.

        Example for retrieving available compute resources:
            ```python
            from mostlyai import MostlyAI
            mostly = MostlyAI()
            mostly.computes()
            # [{'id': '...', 'name': 'CPU Large',...]
            ```

        Returns:
            A list of available compute resources.
        """
        return self.request(verb=GET, path=["computes"])
