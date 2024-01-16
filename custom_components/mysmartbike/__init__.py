"""The Link2Home integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, LOGGER, MYSMARTBIKE_PLATFORMS
from .coordinator import MySmartBikeDataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Set up Link2Home from a config entry."""

    username: str = config_entry.options[CONF_USERNAME]
    password: str = config_entry.options[CONF_PASSWORD]

    websession = async_get_clientsession(hass)

    coordinator = MySmartBikeDataUpdateCoordinator(hass, websession, username, password)
    await coordinator.async_init()

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(config_entry, MYSMARTBIKE_PLATFORMS)

    config_entry.add_update_listener(config_entry_update_listener)

    return True


async def config_entry_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener, called when the config entry options are changed."""
    LOGGER.debug("Start config_entry_update_listener")
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    LOGGER.debug("Start async_unload_entry")

    # coordinator: MySmartBikeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    unload_ok = await hass.config_entries.async_unload_platforms(entry, MYSMARTBIKE_PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
