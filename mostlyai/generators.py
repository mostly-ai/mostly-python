from typing import Any, Iterator, Union
from uuid import UUID

from mostlyai.base import DELETE, PATCH, POST, Paginator, _MostlyBaseClient
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

    def add_table(self, generator_id: str, **params):
        new_table = dict(params)
        response = self.request(
            verb=POST,
            path=[generator_id, "tables"],
            json=new_table,
            response_type=SourceTable,
        )
        return response
