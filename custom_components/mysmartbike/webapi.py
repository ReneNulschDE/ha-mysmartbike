"""The MySmartBike WebAPI."""

from __future__ import annotations

import base64
from datetime import datetime
import json
import logging
import time
import traceback
from typing import Any

from aiohttp import ClientResponseError, ClientSession
from aiohttp.client_exceptions import ClientError

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import API_BASE_URI, API_USER_AGENT, API_X_APP, API_X_THEME, API_X_VERSION, SYSTEM_PROXY, VERIFY_SSL
from .device import MySmartBikeDevice
from .exceptions import MySmartBikeAPINotAvailable, MySmartBikeAuthException

LOGGER = logging.getLogger(__name__)


class MySmartBikeWebApi:
    """Define the WebAPI object."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: ClientSession,
        username: str,
        password: str,
        token: dict[str, Any],
    ) -> None:
        """Initialize."""
        self._session: ClientSession = session
        self._username: str = username
        self._password: str = password
        self.initialized: bool = False
        self.token: dict[str, Any] = token
        self.hass: HomeAssistant = hass

    async def login(self) -> tuple[bool, dict[str, Any]]:
        """Get the login token from MySmartBike cloud."""
        LOGGER.debug("login: Start")

        if self.token and not self.is_token_expired(self.token):
            LOGGER.debug("login: Token not expired")
            return True, self.token

        LOGGER.debug("login: Token expired")
        data = f"password={self._password}&contents_id=&email={self._username}"

        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}

        login_response = await self._request("post", "/api/v1/users/login", data=data, headers=headers)

        if login_response and login_response.get("status") and login_response.get("status") == 200:
            LOGGER.debug("login: Success")
            self.token = self._add_custom_values_to_token_info(
                {"access_token": login_response.get("data").get("token")}
            )
            return True, self.token

        if login_response and login_response.get("status"):
            LOGGER.warning("login: auth error -  %s", login_response)
            raise MySmartBikeAuthException(login_response)

        return False, {}

    async def get_device_list(self) -> dict[str, MySmartBikeDevice]:
        """Pull bikes and generate device list."""

        if self.is_token_expired(self.token):
            LOGGER.info(
                "MySmartBike Cloud token expired. Starting refresh",
            )
            if not await self.login():
                raise MySmartBikeAuthException("Login not successful without exception.")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token['access_token']}",
        }

        _response = await self._request("get", "/api/v1/objects/me?limit=5", headers=headers)

        if _response and _response.get("status") and _response.get("status") == 200:
            LOGGER.debug("get_device_list: %s", _response)

            _location_data: list = []

            _location_response = await self._request(
                "get",
                "/api/v1/objects/me?root_objects=true&list_mode=MAP",
                headers=headers,
            )

            if _location_response and _location_response.get("status") and _location_response.get("status") == 200:
                _location_data = _location_response.get("data", [])

            return await self._build_device_list(_response, _location_data)

        LOGGER.debug("get_device_list: other error -  %s")
        return {}

    async def _request(
        self,
        method: str,
        endpoint: str,
        ignore_errors: bool = False,
        **kwargs,
    ) -> Any:
        """Make a request against the API."""

        url = f"{API_BASE_URI}{endpoint}"

        if "headers" not in kwargs:
            kwargs.setdefault("headers", {})

        kwargs.setdefault("proxy", SYSTEM_PROXY)

        kwargs["headers"].update(
            {
                "Accept": "application/json",
                "User-Agent": API_USER_AGENT,
                "Accept-Language": "de-DE",
                "X-Theme": API_X_THEME,
                "X-App": API_X_APP,
                # "X-Platform": API_X_PLATFORM,
                "X-Version": API_X_VERSION,
            }
        )

        if not self._session or self._session.closed:
            self._session = async_get_clientsession(self.hass, VERIFY_SSL)

        try:
            if "url" in kwargs:
                async with self._session.request(method, **kwargs) as resp:
                    # resp.raise_for_status()
                    return await resp.json(content_type=None)
            else:
                async with self._session.request(method, url, **kwargs) as resp:
                    resp.raise_for_status()
                    return await resp.json(content_type=None)

        except ClientResponseError as err:
            LOGGER.debug(traceback.format_exc())
            if not ignore_errors:
                if err.code > 499:
                    raise MySmartBikeAPINotAvailable(traceback.format_exc()) from err
                raise MySmartBikeAuthException from err
            return None
        except ClientError as err:
            LOGGER.debug(traceback.format_exc())
            if not ignore_errors:
                raise MySmartBikeAPINotAvailable(traceback.format_exc()) from err
            return None
        except Exception as err:
            LOGGER.debug(traceback.format_exc())
            raise err

    async def _build_device_list(self, data, location_data) -> dict[str, MySmartBikeDevice]:
        root_objects: dict[str, MySmartBikeDevice] = {}
        for rbike in data["data"]:
            state_of_charge: int | None = None
            remaining_capacity: int | None = None
            longitude: int | None = None
            latitude: int | None = None

            for obj in rbike["object_tree"]:
                if "state_of_charge" in obj:
                    state_of_charge = obj["state_of_charge"]
                if "remaining_capacity" in obj:
                    remaining_capacity = obj["remaining_capacity"]

            brand_alias = rbike["object_model"]["brand"]["alias"]
            model_name = rbike.get("object_model").get("model_name")
            model_year = rbike.get("object_model").get("model_year")
            location_bike_name = f"{brand_alias} {model_name} {model_year}"

            for bike in location_data:
                if bike[3] and bike[3] == location_bike_name:
                    longitude = bike[2]
                    latitude = bike[1]
                    break

            root_object = MySmartBikeDevice(
                rbike["serial"],
                rbike.get("odometry", -1),
                brand_alias,
                model_name,
                longitude,
                latitude,
                datetime.strptime(rbike.get("diagnosed_at"), "%Y-%m-%d %H:%M:%S"),
                state_of_charge,
                remaining_capacity,
            )

            root_objects[root_object.serial] = root_object
        return root_objects

    def is_token_expired(self, token_info) -> bool:
        """Check if the token is expired."""
        if token_info and "expires_at" in token_info:
            now = int(time.time())
            return token_info["expires_at"] - now < 60

        return True

    def _add_custom_values_to_token_info(self, token_info):
        """Store some values that aren't directly provided by a Web API response."""

        if "access_token" in self.token:
            # Split by dot and get middle, payload, part;
            token_payload = self.token["access_token"].split(".")[1]
            # To make sure decoding will always work - we're adding max padding ("==")
            # to payload - it will be ignored if not needed.
            token_payload_decoded = str(base64.b64decode(token_payload + "=="), "utf-8")
            # Payload is JSON - we can load it to dict for easy access
            payload = json.loads(token_payload_decoded)
            # And now we can access its' elements - e.g. name
            token_info["expires_at"] = payload["exp"]
            return token_info

        return token_info
