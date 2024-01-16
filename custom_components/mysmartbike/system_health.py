"""Provide info to system health."""
from __future__ import annotations

from homeassistant.components import system_health  # type: ignore[attr-defined]
from homeassistant.core import HomeAssistant, callback

from .const import API_BASE_URI


@callback
def async_register(hass: HomeAssistant, register: system_health.SystemHealthRegistration) -> None:
    """Register system health callbacks."""
    register.async_register_info(system_health_info)


async def system_health_info(hass):
    """Get info for the info page."""

    return {
        "api_endpoint_reachable": system_health.async_check_can_reach_url(hass, API_BASE_URI),
    }
