import tempfile
from pathlib import Path
from typing import Any, Iterator, Union
from uuid import UUID

from mostlyai.base import DELETE, GET, PATCH, POST, Paginator, _MostlyBaseClient
from mostlyai.model import Connector, Generator, SourceTable


class _MostlyGeneratorsClient(_MostlyBaseClient):
    SECTION = ["generators"]

    def list(self, offset: int = 0, limit: int = 50) -> Iterator[Generator]:
        with Paginator(self, Generator, offset=offset, limit=limit) as paginator:
            for item in paginator:
                yield item

    def create(self, **params):
        new_generator = dict(params)
        response = self.request(
            verb=POST, path=[], json=new_generator, response_type=Generator
        )
        return response

    def get(self, generator_id: Union[str, UUID]) -> Connector:
        response = self.request(path=[generator_id], response_type=Generator)
        return response

    def update(
        self, generator_id: Union[str, UUID], **params: dict[str, Any]
    ) -> Connector:
        updated_generator = dict(params)
        response = self.request(
            verb=PATCH,
            path=[generator_id],
            json=updated_generator,
            response_type=Generator,
        )
        return response

    def delete(self, generator_id: Union[str, UUID]) -> None:
        self.request(verb=DELETE, path=[generator_id])

    # SOURCE TABLES

    def add_table(self, generator_id: str, **params):
        new_table = dict(params)
        response = self.request(
            verb=POST,
            path=[generator_id, "tables"],
            json=new_table,
            response_type=SourceTable,
            extra_key_values={"generator_id": generator_id},
        )
        return response

    def add_table_by_upload(self, generator_id: str, file: str, **params):
        # TODO improve the code below
        file_path = file
        file_name = Path(file_path).name
        new_table = dict(params)
        with open(file_path, "rb") as file:
            # construct the multipart form data
            files = {
                "file": (file_name, file),
            }
            response = self.request(
                verb=POST,
                path=[generator_id, "tables", "upload"],
                files=files,
                data=new_table,
                response_type=SourceTable,
                extra_key_values={"generator_id": generator_id},
            )
            return response

    def add_table_from_df_by_upload(self, generator_id: str, **params):
        df = params.pop("df")
        # without a suffix, we'll get 500
        with tempfile.NamedTemporaryFile(mode="w+t", suffix=".csv") as temp_file:
            df.to_csv(temp_file.name)  # CSV to ease debugging
            temp_file_name = temp_file.name
            return self.add_table_by_upload(
                generator_id=generator_id, file=temp_file_name, **params
            )

    def get_table(self, generator_id: str, table_id: Union[str, UUID]):
        response = self.request(
            verb=GET,
            path=[generator_id, "tables", table_id],
            response_type=SourceTable,
            extra_key_values={"generator_id": generator_id},
        )
        return response

    def update_table(self, generator_id: str, table_id: str, **params):
        updated_table = dict(params)
        response = self.request(
            verb=PATCH,
            path=[generator_id, "tables", table_id],
            json=updated_table,
            response_type=SourceTable,
            extra_key_values={"generator_id": generator_id},
        )
        return response

    def delete_table(self, generator_id: str, table_id: Union[str, UUID]):
        response = self.request(
            verb=DELETE,
            path=[generator_id, "tables", table_id],
        )
        return response

    def model_qa_report(
        self, generator_id: Union[str, UUID], table_id: Union[str, UUID]
    ):
        pass

    # SOURCE COLUMNS

    def get_column(
        self, generator_id: Union[str, UUID], table_id: Union[str, UUID], column_id: str
    ):
        response = self.request(
            verb=GET,
            path=[generator_id, "tables", table_id, "columns", column_id],
            response_type=SourceTable,
        )
        return response

    # SOURCE FOREIGN KEYS
    def create_foreign_key(
        self, generator_id: Union[str, UUID], table_id: Union[str, UUID], **params
    ):
        new_fk = dict(params)
        response = self.request(
            verb=POST,
            path=[generator_id, "tables", table_id, "columns", "foreign-keys"],
            json=new_fk,
            response_type=SourceTable,
        )
        return response

    # GENERATOR TRAINING
