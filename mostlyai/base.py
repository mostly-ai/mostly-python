import os
from typing import Annotated, Any, List, Literal, Optional, Union

import httpx
from pydantic import BaseModel, ConfigDict, Field

from mostlyai.exceptions import APIError, APIStatusError

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
        path: Union[str, List[Any]],
        verb: HttpVerb = "get",
        response_type: type = dict,
        do_include_client: bool = True,
        **kwargs,
    ) -> Any:
        req_func = _VERB_HTTPX_FUNC_MAP.get(verb)
        if not req_func:
            raise

        path_list = [path] if isinstance(path, str) else [str(p) for p in path]
        full_path = [self.base_url] + self.SECTION + path_list
        full_url = "/".join(full_path)

        kwargs["headers"] = kwargs.get("headers") or {}
        kwargs["headers"] |= self.headers()

        try:
            response = req_func(full_url, **kwargs)  # type: ignore
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            # Handle HTTP errors (not in 2XX range)
            raise APIStatusError(
                f"HTTP error occurred: {exc.response.status_code} {exc.response.content}",
            ) from exc
        except httpx.RequestError as exc:
            # Handle request errors (e.g., network issues)
            raise APIError(
                f"An error occurred while requesting {exc.request.url!r}."
            ) from exc

        response_json = response.json()
        if response.content:
            if do_include_client and isinstance(response_json, dict):
                response_json["client"] = self
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


class CustomBaseModel(BaseModel):
    client: Annotated[Optional[Any], Field(exclude=True)] = None
    model_config = ConfigDict(protected_namespaces=())
