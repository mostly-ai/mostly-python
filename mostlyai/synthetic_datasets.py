import io
import re
import zipfile
from pathlib import Path
from typing import Any, Iterator, Optional, Union

import pandas as pd

from mostlyai.base import DELETE, GET, PATCH, POST, Paginator, _MostlyBaseClient
from mostlyai.model import JobProgress, SyntheticDataset, SyntheticDatasetFormat
from mostlyai.utils import _convert_df_to_base64, _job_wait, _read_table_from_path


class _MostlySyntheticDatasetsClient(_MostlyBaseClient):
    SECTION = ["synthetic-datasets"]

    # PUBLIC METHODS #

    def list(
        self,
        offset: int = 0,
        limit: int = 50,
        status: Optional[Union[str, list[str]]] = None,
    ) -> Iterator[SyntheticDataset]:
        """
        List synthetic datasets.

        Paginate through all synthetic datasets that the user has access to.

        :param offset: Offset the entities in the response. Optional. Default: 0
        :param limit: Limit the number of entities in the response. Optional. Default: 50
        :param status: Filter by generation status. Optional. Default: None
        :return: Iterator over synthetic datasets.
        """
        status = ",".join(status) if isinstance(status, list) else status
        with Paginator(
            self, SyntheticDataset, offset=offset, limit=limit, status=status
        ) as paginator:
            for item in paginator:
                yield item

    def get(self, synthetic_dataset_id: str) -> SyntheticDataset:
        """
        Retrieve synthetic dataset

        :param synthetic_dataset_id: The unique identifier of a synthetic dataset
        :return: The retrieved synthetic dataset
        """
        response = self.request(
            verb=GET, path=[synthetic_dataset_id], response_type=SyntheticDataset
        )
        return response

    def create(self, config: dict[str, Any]) -> SyntheticDataset:
        """
        Create synthetic dataset

        See SyntheticDataset.config for the structure of the parameters.

        :param config: The configuration parameters of the synthetic dataset to be created.
        :return: The created synthetic dataset.
        """
        # convert `sample_seed_data` to base64-encoded Parquet files
        tables = config["tables"] if "tables" in config else []
        for table in tables:
            if (
                "sampleSeedData" in table["configuration"]
                and table["configuration"]["sampleSeedData"] is not None
            ):
                if isinstance(table["configuration"]["sampleSeedData"], pd.DataFrame):
                    table["configuration"]["sampleSeedData"] = _convert_df_to_base64(
                        table["configuration"]["sampleSeedData"]
                    )
                elif isinstance(table["configuration"]["sampleSeedData"], (Path, str)):
                    _, df = _read_table_from_path(
                        table["configuration"]["sampleSeedData"]
                    )
                    table["configuration"]["sampleSeedData"] = _convert_df_to_base64(df)
                    del df
                else:
                    raise ValueError(
                        "sampleSeedData must be a DataFrame or a file path"
                    )
        # convert generator_id to str
        config["generatorId"] = str(config["generatorId"])
        synthetic_dataset = self.request(
            verb=POST,
            path=[],
            json=dict(config),
            response_type=SyntheticDataset,
        )
        return synthetic_dataset

    # PRIVATE METHODS #

    def _update(
        self, synthetic_dataset_id: str, config: dict[str, Any]
    ) -> SyntheticDataset:
        response = self.request(
            verb=PATCH,
            path=[synthetic_dataset_id],
            json=config,
            response_type=SyntheticDataset,
        )
        return response

    def _delete(self, synthetic_dataset_id: str) -> None:
        response = self.request(verb=DELETE, path=[synthetic_dataset_id])
        return response

    def _config(self, synthetic_dataset_id: str) -> SyntheticDataset:
        response = self.request(verb=GET, path=[synthetic_dataset_id, "config"])
        return response

    def _download(
        self,
        synthetic_dataset_id: str,
        ds_format: SyntheticDatasetFormat = SyntheticDatasetFormat.parquet,
    ) -> (bytes, Optional[str]):
        ds_format = ds_format.upper() if isinstance(ds_format, str) else ds_format.value
        response = self.request(
            verb=GET,
            path=[synthetic_dataset_id, "download"],
            params={"format": ds_format},
            headers={
                "Content-Type": "application/zip",
                "Accept": "application/json, text/plain, */*",
            },
            raw_response=True,
        )
        content_bytes = response.content
        # Check if 'Content-Disposition' header is present
        if "Content-Disposition" in response.headers:
            content_disposition = response.headers["Content-Disposition"]
            filename = re.findall("filename=(.+)", content_disposition)[0]
        else:
            filename = None
        return content_bytes, filename

    def _data(self, synthetic_dataset_id: str) -> dict[str, pd.DataFrame]:
        # download pqt
        pqt_zip_bytes, filename = self._download(
            synthetic_dataset_id, SyntheticDatasetFormat.parquet
        )
        # read each parquet file into a pandas dataframe
        with zipfile.ZipFile(io.BytesIO(pqt_zip_bytes), "r") as z:
            dir_list = set([name.split("/")[0] for name in z.namelist()])
            dfs = {}
            for table in dir_list:
                pqt_files = [
                    name
                    for name in z.namelist()
                    if name.startswith(f"{table}/") and name.endswith(".parquet")
                ]
                dfs[table] = pd.concat(
                    [pd.read_parquet(z.open(name)) for name in pqt_files], axis=0
                )
                dfs[table].name = table
        return dfs

    def _generation_start(self, synthetic_dataset_id: str) -> None:
        response = self.request(
            verb=POST, path=[synthetic_dataset_id, "generation", "start"]
        )
        return response

    def _generation_cancel(self, synthetic_dataset_id: str) -> None:
        response = self.request(
            verb=POST, path=[synthetic_dataset_id, "generation", "cancel"]
        )
        return response

    def _generation_progress(self, synthetic_dataset_id: str) -> JobProgress:
        response = self.request(
            verb=GET,
            path=[synthetic_dataset_id, "generation"],
            response_type=JobProgress,
        )
        return response

    def _generation_wait(
        self, synthetic_dataset_id: str, interval: float
    ) -> SyntheticDataset:
        _job_wait(lambda: self._generation_progress(synthetic_dataset_id), interval)
        synthetic_dataset = self.get(synthetic_dataset_id)
        return synthetic_dataset
