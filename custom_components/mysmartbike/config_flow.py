"""Config flow for MySmartBike integration."""
from __future__ import annotations

from http import HTTPStatus
import traceback
from typing import Any, Mapping

from aiohttp import ClientConnectionError, ClientResponseError
import voluptuous as vol  # type: ignore

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, LOGGER, VERIFY_SSL
from .exceptions import MySmartBikeAuthException
from .webapi import MySmartBikeWebApi

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): selector.TextSelector(
            selector.TextSelectorConfig(
                type=selector.TextSelectorType.EMAIL, autocomplete="username"
            )
        ),
        vol.Required(CONF_PASSWORD): selector.TextSelector(
            selector.TextSelectorConfig(
                type=selector.TextSelectorType.PASSWORD, autocomplete="current-password"
            ),
        ),
    }
)


class MySmartBikeConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config or options flow for MySmartBike."""

    VERSION = 1

    def __init__(self):
        """Initialize component."""
        self._existing_entry: ConfigEntry
        self.data: Mapping[str, Any]
        self.reauth_mode = False

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Get configuration from the user."""

        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=CONFIG_SCHEMA)

        errors = {}

        username = user_input[CONF_USERNAME]
        password = user_input[CONF_PASSWORD]

        await self.async_set_unique_id(username)
        if not self.reauth_mode:
            self._abort_if_unique_id_configured()

        webapi: MySmartBikeWebApi = MySmartBikeWebApi(
            self.hass, async_get_clientsession(self.hass, VERIFY_SSL), username, password, {}
        )
        try:
            login_result, token = await webapi.login()
            if not login_result:
                LOGGER.info("")
                errors["base"] = "invalid_auth"
                return self.async_show_form(
                    step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
                )
            else:
                if self.reauth_mode:
                    LOGGER.debug("async_step_user - Reauth save step")
                    self.hass.config_entries.async_update_entry(self._existing_entry, data={"token": token}, options={CONF_USERNAME: username, CONF_PASSWORD: password})
                    self.hass.async_create_task(self.hass.config_entries.async_reload(self._existing_entry.entry_id))
                    return self.async_abort(reason="reauth_successful")
                else:
                    LOGGER.debug("async_step_user - Auth save step")
                    return self.async_create_entry(
                        title=username,
                        data={"token": token},
                        options={CONF_USERNAME: username, CONF_PASSWORD: password},
                    )
        except ClientConnectionError:
            LOGGER.debug("async_step_user - show form after exception - %s", traceback.format_exc())
            errors["base"] = "invalid_auth"
        except ClientResponseError as error:
            if error.status == HTTPStatus.UNAUTHORIZED:
                errors["base"] = "invalid_auth"
            else:
                LOGGER.debug("async_step_user - show form after exception - %s", traceback.format_exc())
                errors["base"] = "unknown"
        except MySmartBikeAuthException:
            errors["base"] = "invalid_auth"
        except Exception as err:
            LOGGER.debug("async_step_user - show form after exception - %s", traceback.format_exc())
            errors["base"] = "unknown"

        return self.async_show_form(step_id="user", data_schema=CONFIG_SCHEMA, errors=errors)

    async def async_step_reauth(self, user_input: ConfigEntry):
        """Get new tokens for a config entry that can't authenticate."""

        self.reauth_mode = True
        self._existing_entry = self.hass.config_entries.async_get_entry(self.context["entry_id"]) # type: ignore

        return self.async_show_form(step_id="user", data_schema=CONFIG_SCHEMA)
