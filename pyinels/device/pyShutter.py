"""Inels shutter class to control blinds."""
from pyinels.device.pyBase import pyBase
from pyinels.timer import Timer

from pyinels.const import (
    ATTR_SWITCH_ON,
    ATTR_SWITCH_OFF,
    SUPPORT_OPEN,
    SUPPORT_CLOSE,
    SUPPORT_STOP,
    SUPPORT_OPEN_TILT,
    SUPPORT_CLOSE_TILT,
    SUPPORT_STOP_TILT,
    STATE_OPEN,
    STATE_CLOSING,
    STATE_OPENING,
    STATE_CLOSED
)


class pyShutter(pyBase):
    """Inels class shutter."""

    def __init__(self, device):
        """Initialize object."""
        super().__init__(device)
        self.__timmer = Timer()
        self.__timeToStop = 0

    @property
    def state(self):
        """State where the shutter is."""
        up_device = self._device.value[self._device.up]
        down_device = self._device.value[self._device.down]

        up_on = up_device == ATTR_SWITCH_ON \
            and down_device == ATTR_SWITCH_OFF
        down_on = up_device == ATTR_SWITCH_OFF \
            and down_device == ATTR_SWITCH_ON

        state = (STATE_OPENING
                 if up_on and not down_on
                 else STATE_CLOSING
                 if not up_on and down_on
                 else None)

        if self.should_stop is True:
            if up_on and not down_on:
                state = STATE_OPEN
            elif not up_on and down_on:
                state = STATE_CLOSED

        return state

    @property
    def should_stop(self):
        """It is watching if the time to stop evaluate or not"""
        if self.__timeToStop == 0:
            return True

        # stop the shutter
        result = True

        if self.__timmer._start_time is not None:
            # timer is still working
            self.__timmer.update_tick()

            result = self.__timeToStop - self.__timmer.tick <= 0

            # when the timer reach of counting, then stop it
            # otherwise return false
            if result is True:
                self.__timmer.stop()
            else:
                result = False

        return result

    @property
    def supported_features(self):
        """Definition what the devices supports."""
        return SUPPORT_OPEN \
            | SUPPORT_CLOSE \
            | SUPPORT_STOP \
            | SUPPORT_OPEN_TILT \
            | SUPPORT_CLOSE_TILT \
            | SUPPORT_STOP_TILT

    def pull_up(self, stop_after=None):
        """Turn up the shutter."""
        self.__timmer.start(STATE_OPENING)

        value = {f'{self._device.down}': ATTR_SWITCH_OFF,
                 f'{self._device.up}': ATTR_SWITCH_ON}

        self.__call_service(value, self._device.up, stop_after)

    def pull_down(self, stop_after=None):
        """ Turn down the shutter."""
        self.__timmer.start(STATE_CLOSING)

        value = {f'{self._device.down}': ATTR_SWITCH_ON,
                 f'{self._device.up}': ATTR_SWITCH_OFF}

        self.__call_service(value, self._device.down, stop_after)

    def stop(self):
        """ Stop the shutter."""
        direction = self.__timmer._direction

        self.__timmer.stop()

        value = {f'{self._device.down}': ATTR_SWITCH_OFF,
                 f'{self._device.up}': ATTR_SWITCH_OFF}

        self.__call_service(value, self._device.down)

        return direction

    def __call_service(self, value, direction, stop_after=None):
        """Internal call of the device write value."""
        self._device.write_value(value, direction)

        if stop_after is not None:
            self.__timeToStop = stop_after
