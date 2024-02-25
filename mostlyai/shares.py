from typing import Union
from uuid import UUID

from mostlyai.base import DELETE, GET, POST, REQUEST, StrUUID, _MostlyBaseClient
from mostlyai.components import (
    CreateShareRequest,
    DeleteShareRequest,
    ShareableResource,
)
from mostlyai.model import PermissionLevel, Share, Connector, Generator, SyntheticDataset
from mostlyai.utils import _as_dict


class _MostlySharesClient(_MostlyBaseClient):
    SECTION = ["shares"]

    @staticmethod
    def _resource_id(resource: Union[str, UUID, Connector, Generator, SyntheticDataset]):
        if isinstance(resource, (str, UUID)):
            resource_id = str(resource)
        elif isinstance(resource, (Connector, Generator, SyntheticDataset)):
            resource_id = str(resource.id)
        else:
            raise ValueError(f"{resource=} is invalid")
        return resource_id

    def _list(self, resource: StrUUID) -> list[Share]:
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
        config = _as_dict(
            CreateShareRequest(user_email=user_email, permission_level=permission_level)
        )
        self.request(verb=POST, path=[resource_id], json=config)

    def _unshare(self, resource: Union[StrUUID, ShareableResource], user_email: str):
        resource_id = self._resource_id(resource)
        config = _as_dict(DeleteShareRequest(user_email=user_email))
        self.request(verb=REQUEST, method="DELETE", path=[resource_id], json=config)


class _MostlySharesMixin:
    @property
    def shares_client(self):
        client_kwargs = {"base_url": self.base_url, "api_key": self.api_key}
        return _MostlySharesClient(**client_kwargs)

    def _shares(self, resource_id: StrUUID) -> list[Share]:
        return self.shares_client._list(resource_id)
