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
from mostlyai.model import Generator, JobProgress
from mostlyai.shares import _MostlySharesMixin
from mostlyai.utils import _convert_df_to_base64, _job_wait, _read_table_from_path


class _MostlyGeneratorsClient(_MostlyBaseClient, _MostlySharesMixin):
    SECTION = ["generators"]

    def list(self, offset: int = 0, limit: int = 50) -> Iterator[Generator]:
        """
        List generators.

        Paginate through all generators that the user has access to.

        :param offset: Offset the entities in the response. Optional. Default: 0
        :param limit: Limit the number of entities in the response. Optional. Default: 50
        :return: Iterator over generators.
        """
        with Paginator(self, Generator, offset=offset, limit=limit) as paginator:
            for item in paginator:
                yield item

    def get(self, generator_id: StrUUID) -> Generator:
        """
        Retrieve generator

        :param generator_id: The unique identifier of a generator
        :return: The retrieved generator
        """
        response = self.request(verb=GET, path=[generator_id], response_type=Generator)
        return response

    def create(self, config: dict) -> Generator:
        # convert `data` to base64-encoded Parquet files
        if "tables" in config and config["tables"]:
            for table in config["tables"]:
                if "data" in table:
                    if isinstance(table["data"], (str, Path)):
                        name, df = _read_table_from_path(table["data"])
                        table["data"] = _convert_df_to_base64(df)
                        if "name" not in table:
                            table["name"] = name
                        del df
                    elif isinstance(table["data"], pd.DataFrame):
                        table["data"] = _convert_df_to_base64(table["data"])
                    else:
                        raise ValueError("data must be a DataFrame or a file path")

        generator = self.request(
            verb=POST, path=[], json=config, response_type=Generator
        )
        return generator

    def _update(self, generator_id: StrUUID, config: dict[str, Any]) -> Generator:
        response = self.request(
            verb=PATCH,
            path=[generator_id],
            json=config,
            response_type=Generator,
        )
        return response

    def _delete(self, generator_id: StrUUID) -> None:
        response = self.request(verb=DELETE, path=[generator_id])
        return response

    def _config(self, generator_id: StrUUID) -> Generator:
        response = self.request(verb=GET, path=[generator_id, "config"])
        return response

    def _training_start(self, generator_id: StrUUID) -> None:
        response = self.request(verb=POST, path=[generator_id, "training", "start"])
        return response

    def _training_cancel(self, generator_id: StrUUID) -> None:
        response = self.request(verb=POST, path=[generator_id, "training", "cancel"])
        return response

    def _training_progress(self, generator_id: StrUUID) -> JobProgress:
        response = self.request(
            verb=GET, path=[generator_id, "training"], response_type=JobProgress
        )
        return response

    def _training_wait(self, generator_id: StrUUID, interval: float) -> Generator:
        _job_wait(lambda: self._training_progress(generator_id), interval)
        generator = self.get(generator_id)
        return generator
