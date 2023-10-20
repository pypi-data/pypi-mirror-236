"""`/api/v4/` endpoints."""

from datetime import datetime
from enum import Enum
from typing import Generic, TypeVar

from pydantic import Field, HttpUrl, model_validator
from pydantic.dataclasses import dataclass


__all__ = (
    "key",
    "site",
    "Response",
    "PngResponse",
    "SortOrder",
    "ObjectType",
    "PrintingDirection",
)


T = TypeVar("T")


@dataclass
class Response(Generic[T]):
    """
    JSON data response.

    Attributes:
        data: Payload specific to the called endpoint
        data_until: All changes in the source until this date are reflected in this taginfo result
        url: URL of the request
        total: Total number of results
        page: Result page number (first has page number 1)
        rp: Results per page
    """

    data: T = Field(repr=True, frozen=True)
    data_until: datetime = Field(repr=False, frozen=True)
    url: HttpUrl = Field(repr=False, frozen=True)
    total: int = Field(ge=0, repr=True, frozen=True)
    page: int | None = Field(default=None, gt=0, repr=True, frozen=True)
    rp: int | None = Field(default=None, gt=0, repr=True, frozen=True)


@dataclass
class PngResponse:
    """
    PNG image response.

    Attributes:
        data: PNG data
    """

    data: bytes = Field(repr=False, frozen=True)

    @model_validator(mode="after")
    def post_root(self) -> "PngResponse":
        """Basic PNG validation by checking for magic bytes."""
        if not self.data.startswith(_PNG_MAGIC):
            msg = "did not find PNG magic bytes"
            raise AssertionError(msg)
        return self


_PNG_MAGIC = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])


class SortOrder(str, Enum):
    """Sort order parameter (ascending by default)."""

    ASC = "asc"
    DESC = "desc"


class ObjectType(str, Enum):
    """OpenStreetMap element types."""

    ALL = "all"
    NODES = "nodes"
    WAYS = "ways"
    RELATIONS = "relations"


class PrintingDirection(str, Enum):
    """Printing direction for native text."""

    AUTO = "auto"
    LTR = "ltr"
    RTL = "rtl"


__docformat__ = "google"
