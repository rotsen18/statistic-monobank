import requests

import settings


class MonobankRequest:

    @staticmethod
    def get_request_data(url: str):
        headers = {'X-Token': settings.TOKEN}
        data = requests.get(url, headers=headers)
        return data.json()

