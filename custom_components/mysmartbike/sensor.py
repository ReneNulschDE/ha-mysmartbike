"""Sensor support for bikes with MySmartBike app.

For more details about this component, please refer to the documentation at
https://github.com/ReneNulschDE/ha-mysmartbike/
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
import logging
from typing import Any, cast

from homeassistant import util
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfLength
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MySmartBikeDataUpdateCoordinator
from .device import MySmartBikeDevice

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class MySmartBikeSensorDescriptionMixin:
    """Mixin for MySmartBike sensor."""

    value_fn: Callable[[dict[str, Any]], str | int | float | datetime | None]


@dataclass(frozen=True)
class MySmartBikeSensorDescription(SensorEntityDescription, MySmartBikeSensorDescriptionMixin):
    """Class describing MySmartBike sensor entities."""

    exists_fn: Callable[[MySmartBikeDevice], bool] = lambda _: True
    attr_fn: Callable[[Any | None], dict[str, Any]] = lambda _: {}


SENSORS: tuple[MySmartBikeSensorDescription, ...] = (
    MySmartBikeSensorDescription(
        key="odometry",
        native_unit_of_measurement=UnitOfLength.METERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        translation_key="odometry",
        value_fn=lambda data: cast(int, data),
        exists_fn=lambda device: bool(device.odometry),
    ),  # type: ignore[call-arg]
    MySmartBikeSensorDescription(
        key="state_of_charge",
        translation_key="state_of_charge",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: cast(int, data),
        exists_fn=lambda device: bool(device.state_of_charge),
    ),  # type: ignore[call-arg]
)


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
        entities.extend(
            [
                MySmartBikeSensor(result, coordinator, description)
                for description in SENSORS
                if description.exists_fn(result)
            ]
        )
    LOGGER.debug("async_setup_entry: Sensor count for creation - %s", len(entities))
    async_add_entities(entities)


class MySmartBikeSensor(CoordinatorEntity[MySmartBikeDataUpdateCoordinator], SensorEntity):
    """MySmartBike Sensor."""

    _attr_has_entity_name = True
    entity_description: MySmartBikeSensorDescription

    def __init__(
        self,
        device: MySmartBikeDevice,
        coordinator: MySmartBikeDataUpdateCoordinator,
        description: MySmartBikeSensorDescription,
    ) -> None:
        """Initialize the sensor."""

        super().__init__(coordinator)

        self.device = device
        self._attr_unique_id = util.slugify(f"{device.serial} {description.key}")
        self._attr_should_poll = False

        self.entity_description = description

        if coordinator.data:
            self._sensor_data = getattr(coordinator.data.get(device.serial), description.key)

    @property
    def native_value(self) -> str | int | float | datetime | None:
        """Return the state."""
        return self.entity_description.value_fn(self._sensor_data)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""

        return (
            self.entity_description.attr_fn(self.coordinator.data.get(self.device.serial))
            if self.coordinator.data
            else {}
        )

    @property
    def device_info(self) -> DeviceInfo:
        """Device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.device.serial)},
            manufacturer=self.device.manufacturer_name,
            model=self.device.model_name,
            name=(f"{self.device.manufacturer_name} {self.device.model_name}"),
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        if self.coordinator.data:
            self._sensor_data = getattr(
                self.coordinator.data.get(self.device.serial),
                self.entity_description.key,
            )
            self.async_write_ha_state()
