from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from time import mktime

import urllib.parse
from enum import Enum

import settings
from client.account import Account
from client.descriptors import Amount, ObjectList
from request_service import MonobankRequest


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
        self.date = self._timestamp_to_date(self.time)

    @staticmethod
    def _timestamp_to_date(value: int):
        return datetime.fromtimestamp(value)


class Report:
    def __init__(self, name: str = '', operations: list[Operation] = None):
        self.name = name
        self.count_operations: int = 0
        self.total_amount: float = 0.0
        self.total_operation_amount: float = 0.0
        self.total_cashback_amount: float = 0.0
        self.total_commission_amount: float = 0.0
        self.operations = []
        if operations is not None:
            for operation in operations:
                self.add_operation(operation)
            self.first_operation_date = None or min(operation.date for operation in self.operations)
            self.last_operation_date = None or max(operation.date for operation in self.operations)

    def add_operation(self, operation: Operation):
        self.count_operations += 1
        self.total_amount += operation.amount
        self.total_operation_amount += operation.operation_mount
        self.total_cashback_amount += operation.cashback_amount
        self.total_commission_amount += operation.commission_rate
        self.operations.append(operation)

    def __add__(self, other):
        # if isinstance(other, Report):
        #     raise ValueError
        report = Report('Total report')
        report.count_operations = self.count_operations + other.count_operations
        report.total_amount = round(self.total_amount + other.total_amount, 2)
        report.total_operation_amount = round(self.total_operation_amount + other.total_operation_amount, 2)
        report.total_cashback_amount = round(self.total_cashback_amount + other.total_cashback_amount, 2)
        report.total_commission_amount = round(self.total_commission_amount + other.total_commission_amount, 2)
        report.first_operation_date = min(self.first_operation_date, other.first_operation_date)
        report.last_operation_date = max(self.last_operation_date, other.last_operation_date)
        report.operations = self.operations + other.operations
        return report


class BaseStatement(ABC):
    operations = ObjectList(Operation)

    def __init__(self, account: Account | str, start: int, end: int = 0):
        self.start = start
        self.end = end
        self.account = account.id if isinstance(account, Account) else account
        self._interval_converter()
        self.operations = self._get_actions()
        self.start_date = self._timestamp_to_date(self.start)
        self.end_date = self._timestamp_to_date(self.end)

    @abstractmethod
    def _interval_converter(self):
        raise NotImplementedError

    def _get_actions(self):
        url = urllib.parse.urljoin(
            settings.API_GATEWAY,
            f'personal/statement/{self.account}/{self.start}/{self.end}'
        )
        return MonobankRequest.get_request_data(url)

    @staticmethod
    def _timedelta_to_timestamp(days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0):
        now = datetime.now()
        start = now - timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        return int(mktime(start.timetuple()))

    @staticmethod
    def _timestamp_to_date(value: int):
        return datetime.fromtimestamp(value)

    def get_receive_operations(self):
        return[operation for operation in self.operations if operation.direction == OperationType.RECEIVE]

    def get_send_operations(self):
        return [operation for operation in self.operations if operation.direction == OperationType.SEND]


class StatementDays(BaseStatement):
    # TODO implement start end validators
    # TODO check max days logic. max 31 days ago or 31 is max interval
    def _interval_converter(self):
        self.start = self._timedelta_to_timestamp(days=self.start)
        self.end = self._timedelta_to_timestamp(days=self.end)


class StatementHours(BaseStatement):
    def _interval_converter(self):
        self.start = self._timedelta_to_timestamp(hours=self.start)
        self.end = self._timedelta_to_timestamp(hours=self.end)
