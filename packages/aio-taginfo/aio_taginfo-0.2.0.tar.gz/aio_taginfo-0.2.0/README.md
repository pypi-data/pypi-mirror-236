A typed async client for the [taginfo] API, a system for finding and aggregating
information about [OpenStreetMap]'s [tags], and making it browsable and searchable.

This library makes use of [aiohttp] for requests, and [Pydantic] for parsing
and validating the responses.

[taginfo]: https://taginfo.openstreetmap.org
[OpenStreetMap]: https://www.openstreetmap.org
[tags]: https://wiki.openstreetmap.org/wiki/Tags
[aiohttp]: https://docs.aiohttp.org/
[Pydantic]: https://pydantic.dev/

#### Contents
- [Rationale](#rationale)
- [Usage](#usage)
  - [Example](#example)
- [Endpoints](#endpoints)

#### See also
- An overview of modules, classes and functions can be found in the [API reference](https://www.timwie.dev/aio-taginfo/)
- The version history is available in [CHANGELOG.md](https://github.com/timwie/aio-taginfo/blob/main/CHANGELOG.md)
- The [taginfo website](https://taginfo.openstreetmap.org/),
  its [API documentation](https://taginfo.openstreetmap.org/taginfo/apidoc),
  and its [OSM Wiki page](https://wiki.openstreetmap.org/wiki/Taginfo)

<br>

## Rationale
> OpenStreetMap uses tags to add meaning to geographic objects. There is no fixed
> list of those tags. New tags can be invented and used as needed. Everybody can
> come up with a new tag and add it to new or existing objects. This makes
> OpenStreetMap enormously flexible, but sometimes also a bit hard to work with.
> 
> Whether you are contributing to OSM or using the OSM data, there are always
> questions like: What tags do people use for feature X? What tags can I use for
> feature Y so that it appears properly on the map? Is the tag Z described on the
> wiki actually in use and where?
> 
> Taginfo helps you by showing statistics about which tags are actually in the
> database, how many people use those tags, where they are used and so on. It also
> gets information about tags from the wiki and from other places. Taginfo tries
> to bring together all information about tags to help you understand how they are
> used and what they mean.

> Taginfo has an API that lets you access the contents of its databases in several
> ways. The API is used internally for the web user interface and can also be used
> by anybody who wants to integrate taginfo data into their websites or
> applications.

<br>

## Usage
> The API is intended for the use of the OpenStreetMap community. Do not use it
> for other services. If you are not sure, ask on the mailing list (see below).
> 
> Always use a sensible User-agent header with enough information that we can
> contact you if there is a problem.
> 
> The server running the taginfo API does not have unlimited resources. Please use
> the API responsibly. Do not create huge amounts of requests to get the whole
> database or large chunks of it, instead use the [database downloads] provided.
> If you are using the API and you find it is slow, you are probably overusing it.
> 
> If you are using the taginfo API it is recommended that you join the
> [taginfo-dev mailing list]. Updates to the API will be announced there and this
> is also the right place for your questions. 

[database downloads]: https://taginfo.openstreetmap.org/download
[taginfo-dev mailing list]: https://lists.openstreetmap.org/listinfo/taginfo-dev

The data available through taginfo is licenced under [ODbL],
the same license as the OpenStreetMap data.

> OpenStreetMap[®] is open data, licensed under the
> [Open Data Commons Open Database License] (ODbL)
> by the [OpenStreetMap Foundation] (OSMF).
> 
> You are free to copy, distribute, transmit and adapt our data, as long as you
> credit OpenStreetMap and its contributors. If you alter or build upon our data,
> you may distribute the result only under the same licence. The full [legal code]
> explains your rights and responsibilities. 

[ODbL]: https://www.openstreetmap.org/copyright/en
[®]: https://www.openstreetmap.org/copyright/en#trademarks
[Open Data Commons Open Database License]: https://opendatacommons.org/licenses/odbl/
[OpenStreetMap Foundation]: https://osmfoundation.org/
[legal code]: https://opendatacommons.org/licenses/odbl/1.0/

### Example
Here is an example of an API request using this library:

```python
from aio_taginfo import key_overview

# either use a temporary session…
response: Response[KeyOverview] = await key_overview(key="amenity")

# …or provide your own
async with aiohttp.ClientSession() as session:
    response: Response[KeyOverview] = await key_overview(key="amenity", session=session)
```

<br>

## Endpoints
This library is early in development and most endpoints are still missing.


|     | Endpoint                             | Schema    |
|----:|--------------------------------------|-----------|
|     | `/api/4/key/chronology`              | multiple  |
|     | `/api/4/key/combinations`            | paginated |
|   ✅ | `/api/4/key/distribution/nodes`      | image     |
|     | `/api/4/key/distribution/ways`       | image     |
|   ✅ | `/api/4/key/overview`                | single    |
|   ✅ | `/api/4/key/prevalent_values`        | multiple  |
|     | `/api/4/key/projects`                | paginated |
|   ✅ | `/api/4/key/similar`                 | paginated |
|     | `/api/4/key/stats`                   | multiple  |
|     | `/api/4/key/values`                  | paginated |
|     | `/api/4/key/wiki_pages`              | multiple  |
|     | `/api/4/keys/all`                    | paginated |
|     | `/api/4/keys/similar`                | paginated |
|     | `/api/4/keys/wiki_pages`             | paginated |
|     | `/api/4/keys/without_wiki_page`      | paginated |
|     | `/api/4/project/icon`                | image     |
|     | `/api/4/project/tags`                | paginated |
|     | `/api/4/projects/all`                | paginated |
|     | `/api/4/projects/keys`               | paginated |
|     | `/api/4/projects/tags`               | paginated |
|     | `/api/4/relation/projects`           | paginated |
|     | `/api/4/relation/roles`              | paginated |
|     | `/api/4/relation/stats`              | multiple  |
|     | `/api/4/relation/wiki_pages`         | multiple  |
|     | `/api/4/relations/all`               | paginated |
|     | `/api/4/search/by_key_and_value`     | paginated |
|     | `/api/4/search/by_keyword`           | paginated |
|     | `/api/4/search/by_role`              | paginated |
|     | `/api/4/search/by_value`             | paginated |
|   ✅ | `/api/4/site/config/geodistribution` | other     |
|     | `/api/4/site/info`                   | other     |
|     | `/api/4/site/sources`                | other     |
|     | `/api/4/tag/chronology`              | multiple  |
|     | `/api/4/tag/combinations`            | paginated |
|     | `/api/4/tag/distribution/nodes`      | image     |
|     | `/api/4/tag/distribution/ways`       | image     |
|     | `/api/4/tag/overview`                | single    |
|     | `/api/4/tag/projects`                | paginated |
|     | `/api/4/tag/stats`                   | multiple  |
|     | `/api/4/tag/wiki_pages`              | multiple  |
|     | `/api/4/tags/list`                   | multiple  |
|     | `/api/4/tags/popular`                | paginated |
|     | `/api/4/unicode/characters`          | multiple  |
|     | `/api/4/wiki/languages`              | multiple  |