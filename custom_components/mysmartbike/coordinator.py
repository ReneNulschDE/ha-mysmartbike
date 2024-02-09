"""DataUpdateCoordinator class for the MySmartBike Integration."""
from __future__ import annotations

import asyncio
from copy import deepcopy
import logging
from typing import Any

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, UPDATE_INTERVAL
from .device import MySmartBikeDevice
from .webapi import MySmartBikeWebApi

LOGGER = logging.getLogger(__name__)


class MySmartBikeDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """DataUpdateCoordinator class for the MySmartBike Integration."""

    initialized: bool = False

    def __init__(
        self,
        hass: HomeAssistant,
        session: ClientSession,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""

        username = config_entry.options[CONF_USERNAME]
        password = config_entry.options[CONF_PASSWORD]
        token = config_entry.data["token"] if "token" in config_entry.data else {}

        self.config_entry: ConfigEntry = config_entry
        self.hass: HomeAssistant = hass
        self.webapi: MySmartBikeWebApi = MySmartBikeWebApi(
            hass, session, username, password, token
        )

        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=UPDATE_INTERVAL)

    async def async_init(self) -> bool:
        """Addition init async."""

        async with asyncio.timeout(10):
            login_result, token = await self.webapi.login()
            if login_result:
                self.save_token(token)

            return login_result

    async def _async_update_data(self) -> dict[str, MySmartBikeDevice]:
        """Update data via library."""
        LOGGER.debug("_async_update_data: started")

        try:
            if self.webapi.is_token_expired(self.webapi.token):
                LOGGER.info(
                    "MySmartBike Cloud token expired. Starting refresh",
                )
                if not await self.webapi.login():
                    raise

            devices = await self.webapi.get_device_list()
            LOGGER.info(
                "MySmartBike Cloud delivered %s device(s).",
                len(devices),
            )
            LOGGER.debug(devices)

            return devices

        except (ClientConnectorError,) as error:
            raise UpdateFailed(error) from error

    def save_token(self, token_info):
        """Extend the MySmartBike token with expiry information out of the JWT."""

        LOGGER.debug("Start save_token")

        new_config_entry_data = deepcopy(dict(self.config_entry.data))
        new_config_entry_data["token"] = token_info
        self.hass.config_entries.async_update_entry(self.config_entry, data=new_config_entry_data)
