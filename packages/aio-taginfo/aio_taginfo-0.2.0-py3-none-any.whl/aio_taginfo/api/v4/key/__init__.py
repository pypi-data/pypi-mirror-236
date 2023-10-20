"""`/api/v4/key/` endpoints."""

from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class PrevalentValue:
    """
    One value of a given tag and the number of times it was used.

    Attributes:
        value: The tag value or ``None`` to count the sum of the counts for all values not listed
        count: Number of objects with this tag value
        fraction: Fraction of number of objects with this tag value compared to all objects
    """

    value: str | None = Field(min_length=1, repr=True, frozen=True)
    count: int = Field(ge=0, repr=True, frozen=True)
    fraction: float = Field(ge=0.0, le=1.0, allow_inf_nan=False, repr=True, frozen=True)


__docformat__ = "google"
