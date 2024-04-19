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
    RESOURCE_TYPE = {
        Connector: "connectors",
        Generator: "generators",
        SyntheticDataset: "synthetic-datasets",
    }

    # PRIVATE METHODS #

    def _list(self, resource: ShareableResource) -> list[Share]:
        resource_type = self.RESOURCE_TYPE.get(type(resource))
        response = self.request(verb=GET, path=[resource_type, resource.id])
        response = [Share(**share) for share in response]
        return response

    def _share(
        self,
        resource: ShareableResource,
        user_email: str,
        permission_level: PermissionLevel,
    ):
        config = {"userEmail": user_email, "permissionLevel": permission_level}
        resource_type = self.RESOURCE_TYPE.get(type(resource))
        self.request(verb=POST, path=[resource_type, resource.id], json=config)

    def _unshare(self, resource: ShareableResource, user_email: str):
        config = {"userEmail": user_email}
        resource_type = self.RESOURCE_TYPE.get(type(resource))
        self.request(verb=DELETE, path=[resource_type, resource.id], json=config)


class _MostlySharesMixin:
    @property
    def shares_client(self):
        client_kwargs = {"base_url": self.base_url, "api_key": self.api_key}
        return _MostlySharesClient(**client_kwargs)

    def _shares(self, resource: ShareableResource) -> list[Share]:
        return self.shares_client._list(resource)
