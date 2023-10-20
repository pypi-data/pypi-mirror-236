"""`/api/v4/key/prevalent_values` endpoint."""
from typing import Annotated

from aio_taginfo.api.v4 import ObjectType, Response
from aio_taginfo.api.v4._internal import api_get_json, api_params
from aio_taginfo.api.v4.key import PrevalentValue

from aiohttp import ClientSession
from pydantic import Field, StringConstraints
from pydantic.dataclasses import dataclass


@dataclass
class _Params:
    key: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] = Field(
        repr=True, frozen=True
    )
    min_fraction: float = Field(ge=0.01, le=1.0, allow_inf_nan=False, repr=True, frozen=True)
    filter: ObjectType = Field(repr=True, frozen=True)


async def call(
    key: str,
    min_fraction: float = 0.01,
    filter: ObjectType = ObjectType.ALL,
    session: ClientSession | None = None,
) -> Response[list[PrevalentValue]]:
    """
    Get most prevalent values used with a given key.

    https://taginfo.openstreetmap.org/taginfo/apidoc#api_4_key_prevalent_values

    Args:
        key: tag key
        min_fraction: only return values which are used in at least this percent
                      of all objects with this key (defaults to 0.01)
        filter: can be used to filter only values on tags used on nodes/ways/relations
        session: request client session

    Raises:
        TagInfoError
    """
    params = api_params(_Params, key=key, min_fraction=min_fraction, filter=filter)
    return await api_get_json(
        path="key/prevalent_values",
        cls=Response[list[PrevalentValue]],
        session=session,
        params=params,
    )


__docformat__ = "google"
