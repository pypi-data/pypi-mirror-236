"""Error types."""

from dataclasses import dataclass

import aiohttp
import pydantic


class TagInfoError(Exception):
    """Base class for taginfo API errors."""


@dataclass
class TagInfoValueError(Exception):
    """Failed to validate given parameters; did not call the taginfo API."""

    cause: pydantic.ValidationError


@dataclass
class TagInfoCallError(Exception):
    """Failed HTTP call to the taginfo API."""

    cause: aiohttp.ClientError


@dataclass
class TagInfoValidationError(Exception):
    """
    Failed to validate the response of the taginfo API.

    This should usually indicate a bug in this library.
    """

    cause: pydantic.ValidationError


__docformat__ = "google"
