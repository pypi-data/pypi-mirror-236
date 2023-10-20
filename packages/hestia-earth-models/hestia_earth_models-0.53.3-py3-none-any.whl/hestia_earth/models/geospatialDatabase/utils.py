import os
from hestia_earth.schema import TermTermType
from hestia_earth.utils.api import download_hestia

from hestia_earth.models.log import debugValues, logErrorRun, logRequirements
from hestia_earth.models.utils.site import CACHE_KEY, region_factor, region_level_1_id
from . import MODEL

MAX_AREA_SIZE = int(os.getenv('MAX_AREA_SIZE', '5000'))
CACHE_VALUE = MODEL
CACHE_AREA_SIZE = 'areaSize'


def _cached_value(site: dict, key: str):
    return site.get(CACHE_KEY, {}).get(CACHE_VALUE, {}).get(key)


def _collection_name(id: str): return id if '/' in id else f"users/hestiaplatform/{id}"


def has_coordinates(site: dict): return all([site.get('latitude') is not None, site.get('longitude') is not None])


def has_boundary(site: dict): return site.get('boundary') is not None


def _site_gadm_id(site: dict): return site.get('region', site.get('country', {})).get('@id')


def has_geospatial_data(site: dict):
    """
    Determines whether the Site has enough geospatial data to run calculations. We are checking for:
    1. If the coordinates (latitude and longitude) are present
    2. Otherwise if the `region` or `country` is present
    3. Otherwise if the `boundary` is present
    Note: this is a general pre-check only, each model can have 1 or more other checks.

    Parameters
    ----------
    site : dict
        The `Site` node.

    Returns
    -------
    bool
        If we should run geospatial calculations on this model or not.
    """
    return has_coordinates(site) or _site_gadm_id(site) is not None or has_boundary(site)


def geospatial_data(site: dict, only_coordinates=False):
    return {
        'coordinates': [{'latitude': site.get('latitude'), 'longitude': site.get('longitude')}]
    } if has_coordinates(site) else ({} if only_coordinates else {
        'boundaries': [site.get('boundary')]
    } if has_boundary(site) else {
        'gadm-ids': [_site_gadm_id(site)]
    })


def _get_boundary_area_size(boundary: dict):
    try:
        from hestia_earth.earth_engine.boundary import get_size_km2
    except ImportError:
        raise ImportError("Run `pip install hestia_earth.earth_engine` to use this functionality")

    try:
        return get_size_km2(boundary)
    except Exception:
        return None


def get_area_size(site: dict):
    return (
        # fallback if `boundary` provided but no `boundaryArea` was computed
        site.get('boundaryArea') or _get_boundary_area_size(site.get('boundary'))
    ) if has_boundary(site) else download_hestia(_site_gadm_id(site)).get('area')


def _is_below_max_size(term: str, site: dict) -> bool:
    current_size = _cached_value(site, CACHE_AREA_SIZE) or get_area_size(site)
    if current_size is not None:
        logRequirements(site, model=MODEL, term=term,
                        current_size=int(current_size),
                        max_area_size=MAX_AREA_SIZE)
        return current_size <= MAX_AREA_SIZE
    return True


def should_download(term: str, site: dict) -> bool:
    return has_coordinates(site) or _is_below_max_size(term, site)


def _run_query(query: dict):
    try:
        from hestia_earth.earth_engine import run
    except ImportError:
        raise ImportError("Run `pip install hestia_earth.earth_engine` to use this functionality")

    return run(query)


def _parse_run_query(term: str, query: dict):
    try:
        res = _run_query(query)
        return res[0] if len(res) > 0 else None
    except Exception as e:
        logErrorRun(MODEL, term, str(e))
        return None


def _get_cached_data(term: str, site: dict, data: dict):
    cache = _cached_value(site, term)
    # data can be grouped by year when required
    value = cache.get(data.get('year')) if data.get('year') and cache is not None else cache
    if value is not None:
        debugValues(site, model=MODEL, term=term, value_from_cache=value)
    return value


def download(term: str, site: dict, data: dict, only_coordinates=False) -> dict:
    """
    Downloads data from Hestia Earth Engine API.

    Returns
    -------
    dict
        Data returned from the API.
    """
    location_data = geospatial_data(site, only_coordinates=only_coordinates)
    query = {
        'ee_type': data.get('ee_type'),
        **location_data,
        'collections': [
            {
                **data,
                'collection': _collection_name(data.get('collection'))
            }
        ]
    }
    # check if we have cached the result already, else run and parse result
    value = _get_cached_data(term, site, data) or _parse_run_query(term, query)
    if value is None:
        debugValues(site, model=MODEL, term=term, value_from_earth_engine=None)
    return value


def get_region_factor(term_id: str, site: dict, termType: TermTermType = TermTermType.MEASUREMENT):
    region_id = region_level_1_id(site.get('region', {}).get('@id'))
    country_id = site.get('country', {}).get('@id')
    return region_factor(MODEL, region_id, term_id, termType) or region_factor(MODEL, country_id, term_id, termType)
