"""Platform for sensor integration."""
from __future__ import annotations
from typing import Any, Dict, Optional

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType


def setup(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    add_entities([LastMovieIdSensor()], update_before_add=False)
    # add_entities([QueryResultSensor()], update_before_add=False)
    


class LastMovieIdSensor(SensorEntity):
    """Representation of a Last Movie Added sensor."""

    def __init__(self, id: int):
        super().__init__()
        # self.attrs: Dict[str, Any] = {ATTR_PATH: self.repo}
        self._name = "last_movie_id"
        self._state = id

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name


    @property
    def state(self) -> int:
        return self._state

    @property
    def device_state_attributes(self) -> Dict[str, Any]:
        return self.attrs
    

# class QueryResultSensor(SensorEntity):
#     """Representation of a Last Movie Added sensor."""

#     def __init__(self, result: Dict[str, Any]):
#         super().__init__()
#         self.attrs: result
#         self._name = "query_result"
#         self._state = 0

#     @property
#     def name(self) -> str:
#         """Return the name of the entity."""
#         return self._name


#     @property
#     def state(self) -> int:
#         return self._state

#     @property
#     def device_state_attributes(self) -> Dict[str, Any]:
#         return self.attrs


