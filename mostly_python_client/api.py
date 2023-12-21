import os
from typing import Any, List, Literal, Optional, Union

import httpx

GET = "get"
POST = "post"
PATCH = "patch"
DELETE = "delete"
HttpVerb = Literal[GET, POST, PATCH, DELETE]  # type: ignore
VERB_HTTPX_FUNC_MAP = {
    GET: httpx.get,
    POST: httpx.post,
    PATCH: httpx.patch,
    DELETE: httpx.delete,
}

EXAMPLE_BASE_URL = "https://llb2.dev.mostlylab.com"


class MostlyBaseClient:
    ENV_VAR_PREFIX = "MOSTLY"
    SECTION = []

    def env_var(self, name: str):
        return f"{self.ENV_VAR_PREFIX}_{name.upper()}"

    def load_from_env_var(self, name: str) -> Optional[str]:
        return os.getenv(self.env_var(name))

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = (
            base_url or self.load_from_env_var("BASE_URL") or EXAMPLE_BASE_URL
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
        req_func = VERB_HTTPX_FUNC_MAP.get(verb)
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


class MostlyConnectorClient(MostlyBaseClient):
    SECTION = ["api", "v2", "connectors"]

    def list(self, offset: int = 0, limit: int = 50, access_type: str = None) -> dict:
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
        response = self.request(path=[connector_id])
        return response

    def create(self, new_connector: dict):
        response = self.request(verb=POST, path=[], json=new_connector)
        return response

    def update(self, updated_connector: dict):
        connector_id = updated_connector["id"]
        response = self.request(verb=PATCH, path=[connector_id], json=updated_connector)
        return response

    def delete(self, connector_id: str):
        pass

    def locations(self, connector_id: str, prefix: str = ""):
        params = {"prefix": prefix}
        response = self.request(path=[connector_id, "locations"], params=params)
        return response


class MostlyClient(MostlyBaseClient):
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__(base_url=base_url, api_key=api_key)
        client_kwargs = {"base_url": self.base_url, "api_key": self.api_key}
        self.connector = MostlyConnectorClient(**client_kwargs)
