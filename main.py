import urllib.parse
from datetime import datetime

import settings
from client.account import Account
from client.person import Client
from services.datetime_service import DateTimeConverter
from services.request_service import MonobankRequest
from statement.report import Report
from statement.statement import Statement
from visualization.chart import Chart


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
        print('Available accounts:')
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


def chose_date(saved_date: str = None):
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


def chose_duration():
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
            date = chose_date()
        if duration is None:
            duration = chose_duration()
        if duration == 'date':
            date = chose_date(date)
        return Statement(account=account, start_date=date, duration=duration)


def print_report_data(receive_report, send_report, total_report):
    print()
    for report in receive_report, send_report, total_report:
        report.print_report_data()
        print('-' * 50)
        print()


def chose_report(reports):
    while True:
        print()
        print('Reports:')
        print('-' * 50)
        for number, report in reports.items():
            print(f'{number}|{report.name}')
        number = input('Chose report to build char: ')
        if not number.isdigit():
            print('Type correct integer!')
            continue
        number = int(number)
        if number not in [0, 1, 2]:
            print('Chose report from list [0, 1, 2]: ')
            continue
        return reports.get(number)


def chose_chart_type():
    variants = {
        0: {'name': 'amounts all', 'show_chart': Chart.show_amount},
        1: {'name': 'amounts per day', 'show_chart': Chart.show_amount_per_day},
        2: {'name': 'balance all', 'show_chart': Chart.show_balance},
        3: {'name': 'balance per day', 'show_chart': Chart.show_balance_per_date},
    }
    while True:
        print()
        print('Charts:')
        print('-' * 50)
        for number, chart in variants.items():
            print(f'{number}|{chart["name"]}')
        number = input('Chose chart to build char: ')
        if not number.isdigit():
            print('Type correct integer!')
            continue
        number = int(number)
        if number not in [0, 1, 2, 3]:
            print('Chose chart from list [0, 1, 2, 3]: ')
            continue
        chart = variants.get(number)
        return chart.get('show_chart')


def draw_chart(receive_report, send_report, total_report):
    while True:
        reports = {
            0: receive_report,
            1: send_report,
            2: total_report,
        }
        report = chose_report(reports)
        show_chart = chose_chart_type()
        show_chart(report)
        draw = input('Drive another one? y/n: ')
        if draw.lower().startswith('y'):
            continue
        elif draw.lower().startswith('n'):
            return


def main():
    client = create_client()
    account = chose_account(client)
    statement = get_statement(account)
    receive_report = Report(operations=statement.get_receive_operations(), name='Receive report')
    send_report = Report(operations=statement.get_send_operations(), name='Send report')
    total_report = receive_report + send_report
    print_report_data(receive_report, send_report, total_report)
    draw_chart(receive_report, send_report, total_report)
    print('EXIT')


if __name__ == '__main__':
    main()
