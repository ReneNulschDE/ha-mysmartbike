"""DataUpdateCoordinator class for the MySmartBike Integration."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError

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
        username: str,
        password: str,
    ) -> None:
        """Initialize."""

        self.hass: HomeAssistant = hass
        self.webapi: MySmartBikeWebApi = MySmartBikeWebApi(session, username, password)

        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=UPDATE_INTERVAL)

    async def async_init(self) -> bool:
        """Addition init async."""
        async with asyncio.timeout(10):
            return await self.webapi.login()

    async def _async_update_data(self) -> dict[str, MySmartBikeDevice]:
        """Update data via library."""
        LOGGER.debug("_async_update_data: started")

        try:
            if not self.initialized:
                devices = await self.webapi.get_device_list()
                LOGGER.info(
                    "MySmartBike Cloud delivered %s device(s).",
                    len(devices),
                )
                LOGGER.debug(devices)

                self.initialized = True

            else:
                devices = await self.webapi.get_device_list()
                LOGGER.info(
                    "MySmartBike Cloud delivered %s device(s).",
                    len(devices),
                )
                LOGGER.debug(devices)

            return devices

        except (ClientConnectorError,) as error:
            raise UpdateFailed(error) from error
