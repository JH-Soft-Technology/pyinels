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
    SUPPORT_OPEN,
    SUPPORT_CLOSE,
    SUPPORT_SET_POSITION,
    SUPPORT_STOP,
    SUPPORT_OPEN_TILT,
    SUPPORT_CLOSE_TILT,
    SUPPORT_STOP_TILT,
    STATE_OPEN,
    STATE_CLOSING,
    STATE_OPENING,
    # STATE_CLOSED
)

MIN_RANGE = RANGE_BLIND[0]
MAX_RANGE = RANGE_BLIND[1]


class pyShutter(pyBase):
    """Inels class shutter."""

    def __init__(self, device):
        """Initialize shutter."""
        super().__init__(device)
        # self._timer = pyTimer()
        # self.__time_to_stop = 0
        # self.__last_position = MAX_RANGE

    @property
    def state(self):
        """State where the shutter is."""
        up_device = self.up
        down_device = self.down

        up_on = up_device == ATTR_SWITCH_ON \
            and down_device == ATTR_SWITCH_OFF
        down_on = up_device == ATTR_SWITCH_OFF \
            and down_device == ATTR_SWITCH_ON

        # if self.should_stop:
        #     if up_on and not down_on:
        #         state = STATE_OPEN
        #     elif not up_on and down_on:
        #         state = STATE_CLOSED
        # else:
        return (STATE_OPENING if up_on and not down_on else STATE_CLOSING
                if not up_on and down_on else STATE_OPEN)

    # @property
    # def should_stop(self):
    #     """It is watching if the time to stop evaluate or not"""

    #     # stop the shutter
    #     result = True

    #     if self._timer.is_running:
    #         # timer is still working
    #         self._timer.update_tick()

    #         # when the timer reach of counting, then stop it
    #         # otherwise return false
    #         if self._timer.elapsed_time < 0:
    #             self._timer.stop()
    #         else:
    #             result = False

    #     return result

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

    # @property
    # def current_position(self):
    #     """Current position of the shutter."""
    #     # It is calculated from the time to close the shutter,
    #     # defined with pull up or pull down fnc called.
    #     # 0 - fully closed - MIN_RANGE
    #     # 100 - fully opened - MAX_RANGE
    #     state = self.state

    #     position = self.__last_position

    #     # this is a situation when is not set the timer to count
    #     if self.__time_to_stop == 0:
    #         position = MAX_RANGE if state is STATE_CLOSING else MIN_RANGE
    #     else:
    #         percent = 0
    #         # calculate the position based on time to stop and current
    #         # tick of the timer
    #         if self._timer.tick is not None:
    #             tick = int(self._timer.tick)
    #             percent = percent if tick == 0 else (
    #                 tick / self.__time_to_stop) * 100

    #             percent = int(MAX_RANGE if percent > MAX_RANGE else percent)
    #         # when the timer stops and last position is the same as one
    #         # of the range side then return the last position
    #         elif self._timer.tick is None and \
    #                 (self.__last_position == MIN_RANGE \
    #                       or self.__last_position
    #                     == MAX_RANGE):
    #             return self.__last_position

    #         if state is STATE_CLOSING:
    #             position = MIN_RANGE if position < MIN_RANGE \
    #                 else MAX_RANGE - percent
    #         elif state is STATE_OPENING:
    #             position = MAX_RANGE if position > MAX_RANGE \
    #                 else MIN_RANGE + percent
    #         elif state is STATE_CLOSED:
    #             position = MIN_RANGE
    #         elif state is STATE_OPEN:
    #             position = MAX_RANGE

    #     self.__last_position = position

    #     return int(self.__last_position)

    def pull_up(self, stop_after=None):
        """Turn up the shutter."""
        # self.__set_time_to_stop(stop_after)
        # self._timer.start(self.__time_to_stop)

        self.__call_service(DIRECTIONS_DICT.get(ATTR_UP))

    def pull_down(self, stop_after=None):
        """ Turn down the shutter."""
        # self.__set_time_to_stop(stop_after)
        # self._timer.start(self.__time_to_stop)

        self.__call_service(DIRECTIONS_DICT.get(ATTR_DOWN))

    def stop(self):
        """ Stop the shutter."""
        # if self._timer.is_running:
        #     self._timer.stop()

        self.__call_service(DIRECTIONS_DICT.get(ATTR_STOP))

    def __call_service(self, direction):
        """Internal call of the device write value."""

        if direction == DIRECTIONS_DICT.get(ATTR_STOP):
            self._device.write_value(self.__set_value(
                ATTR_SWITCH_OFF, ATTR_SWITCH_OFF))
        elif direction == DIRECTIONS_DICT.get(ATTR_UP):
            self._device.write_value(self.__set_value(
                ATTR_SWITCH_OFF, ATTR_SWITCH_ON))
        elif direction == DIRECTIONS_DICT.get(ATTR_DOWN):
            self._device.write_value(self.__set_value(
                ATTR_SWITCH_ON, ATTR_SWITCH_OFF))

    def __set_value(self, down, up):
        """Set the value to call service."""
        return {f'{self._device.down}': down, f'{self._device.up}': up}

    # def __set_time_to_stop(self, stop_after):
    #     """Set time to stop private function."""
    #     if stop_after is not None:
    #         self.__time_to_stop = stop_after
