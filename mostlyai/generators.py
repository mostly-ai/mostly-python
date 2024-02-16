import base64
import io
import tempfile
import time
import uuid
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
    Generator,
    SourceColumn,
    SourceForeignKey,
    SourceTable,
    JobProgress,
    ModelEncodingType,
    Model,
    ModelConfiguration,
)


class _MostlyGeneratorsClient(_MostlyBaseClient):
    SECTION = ["generators"]

    def list(self, offset: int = 0, limit: int = 50) -> Iterator[Generator]:
        with Paginator(self, Generator, offset=offset, limit=limit) as paginator:
            for item in paginator:
                yield item

    def _tables_from_df(self, tables: dict[str, pd.DataFrame]):
        source_tables = []
        for table_name, table_df in tables.items():
            columns = [
                dict(
                    name=c,
                    included=True,
                    modelEncodingType=ModelEncodingType.categorical.value,
                )
                for c in table_df.columns
            ]

            # Save the DataFrame to a buffer in Parquet format
            buffer = io.BytesIO()
            table_df.to_parquet(buffer, index=False)

            # Read the binary data from the buffer
            buffer.seek(0)
            binary_data = buffer.read()

            # Convert the binary data to a base64 string
            base64_encoded_str = base64.b64encode(binary_data).decode()

            source_table = dict(
                name=table_name,
                data=base64_encoded_str,
                columns=columns,
            )
            source_tables.append(source_table)

        return source_tables

    def create(self, start: bool = True, wait: bool = True, **params) -> Generator:
        if "tables" in params and isinstance(params["tables"], dict):
            params["tables"] = self._tables_from_df(params["tables"])
        new_generator = dict(params)
        response = self.request(
            verb=POST, path=[], json=new_generator, response_type=Generator
        )
        if start:
            response.training.start()
        if wait:
            response.training.wait()
        return response

    def get(self, generator_id: StrUUID) -> Generator:
        response = self.request(path=[generator_id], response_type=Generator)
        return response

    def config(self, generator_id: StrUUID) -> Generator:
        response = self.request(path=[generator_id, "config"])
        return response

    def update(self, generator_id: StrUUID, **params: dict[str, Any]) -> Generator:
        updated_generator = dict(params)
        response = self.request(
            verb=PATCH,
            path=[generator_id],
            json=updated_generator,
            response_type=Generator,
        )
        return response

    def delete(self, generator_id: StrUUID) -> None:
        self.request(verb=DELETE, path=[generator_id])

    # GENERATOR TRAINING

    def start_training(self, generator_id: StrUUID) -> None:
        response = self.request(verb=POST, path=[generator_id, "training", "start"])
        return response

    def stop_training(self, generator_id: StrUUID) -> None:
        response = self.request(verb=POST, path=[generator_id, "training", "stop"])
        return response

    def cancel_training(self, generator_id: StrUUID) -> None:
        response = self.request(verb=POST, path=[generator_id, "training", "cancel"])
        return response

    def get_training_progress(self, generator_id: StrUUID) -> JobProgress:
        response = self.request(
            path=[generator_id, "training"], response_type=JobProgress
        )
        return response

    def training_wait(self, generator_id: StrUUID, interval: float) -> None:
        progress = self.get_training_progress(generator_id).progress
        current_progress = 0
        with tqdm(total=progress.max) as pbar:
            time.sleep(interval)
            progress = self.get_training_progress(generator_id).progress
            increment = progress.value - current_progress
            pbar.update(increment)

    #
    #
    #
    # # SOURCE TABLES
    #
    # def add_table(self, generator_id: StrUUID, **params) -> SourceTable:
    #     new_table = dict(params)
    #     response = self.request(
    #         verb=POST,
    #         path=[generator_id, "tables"],
    #         json=new_table,
    #         response_type=SourceTable,
    #         extra_key_values={"generator_id": str(generator_id)},
    #     )
    #     return response
    #
    # def add_table_by_upload(
    #     self, generator_id: StrUUID, file: str, **params
    # ) -> SourceTable:
    #     # TODO improve the code below
    #     file_path = file
    #     file_name = Path(file_path).name
    #     new_table = dict(params)
    #     with open(file_path, "rb") as file:
    #         # construct the multipart form data
    #         files = {
    #             "file": (file_name, file),
    #         }
    #         response = self.request(
    #             verb=POST,
    #             path=[generator_id, "tables", "upload"],
    #             files=files,
    #             data=new_table,
    #             response_type=SourceTable,
    #             extra_key_values={"generator_id": str(generator_id)},
    #         )
    #         return response
    #
    # def add_table_from_df_by_upload(
    #     self, generator_id: StrUUID, df: pd.DataFrame, **params
    # ) -> SourceTable:
    #     # without a suffix, we'll get 500
    #     with tempfile.NamedTemporaryFile(mode="w+t", suffix=".csv") as temp_file:
    #         df.to_csv(temp_file.name)  # CSV to ease debugging
    #         temp_file_name = temp_file.name
    #         return self.add_table_by_upload(
    #             generator_id=generator_id, file=temp_file_name, **params
    #         )
    #
    # def get_table(self, generator_id: str, table_id: StrUUID) -> SourceTable:
    #     response = self.request(
    #         verb=GET,
    #         path=[generator_id, "tables", table_id],
    #         response_type=SourceTable,
    #         extra_key_values={"generator_id": str(generator_id)},
    #     )
    #     return response
    #
    # def update_table(self, generator_id: str, table_id: str, **params) -> SourceTable:
    #     updated_table = dict(params)
    #     response = self.request(
    #         verb=PATCH,
    #         path=[generator_id, "tables", table_id],
    #         json=updated_table,
    #         response_type=SourceTable,
    #         extra_key_values={"generator_id": str(generator_id)},
    #     )
    #     return response
    #
    # def delete_table(self, generator_id: str, table_id: StrUUID) -> None:
    #     self.request(
    #         verb=DELETE,
    #         path=[generator_id, "tables", table_id],
    #     )
    #
    # def model_qa_report(self, generator_id: StrUUID, table_id: StrUUID):
    #     pass
    #
    # # SOURCE COLUMNS
    #
    # def get_column(
    #     self, generator_id: StrUUID, table_id: StrUUID, column_id: str
    # ) -> SourceColumn:
    #     response = self.request(
    #         verb=GET,
    #         path=[generator_id, "tables", table_id, "columns", column_id],
    #         response_type=SourceColumn,
    #     )
    #     return response
    #
    # # SOURCE FOREIGN KEYS
    # def create_foreign_key(
    #     self, generator_id: StrUUID, table_id: StrUUID, **params
    # ) -> SourceForeignKey:
    #     new_fk = dict(params)
    #     response = self.request(
    #         verb=POST,
    #         path=[generator_id, "tables", table_id, "columns", "foreign-keys"],
    #         json=new_fk,
    #         response_type=SourceForeignKey,
    #     )
    #     return response
    #
