from datetime import datetime, timedelta
from time import mktime

import requests
import settings
import urllib.parse

from client.person import Client
from request_service import MonobankRequest
from statement import StatementDays, Report


def create_client():
    url = urllib.parse.urljoin(settings.API_GATEWAY, 'personal/client-info')
    data = MonobankRequest.get_request_data(url)
    client = Client(data)
    return client


def main():
    client = create_client()
    account = client.accounts[0]
    statement = StatementDays(account=account, start=31, end=0)
    receive_report = Report(operations=statement.get_receive_operations())
    send_report = Report(operations=statement.get_send_operations())
    total_report = receive_report + send_report
    return total_report


if __name__ == '__main__':
    data = main()
