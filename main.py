import urllib.parse
from datetime import datetime

import settings
from client.account import Account
from client.person import Client
from services.datetime_service import DateTimeConverter
from services.request_service import MonobankRequest
from statement.report import Report
from statement.statement import Statement


def create_client():
    print('Getting user data from Mono...')
    url = urllib.parse.urljoin(settings.API_GATEWAY, 'personal/client-info')
    response_data = MonobankRequest.get_request_data(url)
    print('Received user data')
    print('Create Client instance')
    client = Client(response_data)
    print(f'client:{client.name}')
    print(f'accounts: {len(client.accounts)}')
    print(f'jars: {len(client.jars)}')
    return client


def chose_account(client: Client):
    while True:
        print()
        print('Avaliable accounts:')
        print('-' * 50)
        for _id, account in enumerate(client.accounts):
            print(f'{str(_id).rjust(2)}|{account.id}|{account.type}|{account.balance} {account.cashback_type}')
        number = input('Choice your account or press enter for default (default: 0): ')
        if not number:
            return client.get_default_account()
        elif not number.isdigit():
            print('Type number of account from the list')
            continue
        elif int(number) not in range(1, len(client.accounts) + 1):
            print(f'Type number of account from the list {list(range(len(client.accounts)))}')
        return client.accounts[int(number)]


def get_date(saved_date: str = None):
    while True:
        print()
        if saved_date:
            print(f'Previous date: {saved_date}')
        print('Write start date in format DD.MM.YYYY (ex.25.10.2015)')
        default_date = DateTimeConverter.date_from_now(31).date().strftime(settings.DATE_FORMAT)
        print(f'Or press enter for default value - 31 days ago: {default_date}')
        date = input('Your date: ')
        if not date:
            date = default_date
            print(f'date DEFAULT: {date}')
            return date
        else:
            try:
                datetime.strptime(date, settings.DATE_FORMAT)
            except Exception as e:
                print(e)
                print(f'date NOT OK')
                continue
            else:
                print(f'date OK: {date}')
                return date


def get_duration():
    while True:
        print('Write statement length (min:0, max:31 days)')
        print('If ou want change selected date before you can type "date" here')
        received_duration = input('Or press enter for default (31 days): ')
        if received_duration.isdigit():
            print(f'duration OK: {received_duration}')
            return int(received_duration)
        elif not received_duration:
            print('duration DEFAULT: 31')
            return 31
        elif received_duration.lower() == 'date':
            print(f'duration NOT OK: new date')
            return 'date'
        else:
            print('Write correct digit!')
            continue


def get_statement(account: Account):
    date = None
    duration = None
    while True:
        if date is None:
            date = get_date()
        if duration is None:
            duration = get_duration()
        if duration == 'date':
            date = get_date(date)
        return Statement(account=account, start_date=date, duration=duration)



def print_report_data(receive_report, send_report, total_report):
    print()
    for report in receive_report, send_report, total_report:
        report.print_report_data()
        print('-' * 50)
        print()


def draw_chart():
    pass


def main():
    client = create_client()
    account = chose_account(client)
    statement = get_statement(account)
    receive_report = Report(operations=statement.get_receive_operations(), name='Receive report')
    send_report = Report(operations=statement.get_send_operations(), name='Send report')
    total_report = receive_report + send_report
    print_report_data(receive_report, send_report, total_report)


if __name__ == '__main__':
    main()
