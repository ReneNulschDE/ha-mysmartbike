"""Exceptions for the MySmartBike integration."""
from __future__ import annotations

from homeassistant.exceptions import IntegrationError


class MySmartBikeException(IntegrationError):
    """Base class for MySmartBike related errors."""


class MySmartBikeAuthException(MySmartBikeException):
    """Auth related errors."""


class MySmartBikeAPIException(MySmartBikeException):
    """Api related errors."""
