import json
import os

import requests

import settings


class MonobankRequest:
    CACHE_PATH = os.path.join('services', settings.CACHE_FILENAME)

    @classmethod
    def get_request_data(cls, url: str):
        headers = {'X-Token': settings.TOKEN}
        data = cls._get_from_cache(url)
        if data:
            print('get from cache', data)
            return data
        data = requests.get(url, headers=headers).json()
        cls._write_to_cache(url, data)
        return data

    @classmethod
    def _write_to_cache(cls, key: str, value: dict):
        if not os.path.exists(cls.CACHE_PATH):
            json.dump({key: value}, open(cls.CACHE_PATH, 'w'))
            return
        with open(cls.CACHE_PATH, 'r') as outfile:
            data = json.load(outfile)
            data[key] = value
        json.dump(data, open(cls.CACHE_PATH, 'w'))

    @classmethod
    def _get_from_cache(cls, key: str):
        if not os.path.exists(cls.CACHE_PATH):
            return
        with open(cls.CACHE_PATH, 'r') as cache:
            data = json.load(cache)
            return data.get(key)
