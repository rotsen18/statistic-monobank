import json
import os

import settings


class Cache:
    def __init__(self, cache_path):
        self.cache_path = cache_path

    CACHE_PATH = os.path.join('services', settings.CACHE_FILENAME)

    def write_to_cache(self, key: str, value: dict):
        if not os.path.exists(self.CACHE_PATH):
            json.dump({key: value}, open(self.CACHE_PATH, 'w'))
            return
        with open(self.CACHE_PATH, 'r') as outfile:
            data = json.load(outfile)
            data[key] = value
        json.dump(data, open(self.CACHE_PATH, 'w'))

    def get_from_cache(self, key: str):
        if not os.path.exists(self.CACHE_PATH):
            return
        with open(self.CACHE_PATH, 'r') as cache:
            data = json.load(cache)
            return data.get(key)
