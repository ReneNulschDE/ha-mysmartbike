"""
Sensor support for bikes with MySmartBike app.

For more details about this component, please refer to the documentation at
https://github.com/ReneNulschDE/ha-mysmartbike/
"""
import logging

from homeassistant.helpers.restore_state import RestoreEntity

from . import MySmartBikeEntity

from .const import (
    DOMAIN,
    SENSORS
)

LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Setup the sensor platform."""

    data = hass.data[DOMAIN]

    if not data.client.bikes:
        LOGGER.info("No Bikes found.")
        return

    sensor_list = []
    for bike in data.client.bikes:

        for key, value in sorted(SENSORS.items()):
            device = MySmartBikeSensor(
                hass=hass,
                data=data,
                internal_name = key,
                sensor_config = value,
                vin = bike.finorvin
                )
            sensor_list.append(device)

    async_add_entities(sensor_list, True)




class MySmartBikeSensor(MySmartBikeEntity, RestoreEntity):
    """Representation of a Sensor."""

    @property
    def state(self):
        """Return the state of the sensor."""

        return self._state


    async def async_added_to_hass(self) -> None:
        """Call when entity about to be added to Home Assistant."""
        await super().async_added_to_hass()
        # __init__ will set self._state to self._initial, only override
        # if needed.
        state = await self.async_get_last_state()
        if state is not None:
            self._state = state.state
