"""Device Support for the MySmartBike integration."""

from __future__ import annotations

from datetime import datetime

from attr import dataclass


@dataclass
class MySmartBikeDevice:
    """Device class for the MySmartBike integration."""

    serial: str
    odometry: int
    manufacturer_name: str
    model_name: str
    longitude: float | None
    latitude: float | None
    last_position_date: datetime
    state_of_charge: int | None
    remaining_capacity: int | None
