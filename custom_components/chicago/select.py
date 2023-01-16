# pyright: ignore
"""Support for Tado selects for each zone."""
import logging


from homeassistant.components.select import SelectEntity

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    DOMAIN,
)
from .util import ChicagoData

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Tado sensor platform."""
    data = hass.data[DOMAIN][entry.entry_id]

    entities: list[SelectEntity] = [ChicagoSelect(data, hass)]

    if entities:
        async_add_entities(entities, True)


class ChicagoSelect(SelectEntity, RestoreEntity):
    """Preset mode selects for swing and fan speed"""

    def __init__(self, data: ChicagoData, hass):
        self._hass = hass
        super().__init__()

        self.data = data

        self._attr_name = f"Chicago select"
        self._attr_unique_id = f"select_{DOMAIN}_chicago"

        # self._current_option = None

        self._options = data.all_options

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        state = await self.async_get_last_state()
        if state and state.state in self._options:
            self.data.selected_option = state.state

    @property
    def options(self) -> list[str]:
        """Return the available options."""
        return self._options

    @property
    def current_option(self) -> str:
        """Return current options."""
        return self.data.selected_option

    async def async_select_option(self, option: str) -> None:
        """Select new (option)."""
        self.data.selected_option = option
        self.async_write_ha_state()
