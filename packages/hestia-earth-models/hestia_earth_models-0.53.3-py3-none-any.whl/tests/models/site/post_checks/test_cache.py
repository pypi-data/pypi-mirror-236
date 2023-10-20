from hestia_earth.models.utils.site import CACHE_KEY

from hestia_earth.models.site.post_checks.cache import run


def rest_run():
    site = {CACHE_KEY: {}}
    assert CACHE_KEY not in run(site)
