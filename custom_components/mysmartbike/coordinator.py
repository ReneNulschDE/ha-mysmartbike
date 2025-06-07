"""DataUpdateCoordinator class for the MySmartBike Integration."""

from __future__ import annotations

import asyncio
from copy import deepcopy
import logging
from typing import Any

from aiohttp import ClientResponseError, ClientSession

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, UPDATE_INTERVAL
from .device import MySmartBikeDevice
from .exceptions import MySmartBikeAPINotAvailable, MySmartBikeAuthException
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
        token = config_entry.data.get("token", {})
        device_type = config_entry.options.get("device_type", "IOS")

        self.config_entry: ConfigEntry = config_entry
        self.hass: HomeAssistant = hass
        self.webapi: MySmartBikeWebApi = MySmartBikeWebApi(hass, session, username, password, token, device_type)

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
            devices = await self.webapi.get_device_list()
            LOGGER.info(
                "MySmartBike Cloud delivered %s device(s).",
                len(devices),
            )
        except (ClientResponseError, MySmartBikeAPINotAvailable) as error:
            raise UpdateFailed(error) from error
        except MySmartBikeAuthException:
            raise

        return devices

    def save_token(self, token_info):
        """Extend the MySmartBike token with expiry information out of the JWT."""

        LOGGER.debug("Start save_token")

        new_config_entry_data = deepcopy(dict(self.config_entry.data))
        new_config_entry_data["token"] = token_info
        self.hass.config_entries.async_update_entry(self.config_entry, data=new_config_entry_data)
