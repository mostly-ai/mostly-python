import tempfile
from pathlib import Path
from typing import Any, Iterator

import pandas as pd

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
)


class _MostlySyntheticDatasetsClient(_MostlyBaseClient):
    SECTION = ["synthetic-datasets"]

    def list(self, offset: int = 0, limit: int = 50) -> Iterator[SyntheticDataset]:
        with Paginator(self, SyntheticDataset, offset=offset, limit=limit) as paginator:
            for item in paginator:
                yield item

    def create(self, **params) -> SyntheticDataset:
        new_synthetic_dataset = dict(params)
        response = self.request(
            verb=POST,
            path=[],
            json=new_synthetic_dataset,
            response_type=SyntheticDataset,
        )
        return response

    def get(self, synthetic_dataset_id: StrUUID) -> SyntheticDataset:
        response = self.request(
            path=[synthetic_dataset_id], response_type=SyntheticDataset
        )
        return response

    def config(self, synthetic_dataset_id: StrUUID) -> SyntheticDataset:
        response = self.request(path=[synthetic_dataset_id, "config"])
        return response

    def download(self, synthetic_dataset_id: StrUUID, fmt: SyntheticDatasetFormat):
        response = self.request(
            path=[synthetic_dataset_id, "download"],
            params={"format": fmt},
            raw_response=True,
        )
        # TODO
        return response
