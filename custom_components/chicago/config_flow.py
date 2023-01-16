"""Config flow to configure the Toon component."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
)

# Validation of the user's configuration
CONFIG_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default="Chicago"): str,
        vol.Required(CONF_HOST): str,
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
