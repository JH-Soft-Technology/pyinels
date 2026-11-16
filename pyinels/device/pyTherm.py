"""Inels heat control class for iNels BUS."""

from pyinels.device.pyBase import pyBase

from pyinels.const import (
    ATTR_HEAT_LEVEL_SELECT,
    ATTR_SWITCH_ON,
    HEAT_LEVELS_DICT
)


class pyTherm(pyBase):
    """Heat control (room thermostat) class based on InelsDevice.

    The set point itself is computed by the central unit from the active
    level, so it is read only. The heating is controlled by selecting
    one of the levels (minimum, attenuation, normal, comfort)."""

    def __init__(self, device):
        """Initialize pyTherm class."""
        super().__init__(device)

    @property
    def current_temperature(self):
        """Measured temperature in the room."""
        return self.__float(self._device.temperature)

    @property
    def target_temperature(self):
        """Set point of the room."""
        return self.__float(self._device.temperature_set)

    @property
    def levels(self):
        """Levels supported by the heat control."""
        if not self._device.level_ids:
            return []
        return list(HEAT_LEVELS_DICT.values())

    @property
    def level(self):
        """Active level of the heat control."""
        for level_id, level in zip(self._device.level_ids,
                                   HEAT_LEVELS_DICT.values()):
            if self.__int(level_id) == ATTR_SWITCH_ON:
                return level
        return None

    @property
    def state(self):
        """Heat control has no on/off state."""
        return None

    def set_level(self, level):
        """Select the level of the heat control."""
        if level not in self.levels:
            raise ValueError(f'Level {level} is not supported')

        letter = [key for key, value in HEAT_LEVELS_DICT.items()
                  if value == level][0]
        select_id = (f'{self._device.heat_control_base}'
                     f'{ATTR_HEAT_LEVEL_SELECT}{letter}')

        self._device.write_value({select_id: f'{ATTR_SWITCH_ON}'},
                                 keep_value=True)

    def __value(self, var_id):
        """Raw value of the variable."""
        value = self._device.value
        if value is None or var_id not in value:
            return None
        return value[var_id]

    def __float(self, var_id):
        """Value of the variable as float."""
        val = self.__value(var_id)
        try:
            return float(val)
        except (TypeError, ValueError):
            return None

    def __int(self, var_id):
        """Value of the variable as int."""
        val = self.__float(var_id)
        return None if val is None else int(val)

    def __repr__(self):
        """Object representation."""
        return "<{} #{} - " \
            "title: {}, " \
            "temperature: {}, " \
            "set point: {}, " \
            "level: {}" \
            ">".format(self._device.type, self._device.id,
                       self._device.title, self.current_temperature,
                       self.target_temperature, self.level)
