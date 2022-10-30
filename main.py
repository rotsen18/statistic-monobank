from datetime import datetime, timedelta
from time import mktime

import requests
import settings
import urllib.parse

from client.person import Client
from statement import Statement


def get_request_data(url: str):
    headers = {'X-Token': settings.TOKEN}
    data = requests.get(url, headers=headers)
    return data.json()


def create_client():
    url = urllib.parse.urljoin(settings.API_GATEWAY, 'personal/client-info')
    data = get_request_data(url)
    client = Client(data)
    return client


def days_to_unix_secs(days: int):
    today = datetime.now()
    start = today - timedelta(days)
    return int(mktime(start.timetuple()))


def get_statement(from_days: int = 31, to_days: int = 0, _id: str = 0):
    _from = days_to_unix_secs(from_days)
    _to = days_to_unix_secs(to_days)
    url = urllib.parse.urljoin(settings.API_GATEWAY, f'personal/statement/{_id}/{_from}/{_to}')
    data = get_request_data(url)
    return Statement(data)


def main():
    client = create_client()
    statement = get_statement(_id='VMOFeULFVTPg1gI15d046g', from_days=31, to_days=0)
    report = statement.get_total_report()
    return report


if __name__ == '__main__':
    data = main()
    print('end')
