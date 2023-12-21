import os
from typing import Any, List, Literal, Optional, Union

import httpx

GET = "get"
POST = "post"
PATCH = "patch"
DELETE = "delete"
HttpVerb = Literal[GET, POST, PATCH, DELETE]  # type: ignore
_VERB_HTTPX_FUNC_MAP = {
    GET: httpx.get,
    POST: httpx.post,
    PATCH: httpx.patch,
    DELETE: httpx.delete,
}

_EXAMPLE_BASE_URL = "https://llb2.dev.mostlylab.com"


class _MostlyBaseClient:
    ENV_VAR_PREFIX = "MOSTLY"
    SECTION = []

    def env_var(self, name: str):
        return f"{self.ENV_VAR_PREFIX}_{name.upper()}"

    def load_from_env_var(self, name: str) -> Optional[str]:
        return os.getenv(self.env_var(name))

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = (
            base_url or self.load_from_env_var("BASE_URL") or _EXAMPLE_BASE_URL
        )
        self.api_key = (
            api_key or self.load_from_env_var("API_KEY") or self._temp_get_token()
        )

    def _temp_get_token(self) -> str:
        path = "auth/realms/mostly-generate/protocol/openid-connect/token"
        data = {
            "username": "superadmin@mostly.ai",
            "password": self.load_from_env_var("PASSWORD"),
            "client_id": "mostly-app-frontend",
            "grant_type": "password",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self.request(verb=POST, path=path, headers=headers, data=data)

        return response["access_token"]

    def headers(self):
        # this hack will be eliminated once temp_get_token is removed
        if hasattr(self, "api_key"):
            return {
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }
        else:
            return {}

    def request(
        self,
        path: Union[str, List[str]],
        verb: HttpVerb = "get",
        response_type: type = dict,
        **kwargs,
    ) -> Any:
        req_func = _VERB_HTTPX_FUNC_MAP.get(verb)
        if not req_func:
            raise

        path_list = [path] if isinstance(path, str) else path
        full_path = [self.base_url] + self.SECTION + path_list
        full_url = "/".join(full_path)

        kwargs["headers"] = kwargs.get("headers") or {}
        kwargs["headers"] |= self.headers()

        response = req_func(full_url, **kwargs)  # type: ignore
        response.raise_for_status()

        response_json = response.json()
        if response.content:
            return (
                response_type(**response_json)
                if isinstance(response_json, dict)
                else response_json
            )
        else:
            return None

    def post_json(self, **kwargs):
        headers = {"Content-Type": "application/json"}
        return self.request(verb=POST, headers=headers, **kwargs)


class _MostlyConnectorClient(_MostlyBaseClient):
    SECTION = ["api", "v2", "connectors"]

    def list(self, offset: int = 0, limit: int = 50, access_type: str = None) -> dict:
        """
        List connectors with pagination and optional access type filtering.

        :param offset: The starting point for listing connectors.
        :param limit: The maximum number of connectors to return per request.
        :param access_type: Filter connectors by access type, defaults to None.
        :return: Yields individual connectors.

        The method uses a while loop to handle pagination and continues to request
        and yield connectors until all available connectors have been listed.
        """
        while True:
            params = {"offset": offset, "limit": limit}
            if access_type:
                params["accessType"] = access_type

            response = self.request(path=[], params=params)

            # Safely handling the case when 'results' or 'totalCount' is not in response
            results = response.get("results", [])
            total_count = response.get("totalCount", 0)

            for connector in results:
                yield connector

            offset += limit

            # Correcting the condition to break the loop
            if offset >= total_count:
                break

    def get(self, connector_id: str) -> dict:
        """
        Retrieve a specific connector by its ID.

        :param connector_id: The unique identifier of the connector.
        :return: The retrieved connector.
        """
        response = self.request(path=[connector_id])
        return response

    def create(self, new_connector: dict) -> dict:
        """
        Create a new connector.

        :param new_connector: The connector data to be created.
        :return: The created connector.
        """
        response = self.request(verb=POST, path=[], json=new_connector)
        return response

    def update(self, updated_connector: dict) -> dict:
        """
        Update an existing connector.

        :param updated_connector: The updated connector data, must include its ID.
        :return: The updated connector.
        """
        connector_id = updated_connector["id"]
        response = self.request(verb=PATCH, path=[connector_id], json=updated_connector)
        return response

    def delete(self, connector_id: str) -> dict:
        """
        Delete a connector by its ID.

        :param connector_id: The unique identifier of the connector to be deleted.
        :return: Empty, if successfully deleted the connector.
        """
        response = self.request(verb=DELETE, path=[connector_id])
        return response

    def locations(self, connector_id: str, prefix: str = "") -> list:
        """
        Retrieve the locations associated with a specific connector and prefix.

        :param connector_id: The unique identifier of the connector.
        :param prefix: A prefix to filter the locations, defaults to "".
        :return: A list of locations (schemas, databases, directories, etc.) on the given level.
        """
        params = {"prefix": prefix}
        response = self.request(path=[connector_id, "locations"], params=params)
        return response


class MostlyClient(_MostlyBaseClient):
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
        self.connector = _MostlyConnectorClient(**client_kwargs)
