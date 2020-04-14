"""Class Api resources returned from the iNels BUS."""
import logging

from pyinels.exception import ApiClassTypeException

from pyinels.const import (
    ATTR_DOWN,
    ATTR_GROUP,
    ATTR_ID,
    ATTR_READ_ONLY,
    ATTR_RELE,
    ATTR_TEMP,
    ATTR_TEMP_SET,
    ATTR_TITLE,
    ATTR_TYPE,
    ATTR_UP,
    INELS_BUS_ATTR_DICT
)

_LOGGER = logging.getLogger(__name__)


class ApiResource:
    """Object returned from the iNels BUS."""

    @property
    def id(self):
        """Id of the object."""
        if INELS_BUS_ATTR_DICT.get(ATTR_ID) not in self.__json:
            return None
        return self.__json[INELS_BUS_ATTR_DICT.get(ATTR_ID)]

    @property
    def title(self):
        """Name of the object."""
        return self.__json[INELS_BUS_ATTR_DICT.get(ATTR_TITLE)]

    @property
    def type(self):
        """Type of the object."""
        return self.__json[INELS_BUS_ATTR_DICT.get(ATTR_TYPE)]

    @property
    def temperature(self):
        """Temperature of the object."""
        if INELS_BUS_ATTR_DICT.get(ATTR_TEMP) not in self.__json:
            return None
        return self.__json[INELS_BUS_ATTR_DICT.get(ATTR_TEMP)]

    @property
    def temperature_set(self):
        """Temperature of the object."""
        if INELS_BUS_ATTR_DICT.get(ATTR_TEMP_SET) not in self.__json:
            return None
        return self.__json[INELS_BUS_ATTR_DICT.get(ATTR_TEMP_SET)]

    @property
    def rele(self):
        """Rele of the object."""
        if INELS_BUS_ATTR_DICT.get(ATTR_RELE) not in self.__json:
            return None
        return self.__json[INELS_BUS_ATTR_DICT.get(ATTR_RELE)]

    @property
    def read_only(self):
        """Read only of the object."""
        if INELS_BUS_ATTR_DICT.get(ATTR_READ_ONLY) not in self.__json:
            return None
        return self.__json[INELS_BUS_ATTR_DICT.get(ATTR_READ_ONLY)]

    @property
    def down(self):
        """Shutter down of the object."""
        if INELS_BUS_ATTR_DICT.get(ATTR_DOWN) not in self.__json:
            return None
        return self.__json[INELS_BUS_ATTR_DICT.get(ATTR_DOWN)]

    @property
    def up(self):
        """Shutter up of the object."""
        if INELS_BUS_ATTR_DICT.get(ATTR_UP) not in self.__json:
            return None
        return self.__json[INELS_BUS_ATTR_DICT.get(ATTR_UP)]

    @property
    def group(self):
        """Group from where the object is loaded."""
        if INELS_BUS_ATTR_DICT.get(ATTR_GROUP) not in self.__json:
            return None
        return self.__json[INELS_BUS_ATTR_DICT.get(ATTR_GROUP)]

    @property
    def value(self):
        """Value of the returned object."""
        if hasattr(self, '_ApiResource__value'):
            return self.__value

        return None

    def __init__(self, json, api):
        """Initializer of the Api resource."""
        self.__json = json
        self.__api = api

    def observe(self, options=None):
        """Read the current value of the device."""
        try:
            if options:
                if not isinstance(options, Observe):
                    raise ApiClassTypeException(
                        '500', f"""Device.observe options
                        param has bad type. {type(options)}.
                        Should by Observe.""")

            raw = self.__api.read([self.id])
            self.__value = raw[self.id]

            if options:
                options.callback(self)

            return self.__value
        except ApiClassTypeException as ex:
            raise ex
        except Exception:
            if options:
                options.err_callback()
            # this is the situation when the proxy is
            # probably not available, then we are going to
            # se the value to None
            self.__value = None

        return None

    def set_value(self, value):
        """Set value to the device."""

        # initialize __value attribute
        if hasattr(self, '_ApiResource__value') is False:
            self.__value = 0

        curr_int = isinstance(self.__value, int)
        new_int = isinstance(value, int)

        if (self.__value != value or curr_int is not new_int):
            self.__value = value
            self.__api.write(self, value)

    @property
    def is_available(self):
        """Device availability property."""
        # first test when device has any value
        if hasattr(self, '_ApiResource__value'):
            return True
        else:
            # if not then try to observer
            self.observe()
        # when nothing change then device is not available
        return False if self.__value is None else True


class Observe:
    """Class defined observe option object."""

    @property
    def callback(self):
        """Callback property."""
        return self.__callback

    @property
    def err(self):
        """Error property."""
        return self.__err_callback

    def __init__(self, callback, err):
        """Initialize Observe object."""
        self.__callback = callback
        self.__err_callback = err
