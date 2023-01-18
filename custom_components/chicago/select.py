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
    """Set up the Chicago select platform."""
    data = hass.data[DOMAIN][entry.entry_id]

    entities: list[SelectEntity] = [ChicagoSelect(data, hass)]

    if entities:
        async_add_entities(entities, True)


class ChicagoSelect(SelectEntity, RestoreEntity):
    def __init__(self, data: ChicagoData, hass):
        self._hass = hass
        super().__init__()

        self.data = data

        self._attr_name = f"Chicago episode select"
        self._attr_unique_id = f"select_{DOMAIN}_chicago_serie"

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        state = await self.async_get_last_state()
        if state and state.state in self.options:
            self.data.set_option(state.state)

    @property
    def options(self) -> list[str]:
        """Return the available options."""
        return self.data.options_list

    @property
    def current_option(self) -> str:
        """Return current options."""
        return self.data.selected_option

    @property
    def extra_state_attributes(self):
        return {
            "subtitle": self.data.selected_option_obj.season_and_episode,
            "title": self.data.selected_option_obj.name,
            "icon_color": self.data.selected_option_obj.icon_color,
        }

    @property
    def icon(self):
        return self.data.selected_option_obj.icon

    async def async_select_option(self, option: str) -> None:
        """Select new (option)."""
        self.data.set_option(option)
        self.async_write_ha_state()
