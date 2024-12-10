"""Exceptions for the MySmartBike integration."""
from __future__ import annotations

from homeassistant.exceptions import ConfigEntryAuthFailed, IntegrationError, ConfigEntryNotReady


class MySmartBikeException(IntegrationError):
    """Base class for MySmartBike related errors."""


class MySmartBikeAuthException(ConfigEntryAuthFailed):
    """Auth related errors."""


class MySmartBikeAPIException(MySmartBikeException):
    """Api related errors."""

class MySmartBikeAPINotAvailable(ConfigEntryNotReady):
    """API 504 error"""