"""Config flow to configure the Chicago component."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import (
    CONF_SEASON,
    DOMAIN,
)
from .util import get_seasons

# Validation of the user's configuration
CONFIG_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default="Chicago"): str,
        vol.Required(CONF_SEASON): vol.In(get_seasons()),
    }
)


class ChicagoFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a Chicago config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=CONFIG_SCHEMA)

        return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
        
    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Add reconfigure step to allow to manually reconfigure a config entry."""
        reconfigure_entry = self._get_reconfigure_entry()
        
        if user_input is not None:
            return self.async_update_reload_and_abort(
                    reconfigure_entry,
                data_updates=user_input
                )
  
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=CONFIG_SCHEMA
        )
