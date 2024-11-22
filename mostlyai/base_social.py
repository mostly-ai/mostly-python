from mostlyai.base import _MostlyBaseClient, GET, POST, DELETE, PUT
from mostlyai.model import ResourceShares, PermissionLevel
import rich


class _MostlyBaseSocialClient(_MostlyBaseClient):
    def _list_shares(self, resource_id: str) -> ResourceShares:
        response = self.request(
            verb=GET, path=[resource_id, "share"], response_type=ResourceShares
        )
        return response

    def _share(
        self, resource_id: str, user_email: str, permission_level: PermissionLevel
    ):
        if not isinstance(permission_level, PermissionLevel):
            permission_level = PermissionLevel(permission_level.upper())
        config = {"user_email": user_email, "permission_level": permission_level}
        self.request(verb=POST, path=[resource_id, "share"], json=config)
        permission = PermissionLevel(permission_level).value
        rich.print(
            f"Granted [bold]{user_email}[/] [grey]{permission}[/] access to resource [bold cyan]{resource_id}[/]"
        )

    def _unshare(self, resource_id: str, user_email: str):
        config = {"user_email": user_email}
        self.request(verb=DELETE, path=[resource_id, "share"], json=config)
        rich.print(
            f"Revoked access of resource [bold cyan]{resource_id}[/] for [bold]{user_email}[/]"
        )

    def _like(self, resource_id: str):
        self.request(verb=POST, path=[resource_id, "like"])
        rich.print(f"Liked resource [bold cyan]{resource_id}[/]")

    def _unlike(self, resource_id: str):
        self.request(verb=DELETE, path=[resource_id, "like"])
        rich.print(f"Remove Like from resource [bold cyan]{resource_id}[/]")
