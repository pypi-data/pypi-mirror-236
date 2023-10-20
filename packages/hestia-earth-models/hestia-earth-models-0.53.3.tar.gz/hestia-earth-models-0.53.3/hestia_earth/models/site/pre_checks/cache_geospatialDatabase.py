"""
Site Pre Checks Cache Geospatial Database

This model caches results from Geospatial Database.
"""
from functools import reduce
from hestia_earth.utils.tools import flatten

from hestia_earth.models.geospatialDatabase.utils import (
    MAX_AREA_SIZE, CACHE_VALUE, CACHE_AREA_SIZE,
    has_geospatial_data, has_coordinates, get_area_size, geospatial_data, _run_query, _collection_name
)
from hestia_earth.models.geospatialDatabase import list_ee_params
from hestia_earth.models.utils.site import CACHE_KEY, related_years
from hestia_earth.models.log import debugValues

REQUIREMENTS = {
    "Site": {
        "or": [
            {"latitude": "", "longitude": ""},
            {"boundary": {}},
            {"region": {"@type": "Term", "termType": "region"}}
        ]
    }
}
RETURNS = {
    "Site": {}
}


def _extend_collection(name: str, collection: dict, years: list = []):
    data = collection | {'name': name, 'collection': _collection_name(collection.get('collection'))}
    return [
        data | {
            'year': str(year)
        } for year in years
    ] if 'reducer_annual' in collection and 'reducer_period' not in collection else [data]


def _cache_results(site: dict, area_size: float):
    # to fetch data related to the year
    years = related_years(site)

    ee_params = list_ee_params()
    # only cache `raster` results as can be combined in a single query
    ee_params = [value for value in ee_params if value.get('params').get('ee_type') == 'raster']

    collections = flatten([
        _extend_collection(value.get('name'), value.get('params'), years) for value in ee_params
    ])
    query = {
        'ee_type': 'raster',
        'collections': collections,
        **geospatial_data(site)
    }
    results = _run_query(query)

    def _combine_result(group: dict, index: int):
        collection = collections[index]
        name = collection.get('name')
        value = results[index]
        data = (group.get(name, {}) | {collection.get('year'): value}) if 'year' in collection else value
        return group | {name: data}

    return {
        CACHE_AREA_SIZE: area_size,
        **reduce(_combine_result, range(0, len(results)), {})
    }


def _should_cache_results(site: dict):
    area_size = get_area_size(site)
    contains_geospatial_data = has_geospatial_data(site)
    contains_coordinates = has_coordinates(site)
    has_cache = site.get(CACHE_KEY, {}).get(CACHE_VALUE) is not None

    debugValues(site,
                area_size=area_size,
                MAX_AREA_SIZE=MAX_AREA_SIZE,
                contains_geospatial_data=contains_geospatial_data,
                has_cache=has_cache)

    should_cache = all([
        not has_cache,
        contains_coordinates or area_size <= MAX_AREA_SIZE,
        contains_geospatial_data
    ])
    return should_cache, area_size


def run(site: dict):
    should_cache, area_size = _should_cache_results(site)
    return {
        **site,
        CACHE_KEY: {**site.get(CACHE_KEY, {}), CACHE_VALUE: _cache_results(site, area_size)}
    } if should_cache else site
