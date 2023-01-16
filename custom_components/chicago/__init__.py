"""Support for Toon van Eneco devices."""
from dataclasses import dataclass
from typing import List
import voluptuous as vol
from .util import ChicagoData

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME, Platform
from homeassistant.core import CoreState, HomeAssistant
from homeassistant.helpers import config_validation as cv, device_registry as dr
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

PLATFORMS = [
    Platform.SENSOR,
    Platform.SELECT,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    data = ChicagoData(["test1", "test2", "test3"], "test1")

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = data

    # Spin up the platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Toon config entry."""

    # Unload entities for this entry/device.
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    # Cleanup
    if unload_ok:
        del hass.data[DOMAIN][entry.entry_id]

    return unload_ok
