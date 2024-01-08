import tempfile
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

    # TABLES

    def add_table(self, generator_id: str, **params):
        new_table = dict(params)
        response = self.request(
            verb=POST,
            path=[generator_id, "tables"],
            json=new_table,
            response_type=SourceTable,
        )
        return response

    def add_table_by_upload(self, generator_id: str, **params):
        # TODO this is still WIP
        file_content = params.pop("file")
        files = {"file": file_content}
        new_table = dict(params)
        response = self.request(
            verb=POST,
            path=[generator_id, "tables", "upload"],
            files=files,
            json=new_table,
            response_type=SourceTable,
        )
        return response

    def add_table_from_df_by_upload(self, generator_id: str, **params):
        df = params.pop("df")
        with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
            df.to_parquet(temp_file.name)
            temp_file_name = temp_file.name
            with open(temp_file_name, "rb") as file:
                temp_file_content = file.read()
                params["file"] = (temp_file_name, temp_file_content)

        return self.add_table_by_upload(generator_id=generator_id, **params)

    def get_table(self, generator_id: str, table_id: Union[str, UUID]):
        response = self.request(
            verb=GET,
            path=[generator_id, "tables", table_id],
            response_type=SourceTable,
        )
        return response

    def update_table(self, generator_id: str, **params):
        updated_table = dict(params)
        response = self.request(
            verb=PATCH,
            path=[generator_id, "tables"],
            json=updated_table,
            response_type=SourceTable,
        )
        return response

    def delete_table(self, generator_id: str, table_id: Union[str, UUID]):
        response = self.request(
            verb=DELETE,
            path=[generator_id, "tables", table_id],
            response_type=SourceTable,
        )
        return response
