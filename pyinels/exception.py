"""Library specified for iNels BUS."""
import logging

from dataclasses import dataclass

_LOGGER = logging.getLogger(__name__)


@dataclass
class ApiException(Exception):
    """Base iNels BUS exception."""
    code: str
    message: str
    trace: Exception = None


@dataclass
class ApiConnectionException(ApiException):
    """Connection exception class."""


@dataclass
class ApiDataTypeException(ApiException):
    """Bad type exception."""


@dataclass
class ApiClassTypeException(ApiException):
    """Bad Class type exception."""
