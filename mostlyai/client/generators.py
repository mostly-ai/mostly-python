from pathlib import Path
from typing import Any, Iterator, Optional, Union
import re

import pandas as pd

from mostlyai.client.base import DELETE, GET, PATCH, POST, Paginator, _MostlyBaseClient
from mostlyai.client.model import (
    Generator,
    JobProgress,
    GeneratorListItem,
    GeneratorConfig,
    GeneratorPatchConfig,
)
from mostlyai.client._base_utils import (
    convert_to_base64,
)
from mostlyai.client._mostly_utils import job_wait, read_table_from_path


class _MostlyGeneratorsClient(_MostlyBaseClient):
    SECTION = ["generators"]

    # PUBLIC METHODS #

    def list(
        self,
        offset: int = 0,
        limit: int = 50,
        status: Optional[Union[str, list[str]]] = None,
        search_term: Optional[str] = None,
    ) -> Iterator[GeneratorListItem]:
        """
        List generators.

        Paginate through all generators accessible by the user.

        Args:
            offset: Offset for the entities in the response.
            limit: Limit for the number of entities in the response.
            status: Filter by training status.
            search_term: Filter by name or description.

        Returns:
            Iterator[GeneratorListItem]: An iterator over generator list items.
        """
        status = ",".join(status) if isinstance(status, list) else status
        with Paginator(
            self,
            GeneratorListItem,
            offset=offset,
            limit=limit,
            status=status,
            search_term=search_term,
        ) as paginator:
            for item in paginator:
                yield item

    def get(self, generator_id: str) -> Generator:
        """
        Retrieve a generator by its ID.

        Args:
            generator_id: The unique identifier of the generator.

        Returns:
            Generator: The retrieved generator object.
        """
        response = self.request(verb=GET, path=[generator_id], response_type=Generator)
        return response

    def create(self, config: Union[GeneratorConfig, dict]) -> Generator:
        """
        Create a generator.

        Args:
            config: Configuration for the generator.

        Returns:
            The created generator object.
        """
        if isinstance(config, dict) and config.get("tables"):
            for table in config["tables"]:
                # convert `data` to base64-encoded Parquet files
                if table.get("data") is not None:
                    if isinstance(table["data"], (str, Path)):
                        name, df = read_table_from_path(table["data"])
                        table["data"] = convert_to_base64(df)
                        if "name" not in table:
                            table["name"] = name
                        del df
                    elif isinstance(table["data"], pd.DataFrame):
                        table["data"] = convert_to_base64(table["data"])
                    else:
                        raise ValueError("data must be a DataFrame or a file path")
                if table.get("columns"):
                    # convert `columns` to list[dict], if provided as list[str]
                    table["columns"] = [
                        {"name": col} if isinstance(col, str) else col
                        for col in table["columns"]
                    ]
        generator = self.request(
            verb=POST, path=[], json=config, response_type=Generator
        )
        return generator

    def import_from_file(
        self,
        file_path: Union[str, Path],
    ) -> Generator:
        """
        Import a generator from a file.
        Supported from release v212 onwards.

        Args:
            file_path: Path to the file to import.

        Returns:
            The imported generator object.
        """
        response = self.request(
            verb=POST,
            path=["import-from-file"],
            headers={
                "Accept": "application/json, text/plain, */*",
            },
            files={"file": open(file_path, "rb")},
            response_type=Generator,
        )
        return response

    # PRIVATE METHODS #
    def _export_to_file(
        self,
        generator_id: str,
    ) -> (bytes, Optional[str]):
        response = self.request(
            verb=GET,
            path=[generator_id, "export-to-file"],
            headers={
                "Content-Type": "application/octet-stream",
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
            filename = f"generator-{generator_id[:8]}.mostly"
        return content_bytes, filename

    def _update(
        self, generator_id: str, config: Union[GeneratorPatchConfig, dict[str, Any]]
    ) -> Generator:
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

    def _clone(self, generator_id: str, training_status: str) -> Generator:
        response = self.request(
            verb=POST,
            path=[generator_id, "clone"],
            json={"trainingStatus": training_status},
            response_type=Generator,
        )
        return response

    def _config(self, generator_id: str) -> GeneratorConfig:
        response = self.request(
            verb=GET, path=[generator_id, "config"], response_type=GeneratorConfig
        )
        return response

    def _training_start(self, generator_id: str) -> None:
        self.request(verb=POST, path=[generator_id, "training", "start"])

    def _training_cancel(self, generator_id: str) -> None:
        self.request(verb=POST, path=[generator_id, "training", "cancel"])

    def _training_progress(self, generator_id: str) -> JobProgress:
        response = self.request(
            verb=GET, path=[generator_id, "training"], response_type=JobProgress
        )
        return response

    def _training_wait(
        self, generator_id: str, progress_bar: bool, interval: float
    ) -> Generator:
        job_wait(lambda: self._training_progress(generator_id), interval, progress_bar)
        generator = self.get(generator_id)
        return generator
