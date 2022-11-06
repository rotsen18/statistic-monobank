import os

import requests

import settings
from services.cache import Cache


class MonobankRequest:
    cache = Cache(cache_path=os.path.join('services', settings.CACHE_FILENAME))

    @classmethod
    def get_request_data(cls, url: str):
        headers = {'X-Token': settings.TOKEN}
        data = cls.cache.get_from_cache(url)
        if data:
            return data
        data = requests.get(url, headers=headers).json()
        cls.cache.write_to_cache(url, data)
        return data
