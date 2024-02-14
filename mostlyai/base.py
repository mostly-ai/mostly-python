import os
from typing import Annotated, Any, Generic, List, Literal, Optional, TypeVar, Union
from uuid import UUID

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
T = TypeVar("T")
StrUUID = Union[str, UUID]


class _MostlyBaseClient:
    """
    Base client class, which contains all the essentials to be used by sub-classes.
    """

    ENV_VAR_PREFIX = "MOSTLY"
    API_SECTION = ["api", "v2"]
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
        response = self.request(
            is_api_call=False, verb=POST, path=path, headers=headers, data=data
        )

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
        is_api_call: bool = True,
        do_include_client: bool = True,
        extra_key_values: Optional[dict] = None,
        **kwargs,
    ) -> Any:
        """
        This method is rather an extended request helper method, which could be split into two:
        1. Create a request with its params and execute it; Raise an exception in case of an unsuccessful result.
        2. Pack the response into: a specific type (e.g. Pydantic class) with the optional inclusion of:
            - client - so that the returned object can access the API
            - extra_key_values - to store extra information, that is potentially used via that object
        :param path: a single str, or a list of parts of the path to concatenate
        :param verb: get/post/patch/delete
        :param response_type: a specific type to return (e.g. Pydantic class)
        :param is_api_call: True by default; if False, API_SECTION and SECTION won't be prefixed
        :param do_include_client: True by default; if True, client property will be included in the returned instance
        :param extra_key_values: Any extra information storage to include in the returned object
        :param kwargs: httpx's request function's kwargs
        :return: response in a designated type with optional extras
        """
        req_func = _VERB_HTTPX_FUNC_MAP.get(verb)
        if not req_func:
            raise

        path_list = [path] if isinstance(path, str) else [str(p) for p in path]
        prefix = self.API_SECTION + self.SECTION if is_api_call else []
        full_path = [self.base_url] + prefix + path_list
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

        if response.content:
            # this section could be split into a separate method
            response_json = response.json()
            if isinstance(response_json, dict) and not response_type == dict:
                if do_include_client:
                    response_json["client"] = self
                if isinstance(extra_key_values, dict):
                    response_json["extra_key_values"] = extra_key_values
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


class Paginator(Generic[T]):
    def __init__(self, request_context, object_class: T, **kwargs):
        """
        Generic paginator for listing objects with pagination.

        :param request_context: The context in which the request function is called.
        :param object_class: Class of the object to be listed.
        :param kwargs: Additional filter parameters including 'offset' and 'limit'.
        """
        self.request_context = request_context
        self.object_class = object_class
        self.offset = kwargs.pop("offset", 0)
        self.limit = kwargs.pop("limit", 50)
        self.kwargs = kwargs
        self.current_items = []
        self.current_index = 0
        self.is_last_page = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Any cleanup if necessary
        pass

    def __iter__(self):
        return self

    def __next__(self) -> T:
        if self.current_index >= len(self.current_items):
            self._fetch_data()
            self.current_index = 0
            if not self.current_items:
                raise StopIteration

        item = self.current_items[self.current_index]
        self.current_index += 1
        return self.object_class(**item, client=self.request_context, by_alias=True)

    def _fetch_data(self):
        if self.is_last_page:
            self.current_items = []

        params = {"offset": self.offset, "limit": self.limit}
        params.update(self.kwargs)

        response = self.request_context.request([], params=params)

        self.current_items = response.get("results", [])
        total_count = response.get("totalCount", 0)
        self.offset += self.limit

        if self.offset >= total_count:
            self.is_last_page = True


class CustomBaseModel(BaseModel):
    client: Annotated[Optional[Any], Field(exclude=True)] = None
    extra_key_values: Annotated[Optional[dict], Field(exclude=True)] = None
    model_config = ConfigDict(protected_namespaces=())
