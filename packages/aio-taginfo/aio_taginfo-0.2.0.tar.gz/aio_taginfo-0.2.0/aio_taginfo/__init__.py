"""
Typed async client for the taginfo API.

The ``aio_taginfo.api`` module structure is derived from the endpoint path segments.
All the calls are re-exported here at the top level for convenience.

**Jump to:**
* ``aio_taginfo.api.v4.key.distribution.nodes``
* ``aio_taginfo.api.v4.key.overview``
* ``aio_taginfo.api.v4.key.prevalent_values``
* ``aio_taginfo.api.v4.key.similar``
* ``aio_taginfo.api.v4.site.config.geodistribution``
"""
import importlib.metadata


__version__: str = importlib.metadata.version("aio-taginfo")

__docformat__ = "google"

__all__ = (
    "api",
    "error",
    "key_distribution_nodes",
    "key_overview",
    "key_prevalent_values",
    "key_similar",
    "site_config_geodistribution",
    "TagInfoError",
)

from aio_taginfo.api.v4.key.distribution.nodes import call as key_distribution_nodes
from aio_taginfo.api.v4.key.overview import call as key_overview
from aio_taginfo.api.v4.key.prevalent_values import call as key_prevalent_values
from aio_taginfo.api.v4.key.similar import call as key_similar
from aio_taginfo.api.v4.site.config.geodistribution import call as site_config_geodistribution
from aio_taginfo.error import TagInfoError
