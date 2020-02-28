"""Library specified for iNels BUS CU3."""
import logging

from dataclasses import dataclass

_LOGGER = logging.getLogger(__name__)


@dataclass
class InelsBusException(Exception):
    """Base iNels BUS exception."""
    code: str
    message: str
    trace: Exception = None


@dataclass
class InelsBusConnectionException(InelsBusException):
    """Connection exception class."""


@dataclass
class InelsBusDataTypeException(InelsBusException):
    """Bad type exception."""


@dataclass
class InelsBusClassTypeException(InelsBusException):
    """Bad Class type exception."""
