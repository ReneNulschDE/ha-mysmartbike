"""Device tracker for MySmartBike."""
from __future__ import annotations

import logging

from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DOMAIN
from .coordinator import MySmartBikeDataUpdateCoordinator
from .device import MySmartBikeDevice

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the sensor platform."""
    coordinator: MySmartBikeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    data: list[MySmartBikeDevice] = list(coordinator.data.values())

    for result in data:
        entities.append(MySmartBikeTrackerEntity(result, coordinator))

    LOGGER.debug("async_setup_entry: DeviceTracker count for creation - %s", len(entities))
    async_add_entities(entities)


class MySmartBikeTrackerEntity(TrackerEntity, RestoreEntity):
    """Represent a tracked MySmartBike device."""

    def __init__(
        self,
        device: MySmartBikeDevice,
        coordinator: MySmartBikeDataUpdateCoordinator,
    ) -> None:
        """Initialize the sensor."""

        self.coordinator: MySmartBikeDataUpdateCoordinator = coordinator
        self.device: MySmartBikeDevice = device

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        return (
            self.coordinator.data[self.device.serial].latitude if self.coordinator.data else None
        )

    @property
    def should_poll(self) -> bool:
        """No polling for entities that have location pushed."""
        return True

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        return (
            self.coordinator.data[self.device.serial].longitude if self.coordinator.data else None
        )

    @property
    def icon(self) -> str:
        """Return the icon of the device."""
        return "mdi:bike"

    @property
    def source_type(self) -> SourceType:
        """Return the source type of the device."""
        return SourceType.GPS

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.device.serial)},
            manufacturer=self.device.manufacturer_name,
            model=self.device.model_name,
            name=(f"{self.device.manufacturer_name} {self.device.model_name}"),
        )

    @property
    def battery_level(self) -> int | None:
        """Return the battery level of the device. Percentage from 0-100."""

        return (
            self.coordinator.data[self.device.serial].state_of_charge
            if self.coordinator.data
            else None
        )
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        self.async_write_ha_state()
