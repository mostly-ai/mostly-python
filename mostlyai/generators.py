from pathlib import Path
from typing import Any, Iterator, Optional, Union

import pandas as pd

from mostlyai.base import DELETE, GET, PATCH, POST, Paginator, _MostlyBaseClient
from mostlyai.model import Generator, JobProgress
from mostlyai.shares import _MostlySharesMixin
from mostlyai.utils import _convert_df_to_base64, _job_wait, _read_table_from_path


class _MostlyGeneratorsClient(_MostlyBaseClient, _MostlySharesMixin):
    SECTION = ["generators"]

    # PUBLIC METHODS #

    def list(
        self,
        offset: int = 0,
        limit: int = 50,
        status: Optional[Union[str, list[str]]] = None,
    ) -> Iterator[Generator]:
        """
        List generators.

        Paginate through all generators that the user has access to.

        :param offset: Offset the entities in the response. Optional. Default: 0
        :param limit: Limit the number of entities in the response. Optional. Default: 50
        :param status: Filter by training status. Optional. Default: None
        :return: Iterator over generators.
        """
        status = ",".join(status) if isinstance(status, list) else status
        with Paginator(
            self, Generator, offset=offset, limit=limit, status=status
        ) as paginator:
            for item in paginator:
                yield item

    def get(self, generator_id: str) -> Generator:
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
                if "data" in table and table["data"] is not None:
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

    # PRIVATE METHODS #

    def _update(self, generator_id: str, config: dict[str, Any]) -> Generator:
        response = self.request(
            verb=PATCH,
            path=[generator_id],
            json=config,
            response_type=Generator,
        )
        return response

    def _delete(self, generator_id: str) -> None:
        response = self.request(verb=DELETE, path=[generator_id])
        return response

    def _config(self, generator_id: str) -> Generator:
        response = self.request(verb=GET, path=[generator_id, "config"])
        return response

    def _training_start(self, generator_id: str) -> None:
        response = self.request(verb=POST, path=[generator_id, "training", "start"])
        return response

    def _training_cancel(self, generator_id: str) -> None:
        response = self.request(verb=POST, path=[generator_id, "training", "cancel"])
        return response

    def _training_progress(self, generator_id: str) -> JobProgress:
        response = self.request(
            verb=GET, path=[generator_id, "training"], response_type=JobProgress
        )
        return response

    def _training_wait(self, generator_id: str, interval: float) -> Generator:
        _job_wait(lambda: self._training_progress(generator_id), interval)
        generator = self.get(generator_id)
        return generator
