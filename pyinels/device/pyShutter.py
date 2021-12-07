"""Inels shutter class to control blinds."""
from pyinels.device.pyBase import pyBase
# from pyinels.pyTimer import pyTimer

from pyinels.const import (
    ATTR_DOWN,
    ATTR_UP,
    ATTR_STOP,
    ATTR_SWITCH_ON,
    ATTR_SWITCH_OFF,
    DIRECTIONS_DICT,
    RANGE_BLIND,
    STATE_OPEN,
    SUPPORT_OPEN,
    SUPPORT_CLOSE,
    SUPPORT_SET_POSITION,
    SUPPORT_STOP,
    SUPPORT_OPEN_TILT,
    SUPPORT_CLOSE_TILT,
    SUPPORT_STOP_TILT,
    STATE_CLOSING,
    STATE_OPENING,
    STATE_CLOSED
)

MIN_RANGE = RANGE_BLIND[0]
MAX_RANGE = RANGE_BLIND[1]


class pyShutter(pyBase):
    """Inels class shutter."""

    def __init__(self, device):
        """Initialize shutter."""
        super().__init__(device)
        self._current_possition = 0
        self._previous_state = self._device.value

    @property
    def state(self):
        """State where the shutter is."""
        up_device = self.up
        down_device = self.down

        up_on = up_device == ATTR_SWITCH_ON \
            and down_device == ATTR_SWITCH_OFF
        down_on = up_device == ATTR_SWITCH_OFF \
            and down_device == ATTR_SWITCH_ON

        previous_up = self._previous_state[self._device.up]
        previous_down = self._previous_state[self._device.down]

        prev_up_on = previous_up == ATTR_SWITCH_ON \
            and previous_down == ATTR_SWITCH_OFF
        prev_down_on = previous_up == ATTR_SWITCH_OFF \
            and previous_down == ATTR_SWITCH_ON

        # returning state based on current state of up and down and previous
        # state up and down
        return (STATE_OPENING if up_on and not down_on else STATE_CLOSING
                if not up_on and down_on else STATE_CLOSED if not prev_up_on
                and prev_down_on else STATE_OPEN)

    @property
    def supported_features(self):
        """Definition what the devices supports."""
        return SUPPORT_OPEN \
            | SUPPORT_CLOSE \
            | SUPPORT_SET_POSITION \
            | SUPPORT_STOP \
            | SUPPORT_OPEN_TILT \
            | SUPPORT_CLOSE_TILT \
            | SUPPORT_STOP_TILT

    @property
    def current_position(self) -> int:
        """Current position of the shutter."""
        return self._current_possition

    @property
    def value(self):
        """Overrided value, becuase shutter has two values in one."""
        return self._device.value

    def pull_up(self, stop_after=None):
        """Turn up the shutter."""
        self.__call_service(DIRECTIONS_DICT.get(ATTR_UP))

    def pull_down(self, stop_after=None):
        """ Turn down the shutter."""
        self.__call_service(DIRECTIONS_DICT.get(ATTR_DOWN))

    def stop(self):
        """ Stop the shutter."""
        self.__call_service(DIRECTIONS_DICT.get(ATTR_STOP))

    def __call_service(self, direction):
        """Internal call of the device write value."""
        self._previous_state = self._device.value

        if direction == DIRECTIONS_DICT.get(ATTR_STOP):
            prev_up = self._previous_state[self._device.up]
            prev_down = self._previous_state[self._device.down]
            # when previous up state is
            self._current_possition = (0 if prev_down == 1
                                       and prev_up == 0
                                       else 100
                                       if prev_down == 0
                                       and prev_up == 1
                                       else 0)

            self._device.write_value(self.__set_value(
                ATTR_SWITCH_OFF, ATTR_SWITCH_OFF))
        elif direction == DIRECTIONS_DICT.get(ATTR_UP):
            self._current_possition = 100
            self._device.write_value(self.__set_value(
                ATTR_SWITCH_OFF, ATTR_SWITCH_ON))
        elif direction == DIRECTIONS_DICT.get(ATTR_DOWN):
            self._current_possition = 0
            self._device.write_value(self.__set_value(
                ATTR_SWITCH_ON, ATTR_SWITCH_OFF))

    def __set_value(self, down, up):
        """Set the value to call service."""
        return {f'{self._device.down}': down, f'{self._device.up}': up}
