# pyright: ignore
"""Support for Tado selects for each zone."""
import logging
from typing import Any


from homeassistant.components.select import SelectEntity

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.const import CONF_NAME
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import (
    AddEntitiesCallback,
    async_get_current_platform,
)
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    CHICAGO_PREVIOUS_EPISODE,
    CHICAGO_NEXT_EPISODE,
    DOMAIN,
)
from .util import ChicagoData

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Chicago select platform."""
    data = hass.data[DOMAIN][entry.entry_id]

    platform = async_get_current_platform()

    platform.async_register_entity_service(
        CHICAGO_PREVIOUS_EPISODE,
        None,
        "previous_episode",
    )

    platform.async_register_entity_service(
        CHICAGO_NEXT_EPISODE,
        None,
        "next_episode",
    )

    entities: list[SelectEntity] = [ChicagoSelect(entry, data, hass)]

    if entities:
        async_add_entities(entities, True)


class ChicagoSelect(SelectEntity, RestoreEntity):
    def __init__(self, entry: ConfigEntry, data: ChicagoData, hass):
        self._hass = hass
        super().__init__()

        self.data = data

        self._attr_name = f"{entry.data.get(CONF_NAME)} episode"
        self._attr_unique_id = f"select_{DOMAIN}_{entry.data.get(CONF_NAME)}"

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        state = await self.async_get_last_state()
        if state and state.state in self.options:
            self.data.set_episode(state.state)

    async def next_episode(self):
        self.data.next_episode()

    async def previous_episode(self):
        self.data.previous_episode()

    @property
    def options(self) -> list[str]:
        """Return the available options."""
        return self.data.episodes_lists

    @property
    def current_option(self) -> str:
        """Return current options."""
        return self.data.selected_episode

    @property
    def extra_state_attributes(self):
        return {
            "subtitle": self.data.selected_episode_obj.season_and_episode,
            "title": self.data.selected_episode_obj.name,
            "icon_color": self.data.selected_episode_obj.icon_color,
            "id": self.data.selected_episode_obj.episode_id,
        }

    @property
    def icon(self):
        return self.data.selected_episode_obj.icon

    async def async_select_option(self, option: str) -> None:
        """Select new episode."""
        self.data.set_episode(option)
        self.async_write_ha_state()
