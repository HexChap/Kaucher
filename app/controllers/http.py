import json
import sys
from urllib.parse import quote
from typing import Any

import requests

from app.core import settings, errors
from app.schemas import user_schemas, misc_schemas
from app.schemas import launch_data_schemas as ld_schemas

# BASE_PATH: str = settings.API_BASE_PATH
# API_VER: str = settings.API_VER


class Route:
    def __init__(self, method: str, endpoint: str, **parameters: Any):
        self.endpoint = endpoint
        self.method = method

        url = settings.API_BASE_PATH + f"/{settings.API_VER}" + self.endpoint
        if parameters:
            url = url.format_map({k: quote(v) if isinstance(v, str) else v for k, v in parameters.items()})

        self.url = url


class HTTPClient:
    def __init__(self):
        self.token: str | None = None
        self.__session = requests.Session()

        user_agent = "KaucherClient/{0} Python/{1} requests/{2}"
        self.user_agent = user_agent.format(settings.CLIENT_VERSION, sys.winver, requests.__version__)

        self.api_info = self.get_api_info()

    def request(
            self,
            route: Route,
            **kwargs: Any
    ) -> requests.Response:
        data: dict[str, str] = {}
        headers: dict[str, str] = {
            "user-agent": self.user_agent
        }
        if self.token is not None:
            headers["Authorization"] = "Bearer " + self.token

        if "json" in kwargs:
            headers["content-type"] = "application/json"
            data = json.loads(kwargs.pop("json"))

        resp = self.__session.request(
            method=route.method,
            url=route.url,
            headers=headers,
            json=data
        )
        status_code = resp.status_code

        if 300 > status_code >= 200:
            return resp

        elif status_code == 401:
            raise errors.Unauthorized(resp)

        elif status_code == 403:
            raise errors.Forbidden(resp)

        elif status_code == 404:
            raise errors.NotFound(resp)

        elif status_code == 422:
            raise errors.UnprocessableEntity(resp)

        elif status_code >= 500:
            raise errors.ServerError(resp)

        else:
            raise errors.HTTPException(resp)

    def close(self):
        #  TODO: Test this one
        self.__session.close()

    def get_api_info(self) -> misc_schemas.APIInfo:
        info = self.request(
            Route("GET", "/api-info/")
        ).json()

        return misc_schemas.APIInfo(**info)

    def login(self, payload: user_schemas.UserCredentials):
        resp = self.request(
            Route("POST", "/auth/"),
            json=payload.json()
        ).json()
        token_resp = user_schemas.TokenResponse(**resp)
        self.token = token_resp.access_token

        return token_resp

    def logout(self):
        self.token = None

        return self.request(
            Route("GET", "/logout/"),
        )

    def register_user(self, payload: user_schemas.UserPayload):
        return self.request(
            Route("POST", "/users/"),
            json=payload.json()
        )

    def get_users(self):
        return self.request(
            Route("GET", "/users/")
        )

    def add_launch_data(self, payload: ld_schemas.LaunchDataPayload):
        return self.request(
            Route("POST", "/launch-data/"),
            json=payload.json()
        )

    def get_launch_data(self, ld_id: int):
        return self.request(
            Route("GET", "/launch-data/{ld_id}/", ld_id=ld_id)
        )
