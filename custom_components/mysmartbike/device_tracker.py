"""Device tracker for MySmartBike."""
from __future__ import annotations

import logging

from homeassistant import util
from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_LATITUDE, ATTR_LONGITUDE
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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


class MySmartBikeTrackerEntity(
    CoordinatorEntity[MySmartBikeDataUpdateCoordinator], TrackerEntity, RestoreEntity
):
    """Represent a tracked MySmartBike device."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:bicycle"
    _attr_name = "Device Tracker"

    def __init__(
        self,
        device: MySmartBikeDevice,
        coordinator: MySmartBikeDataUpdateCoordinator,
    ) -> None:
        """Initialize the device tracker."""

        super().__init__(coordinator)
        self.device: MySmartBikeDevice = device

        self._attr_unique_id = util.slugify(f"{device.serial}_device_tracker")

        self._latitude: float | None = None
        self._longitude: float | None = None
        self._update_position_from_coordinator()

    async def async_added_to_hass(self) -> None:
        """Restore the last known position if the API has none yet."""
        await super().async_added_to_hass()

        if self._latitude is not None and self._longitude is not None:
            return

        if (last_state := await self.async_get_last_state()) is None:
            return

        latitude = last_state.attributes.get(ATTR_LATITUDE)
        longitude = last_state.attributes.get(ATTR_LONGITUDE)
        if latitude is not None and longitude is not None:
            LOGGER.debug(
                "Restored last known position for %s: %s, %s",
                self.device.serial,
                latitude,
                longitude,
            )
            self._latitude = float(latitude)
            self._longitude = float(longitude)

    def _update_position_from_coordinator(self) -> None:
        """Take over the position from the coordinator if it delivers one."""
        if not self.coordinator.data:
            return
        if (device := self.coordinator.data.get(self.device.serial)) is None:
            return
        if device.latitude is not None and device.longitude is not None:
            self._latitude = device.latitude
            self._longitude = device.longitude

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_position_from_coordinator()
        super()._handle_coordinator_update()

    @property
    def latitude(self) -> float | None:
        """Return the last known latitude of the device."""
        return self._latitude

    @property
    def longitude(self) -> float | None:
        """Return the last known longitude of the device."""
        return self._longitude

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
