"""Define the objects to store bike data."""
from typing import Any

ODOMETER_OPTIONS = [
    "odo",
]

LOCATION_OPTIONS = [
    "positionLat",
    "positionLong",
    "positionHeading"]


ELECTRIC_OPTIONS = [
    'rangeelectric',
    ]


class Bike(object):
    """ Bike class, stores the bike values at runtime """
    def __init__(self):
        self.finorvin = None

        self.odometer = None
        self.location = None
        self.entry_setup_complete = False
        self._update_listeners = set()


    def add_update_listener(self, listener):
        """Add a listener for update notifications."""
        self._update_listeners.add(listener)

    def remove_update_callback(self, listener):
        """Remove a listener for update notifications."""
        self._update_listeners.discard(listener)

    def publish_updates(self):
        """Schedule call all registered callbacks."""
        for callback in self._update_listeners:
            callback()


class Odometer():
    """ Stores the Odometer values at runtime """
    def __init__(self):
        self.name = "Odometer"


class Electric():
    """ Stores the Electric values at runtime """
    def __init__(self):
        self.name = "Electric"



class Location():
    """ Stores the Location values at runtime """
    def __init__(self, latitude=None, longitude=None, heading=None):
        self.name = "Location"
        self.latitude = None
        self.longitude = None
        self.heading = None
        if latitude is not None:
            self.latitude = latitude
        if longitude is not None:
            self.longitude = longitude
        if heading is not None:
            self.heading = heading


class BikeAttribute():
    """ Stores the BikeAttribute values at runtime """
    def __init__(self, value, retrievalstatus, timestamp, distance_unit=None, display_value=None, unit=None):
        self.value = value
        self.retrievalstatus = retrievalstatus
        self.timestamp = timestamp
        self.distance_unit = distance_unit
        self.display_value = display_value
        self.unit = unit

    def as_dict(self) -> dict[str, Any]:
        """Return dictionary version of this entry."""
        return {
            "value": self.value,
            "retrievalstatus": self.retrievalstatus,
            "timestamp": self.timestamp,
            "distance_unit": self.distance_unit,
            "display_value": self.display_value,
            "unit": self.unit,
        }

