import settings
import urllib.parse

from client.person import Client
from request_service import MonobankRequest
from statement.report import Report
from statement.statement import Statement


def create_client():
    url = urllib.parse.urljoin(settings.API_GATEWAY, 'personal/client-info')
    response_data = MonobankRequest.get_request_data(url)
    return Client(response_data)


def main():
    client = create_client()
    account = client.get_default_account()
    statement = Statement(account=account, start_date='01.10.2022', duration=30)
    receive_report = Report(operations=statement.get_receive_operations(), name='Receive report')
    send_report = Report(operations=statement.get_send_operations(), name='Send report')
    total_report = receive_report + send_report
    return total_report


if __name__ == '__main__':
    data = main()
