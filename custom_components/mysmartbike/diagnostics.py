"""Diagnostics support for MySmartBike."""
from __future__ import annotations

import json
from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, JSON_EXPORT_IGNORED_KEYS
from .coordinator import MySmartBikeDataUpdateCoordinator
from .helper import MBJSONEncoder


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: MySmartBikeDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    diagnostics_data = {
        "config_entry_data": async_redact_data(
            dict(config_entry.options), JSON_EXPORT_IGNORED_KEYS
        ),
        "coordinator_data": json.loads(json.dumps(coordinator.data, cls=MBJSONEncoder)),
    }

    return diagnostics_data
