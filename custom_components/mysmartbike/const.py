"""Constants for the MySmartBike integration."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform

MYSMARTBIKE_PLATFORMS = [Platform.SENSOR, Platform.DEVICE_TRACKER]

DOMAIN = "mysmartbike"
LOGGER = logging.getLogger(__package__)
UPDATE_INTERVAL = timedelta(seconds=300)

USE_SIMULATOR = False
API_BASE_URI_SIMULATOR = "http://0.0.0.0:8001"

API_BASE_URI_CLOUD = "https://my-smartbike.com"
API_BASE_URI = API_BASE_URI_CLOUD if not USE_SIMULATOR else API_BASE_URI_SIMULATOR

USE_PROXY = False
VERIFY_SSL = True
SYSTEM_PROXY: str | None = None if not USE_PROXY else "http://192.168.178.68:9090"

API_USER_AGENT_IOS = "ONE/2.4.2 (com.mahle.sbs; build 4; IOS 17.3)"
API_USER_AGENT_ANDROID = "ONE/2.4.2 (com.mahle.sbs; build: 1812; IOS 17.3)"
API_X_APP = "ENDUSER"
API_X_PLATFORM = "IOS"
API_X_THEME = "DARK"
API_X_VERSION = "2.4.2"

JSON_EXPORT_IGNORED_KEYS = (
    "access_token",
    "refresh_token",
    CONF_PASSWORD,
    CONF_USERNAME,
    "unique_id",
)
