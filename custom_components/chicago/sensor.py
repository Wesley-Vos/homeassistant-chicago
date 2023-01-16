"""Support for Toon sensors."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_NAME,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Toon sensors based on a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]

    entities = [ChicagoSensor(entry, data)]
    async_add_entities(entities, True)


class ChicagoSensor(SensorEntity):
    """Defines a Toon sensor."""

    
    def __init__(
        self,
        entry: ConfigEntry,
        data: Any
    ) -> None:
        """Initialize the Chicago sensor."""
        super().__init__()
        self.data = data
        print(self.data)

        self._attr_unique_id = (
            f"{DOMAIN}_{entry.data.get(CONF_NAME)}_sensor_current"
        )

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        # return getattr(self.device, self.entity_description.key)
        return "Test"

