from typing import Optional

from mostlyai.base import _MostlyBaseClient
from mostlyai.connectors import _MostlyConnectorsClient
from mostlyai.generators import _MostlyGeneratorsClient
from mostlyai.model import Connector


class MostlyAI(_MostlyBaseClient):
    """
    Client for interacting with the Mostly AI Public API.

    This client serves as the main entry point for accessing various functionalities
    provided. It initializes and holds various specialized clients for
    different sections of the API.

    :param base_url: The base URL. If not provided, a default value is used.
    :param api_key: The API key for authenticating. If not provided, it would rely on env vars.
    """

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__(base_url=base_url, api_key=api_key)
        client_kwargs = {"base_url": self.base_url, "api_key": self.api_key}
        self.connectors = _MostlyConnectorsClient(**client_kwargs)
        self.generators = _MostlyGeneratorsClient(**client_kwargs)


# NOTE: the part below part is very hacky! Just for a quick POC
def connector_locations(self, prefix: str = ""):
    if isinstance(self.client, _MostlyConnectorsClient):
        return self.client.locations(connector_id=self.id, prefix=prefix)


Connector.locations = connector_locations
