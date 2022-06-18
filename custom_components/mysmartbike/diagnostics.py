"""Diagnostics support for HACS."""
from __future__ import annotations
import json
from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    domain = hass.data[DOMAIN]

    data = {
        "entry": entry.as_dict(),
        "cars" : json.dumps(domain.client.bikes)
    }

    return async_redact_data(data, ("password", "access_token", "refresh_token", "username", "unique_id"))
