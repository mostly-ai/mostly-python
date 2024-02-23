from mostlyai.base import DELETE, GET, POST, REQUEST, StrUUID, _MostlyBaseClient
from mostlyai.components import (
    CreateShareRequest,
    DeleteShareRequest,
    ShareableResource,
)
from mostlyai.model import PermissionLevel, Share
from mostlyai.utils import _as_dict


class _MostlySharesClient(_MostlyBaseClient):
    SECTION = ["shares"]

    @staticmethod
    def _resource_id(resource: StrUUID | ShareableResource):
        if isinstance(resource, StrUUID):
            resource_id = str(resource)
        elif isinstance(resource, ShareableResource):
            resource_id = str(resource.id)
        else:
            raise ValueError(f"{resource=} is invalid")
        return resource_id

    def get(self, resource: StrUUID) -> list[Share]:
        resource_id = self._resource_id(resource)
        response = self.request(verb=GET, path=[resource_id])
        response = [Share(**share) for share in response]
        return response

    def _share(
        self,
        resource: StrUUID | ShareableResource,
        user_email: str,
        permission_level: PermissionLevel,
    ) -> Share:
        resource_id = self._resource_id(resource)

        config = _as_dict(
            CreateShareRequest(user_email=user_email, permission_level=permission_level)
        )
        self.request(verb=POST, path=[resource_id], json=config)

    def _unshare(self, resource_id: str, user_email: str):
        resource_id = self._resource_id(resource_id)
        config = _as_dict(DeleteShareRequest(user_email=user_email))
        self.request(verb=REQUEST, method="DELETE", path=[resource_id], json=config)
