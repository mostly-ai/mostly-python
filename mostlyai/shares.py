from typing import Union
from uuid import UUID

from mostlyai.base import DELETE, GET, POST, _MostlyBaseClient
from mostlyai.model import (
    Connector,
    Generator,
    PermissionLevel,
    Share,
    SyntheticDataset,
)
from mostlyai.utils import ShareableResource


class _MostlySharesClient(_MostlyBaseClient):
    SECTION = ["shares"]

    # PRIVATE METHODS #

    @staticmethod
    def _resource_id(
        resource: Union[str, UUID, Connector, Generator, SyntheticDataset],
    ):
        if isinstance(resource, (str, UUID)):
            resource_id = str(resource)
        elif isinstance(resource, (Connector, Generator, SyntheticDataset)):
            resource_id = str(resource.id)
        else:
            raise ValueError(f"{resource=} is invalid")
        return resource_id

    def _list(self, resource: str) -> list[Share]:
        resource_id = self._resource_id(resource)
        response = self.request(verb=GET, path=[resource_id])
        response = [Share(**share) for share in response]
        return response

    def _share(
        self,
        resource_id: str,
        user_email: str,
        permission_level: PermissionLevel,
    ):
        config = {"userEmail": user_email, "permissionLevel": permission_level}
        self.request(verb=POST, path=[resource_id], json=config)

    def _unshare(self, resource: Union[str, ShareableResource], user_email: str):
        resource_id = self._resource_id(resource)
        config = {"userEmail": user_email}
        self.request(verb=DELETE, path=[resource_id], json=config)


class _MostlySharesMixin:
    @property
    def shares_client(self):
        client_kwargs = {"base_url": self.base_url, "api_key": self.api_key}
        return _MostlySharesClient(**client_kwargs)

    def _shares(self, resource_id: str) -> list[Share]:
        return self.shares_client._list(resource_id)
