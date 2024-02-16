import io
import zipfile
from typing import Iterator, Any, Optional
import pandas as pd
from mostlyai.base import (
    POST,
    Paginator,
    StrUUID,
    _MostlyBaseClient,
    GET,
    PATCH,
    DELETE,
)
from mostlyai.utils import _job_wait, _convert_df_to_base64
from mostlyai.model import (
    SyntheticDataset,
    SyntheticDatasetFormat,
    JobProgress,
)


class _MostlySyntheticDatasetsClient(_MostlyBaseClient):
    SECTION = ["synthetic-datasets"]

    def list(self, offset: int = 0, limit: int = 50) -> Iterator[SyntheticDataset]:
        """
        List synthetic datasets.

        Paginate through all synthetic datasets that the user has access to.

        :param offset: Offset the entities in the response. Optional. Default: 0
        :param limit: Limit the number of entities in the response. Optional. Default: 50
        :return: Iterator over synthetic datasets.
        """
        with Paginator(self, SyntheticDataset, offset=offset, limit=limit) as paginator:
            for item in paginator:
                yield item

    def get(self, synthetic_dataset_id: StrUUID) -> SyntheticDataset:
        """
        Retrieve synthetic dataset

        :param synthetic_dataset_id: The unique identifier of a synthetic dataset
        :return: The retrieved synthetic dataset
        """
        response = self.request(
            verb=GET, path=[synthetic_dataset_id], response_type=SyntheticDataset
        )
        return response

    def create(
        self, start: bool = True, wait: bool = True, **kwargs: dict[str, Any]
    ) -> SyntheticDataset:
        """
        Create synthetic dataset

        See SyntheticDataset.to_dict for the structure of the parameters.

        :param start: If true, then generation is started right away.
        :param wait: If true, then the function only returns once generation has finished.
        :param **kwargs: The configuration parameters of the synthetic dataset to be created.
        :return: The created synthetic dataset.
        """
        # convert `sample_seed_data` to base64-encoded Parquet files
        if "tables" in kwargs:
            for table in kwargs["tables"]:
                if "sampleSeedData" in table:
                    if isinstance(table["sampleSeedData"], pd.DataFrame):
                        table["sampleSeedData"] = _convert_df_to_base64(
                            table["sampleSeedData"]
                        )
                    elif isinstance(table["sampleSeedData"], str):
                        if table["sampleSeedData"].lower().endswith(".csv"):
                            df = pd.read_csv(table["sampleSeedData"])
                        elif table["sampleSeedData"].lower().endswith(
                            ".parquet"
                        ) or table["sampleSeedData"].lower().endswith(".pqt"):
                            df = pd.read_parquet(table["sampleSeedData"])
                        else:
                            raise ValueError("data must be a DataFrame or a file path")
                        table["sampleSeedData"] = _convert_df_to_base64(df)
                        del df
                    else:
                        raise ValueError("data must be a DataFrame or a file path")
        # convert generator_id to str
        kwargs["generatorId"] = str(kwargs["generatorId"])
        synthetic_dataset = self.request(
            verb=POST,
            path=[],
            json=dict(kwargs),
            response_type=SyntheticDataset,
        )
        if start:
            synthetic_dataset.generation.start()
        if start and wait:
            synthetic_dataset = synthetic_dataset.generation.wait()
        return synthetic_dataset

    def _update(
        self, synthetic_dataset_id: StrUUID, **kwargs: dict[str, Any]
    ) -> SyntheticDataset:
        response = self.request(
            verb=PATCH,
            path=[synthetic_dataset_id],
            json=dict(kwargs),
            response_type=SyntheticDataset,
        )
        return response

    def _delete(self, synthetic_dataset_id: StrUUID) -> None:
        response = self.request(verb=DELETE, path=[synthetic_dataset_id])
        return response

    def _to_dict(self, synthetic_dataset_id: StrUUID) -> SyntheticDataset:
        response = self.request(verb=GET, path=[synthetic_dataset_id, "config"])
        return response

    def _data(self, synthetic_dataset_id: StrUUID) -> dict[str, pd.DataFrame]:
        pqt_zip = self.request(
            verb=GET,
            path=[synthetic_dataset_id, "download"],
            params={"format": SyntheticDatasetFormat.parquet.value},
            headers={
                "Content-Type": "application/zip",
                "Accept": "application/json, text/plain, */*",
            },
            raw_response=True,
        )
        # read each parquet file into a pandas dataframe
        with zipfile.ZipFile(io.BytesIO(pqt_zip), "r") as z:
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
        return dfs

    def _generation_start(self, synthetic_dataset_id: StrUUID) -> None:
        response = self.request(
            verb=POST, path=[synthetic_dataset_id, "generation", "start"]
        )
        return response

    def _generation_cancel(self, synthetic_dataset_id: StrUUID) -> None:
        response = self.request(
            verb=POST, path=[synthetic_dataset_id, "generation", "cancel"]
        )
        return response

    def _generation_progress(self, synthetic_dataset_id: StrUUID) -> JobProgress:
        response = self.request(
            verb=GET,
            path=[synthetic_dataset_id, "generation"],
            response_type=JobProgress,
        )
        return response

    def _generation_wait(
        self, synthetic_dataset_id: StrUUID, interval: float
    ) -> SyntheticDataset:
        _job_wait(lambda: self._generation_progress(synthetic_dataset_id), interval)
        synthetic_dataset = self.get(synthetic_dataset_id)
        return synthetic_dataset
