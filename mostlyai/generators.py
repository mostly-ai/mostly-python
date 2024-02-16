import time
from typing import Any, Iterator, Optional
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
from mostlyai.utils import _job_wait, _convert_df_to_base64
from mostlyai.model import (
    Generator,
    JobProgress,
)


class _MostlyGeneratorsClient(_MostlyBaseClient):
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

    def create(
        self, start: bool = True, wait: bool = True, **kwargs: dict[str, Any]
    ) -> Generator:
        """
        Create generator

        See Generator.to_dict for the structure of the parameters.

        :param start: If true, then training is started right away.
        :param wait: If true, then the function only returns once training has finished.
        :param **kwargs: The configuration parameters of the generator to be created.
        :return: The created generator.
        """

        # convert `data` field to base64-encoded Parquet files
        if "tables" in kwargs:
            for table in kwargs["tables"]:
                if "data" in table:
                    if isinstance(table["data"], pd.DataFrame):
                        table["data"] = _convert_df_to_base64(table["data"])
                    elif isinstance(table["data"], str):
                        if table["data"].lower().endswith(".csv"):
                            df = pd.read_csv(table["data"])
                        elif table["data"].lower().endswith(".parquet") or table[
                            "data"
                        ].lower().endswith(".pqt"):
                            df = pd.read_parquet(table["data"])
                        else:
                            raise ValueError("data must be a DataFrame or a file path")
                        table["data"] = _convert_df_to_base64(df)
                        del df
                    else:
                        raise ValueError("data must be a DataFrame or a file path")
        generator = self.request(
            verb=POST, path=[], json=dict(kwargs), response_type=Generator
        )
        if start:
            generator.training.start()
            # self._training_start(generator.id)
        if start and wait:
            generator = generator.training.wait()
            # generator = self._training_wait(generator.id)
        return generator

    def _update(self, generator_id: StrUUID, **kwargs: dict[str, Any]) -> Generator:
        response = self.request(
            verb=PATCH,
            path=[generator_id],
            json=dict(kwargs),
            response_type=Generator,
        )
        return response

    def _delete(self, generator_id: StrUUID) -> None:
        response = self.request(verb=DELETE, path=[generator_id])
        return response

    def _to_dict(self, generator_id: StrUUID) -> Generator:
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
