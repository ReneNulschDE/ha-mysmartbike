"""The MySmartBike integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, LOGGER, MYSMARTBIKE_PLATFORMS, VERIFY_SSL
from .coordinator import MySmartBikeDataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Set up MySmartBike from a config entry."""

    websession = async_get_clientsession(hass, VERIFY_SSL)

    coordinator = MySmartBikeDataUpdateCoordinator(hass, websession, config_entry)
    await coordinator.async_init()
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(config_entry, MYSMARTBIKE_PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    LOGGER.debug("Start async_unload_entry")

    unload_ok = await hass.config_entries.async_unload_platforms(entry, MYSMARTBIKE_PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
