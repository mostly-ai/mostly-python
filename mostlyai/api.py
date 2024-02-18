from pathlib import Path
from typing import Optional
from uuid import UUID

import pandas as pd

from mostlyai.base import _MostlyBaseClient
from mostlyai.connectors import _MostlyConnectorsClient
from mostlyai.generators import _MostlyGeneratorsClient
from mostlyai.model import Generator
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

    def train(self, data_or_config: pd.DataFrame | str | Path | dict, start: bool = True, wait: bool = True):
        """
        Train a generator

        :param data_or_config: Either a single pandas DataFrame data, a path to a CSV or PARQUET file, or a dictionary with the configuration parameters of the generator to be created. See Generator.to_dict for the structure of the parameters.
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
            config = {"name": f"DataFrame {df.shape}", "tables": [{"data": df, "name": "data"}]}
        elif isinstance(data_or_config, dict):
            config = data_or_config
        else:
            raise ValueError("data_or_config must be a DataFrame, a file path or a dictionary")

        # convert `data` to base64-encoded Parquet files
        if "tables" in config:
            for table in config["tables"]:
                if "data" in table:
                    if isinstance(table["data"], (str, Path)):
                        fn = str(table["data"])
                        if fn.lower().endswith((".pqt", ".parquet")):
                            df = pd.read_parquet(fn)
                        else:
                            df = pd.read_csv(fn)
                        name = Path(fn).stem
                        table["data"] = _convert_df_to_base64(df)
                        if "name" not in table:
                            table["name"] = name
                        del df
                    elif isinstance(table["data"], pd.DataFrame):
                        table["data"] = _convert_df_to_base64(table["data"])
                    else:
                        raise ValueError("data must be a DataFrame or a file path")

        g = self.generators.create(**config)
        if start:
            g.training.start()
        if start and wait:
            g = g.training.wait()
        return g

    def generate(self, generator: Optional[Generator | str | UUID], config: Optional[dict] = None, start: bool = True, wait: bool = True):
        """
        Train a generator

        :param generator: The generator instance or its UUID, that is to be used for generating synthetic data.
        :param config: The configuration parameters of the synthetic dataset to be created. See SyntheticDataset.to_dict for the structure of the parameters.
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
            raise ValueError("Either a generator or a configuration with a generatorId must be provided.")

        sd = self.synthetic_datasets.create(**config)
        if start:
            sd.generation.start()
        if start and wait:
            sd = sd.generation.wait()
        return sd
