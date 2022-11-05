from datetime import datetime, timedelta
from time import mktime

import urllib.parse
from enum import Enum

import settings
from client.account import Account
from client.descriptors import Amount, ObjectList
from request_service import MonobankRequest
from services.datetime_service import DateTimeConverter


class OperationType(Enum):
    RECEIVE = 'Input operation'
    SEND = 'Output operation'


class Operation:
    amount = Amount()
    operation_mount = Amount()
    cashback_amount = Amount()
    balance = Amount()

    def __init__(self, operation_data: dict):
        self.id = operation_data.get('id')
        self.time = operation_data.get('time')
        self.description = operation_data.get('description')
        self.mcc = operation_data.get('mcc')
        self.hold = operation_data.get('hold')
        self.amount = operation_data.get('amount')
        self.operation_mount = operation_data.get('operationAmount')
        self.currency_code = operation_data.get('currencyCode')
        self.commission_rate = operation_data.get('commissionRate')
        self.cashback_amount = operation_data.get('cashbackAmount')
        self.balance = operation_data.get('balance')
        self.comment = operation_data.get('comment')
        self.receipt_id = operation_data.get('receiptId')
        self.invoice_id = operation_data.get('invoiceId')
        self.counter_iban = operation_data.get('counterEdrpou')
        self.direction = OperationType.RECEIVE if self.amount > 0 else OperationType.SEND
        self.date = DateTimeConverter.from_timestamp_to_date(self.time)


class Statement:
    operations = ObjectList(Operation)

    def __init__(self, account: Account | str = 0, start_date: str = None, duration: int = 31):
        if start_date is None:
            self.start_date = DateTimeConverter.date_from_now(duration)
        else:
            self.start_date = DateTimeConverter.from_str_to_date(start_date)
        self.start_timestamp = DateTimeConverter.from_date_to_timestamp(self.start_date)
        self.end_date = self.start_date + timedelta(days=duration)
        self.end_timestamp = DateTimeConverter.from_date_to_timestamp(self.end_date)
        self.account = account
        self.operations = self._get_actions()

    def _get_actions(self):
        url = urllib.parse.urljoin(
            settings.API_GATEWAY,
            f'personal/statement/{self.account}/{self.start_timestamp}/{self.end_timestamp}'
        )
        return MonobankRequest.get_request_data(url)

    def get_receive_operations(self):
        return[operation for operation in self.operations if operation.direction == OperationType.RECEIVE]

    def get_send_operations(self):
        return [operation for operation in self.operations if operation.direction == OperationType.SEND]
