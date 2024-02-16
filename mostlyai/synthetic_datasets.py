import tempfile
import time
from pathlib import Path
from typing import Any, Iterator

import pandas as pd
from tqdm import tqdm

from mostlyai.base import (
    DELETE,
    GET,
    PATCH,
    POST,
    Paginator,
    StrUUID,
    _MostlyBaseClient,
)
from mostlyai.model import (
    SyntheticDataset,
    SourceColumn,
    SourceForeignKey,
    SourceTable,
    SyntheticDatasetFormat,
    JobProgress,
)


class _MostlySyntheticDatasetsClient(_MostlyBaseClient):
    SECTION = ["synthetic-datasets"]

    def list(self, offset: int = 0, limit: int = 50) -> Iterator[SyntheticDataset]:
        with Paginator(self, SyntheticDataset, offset=offset, limit=limit) as paginator:
            for item in paginator:
                yield item

    def create(
        self, start: bool = True, wait: bool = True, **params
    ) -> SyntheticDataset:
        new_synthetic_dataset = dict(params)
        response = self.request(
            verb=POST,
            path=[],
            json=new_synthetic_dataset,
            response_type=SyntheticDataset,
        )
        if start:
            response.generation.start()
        if wait:
            response.generation.wait()
        return response

    def get(self, synthetic_dataset_id: StrUUID) -> SyntheticDataset:
        response = self.request(
            path=[synthetic_dataset_id], response_type=SyntheticDataset
        )
        return response

    def get_config(self, synthetic_dataset_id: StrUUID) -> SyntheticDataset:
        response = self.request(path=[synthetic_dataset_id, "config"])
        return response

    def download_zip(self, synthetic_dataset_id: StrUUID, fmt: SyntheticDatasetFormat):
        response = self.request(
            path=[synthetic_dataset_id, "download"],
            params={"format": fmt},
            raw_response=True,
        )
        # TODO
        return response

    def download(self, synthetic_dataset_id: StrUUID):
        pqt_zip = self._download(
            synthetic_dataset_id=synthetic_dataset_id,
            fmt=SyntheticDatasetFormat.parquet.value,
        )
        return pd.DataFrame()

    # SD GENERATION

    def start_generation(self, synthetic_dataset_id: StrUUID) -> None:
        response = self.request(
            verb=POST, path=[synthetic_dataset_id, "generation", "start"]
        )
        return response

    def stop_generation(self, synthetic_dataset_id: StrUUID) -> None:
        response = self.request(
            verb=POST, path=[synthetic_dataset_id, "generation", "stop"]
        )
        return response

    def cancel_generation(self, synthetic_dataset_id: StrUUID) -> None:
        response = self.request(
            verb=POST, path=[synthetic_dataset_id, "generation", "cancel"]
        )
        return response

    def get_generation_progress(self, synthetic_dataset_id: StrUUID) -> JobProgress:
        response = self.request(
            path=[synthetic_dataset_id, "generation"], response_type=JobProgress
        )
        return response

    def generation_wait(self, synthetic_dataset_id: StrUUID, interval: float) -> None:
        progress = self.get_generation_progress(synthetic_dataset_id).progress
        current_progress = 0
        with tqdm(total=progress.max) as pbar:
            time.sleep(interval)
            progress = self.get_generation_progress(synthetic_dataset_id).progress
            increment = progress.value - current_progress
            pbar.update(increment)
