from enum import Enum

from client.descriptors import Amount, ObjectList


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


class Report:
    def __init__(self, name: str = ''):
        self.name = name
        self.count_operations: int = 0
        self.total_amount: float = 0.0
        self.total_operation_amount: float = 0.0
        self.total_cashback_amount: float = 0.0
        self.total_commission_amount: float = 0.0

    def add_operation(self, operation: Operation):
        self.count_operations += 1
        self.total_amount += operation.amount
        self.total_operation_amount += operation.operation_mount
        self.total_cashback_amount += operation.cashback_amount
        self.total_commission_amount += operation.commission_rate

    def __add__(self, other):
        # if isinstance(other, Report):
        #     raise ValueError
        report = Report('Total report')
        report.count_operations = self.count_operations + other.count_operations
        report.total_amount = round(self.total_amount + other.total_amount, 2)
        report.total_operation_amount = round(self.total_operation_amount + other.total_operation_amount, 2)
        report.total_cashback_amount = round(self.total_cashback_amount + other.total_cashback_amount, 2)
        report.total_commission_amount = round(self.total_commission_amount + other.total_commission_amount, 2)
        return report


class Statement:
    operations = ObjectList(Operation)

    def __init__(self, operations: list):
        self.operations = operations
        self._receive_report = None
        self._send_report = None

    def _create_reports(self):
        receive_report = Report(name='total receive')
        send_report = Report(name='total send')
        for operation in self.operations:
            if operation.direction == OperationType.RECEIVE:
                receive_report.add_operation(operation)
            elif operation.direction == OperationType.SEND:
                receive_report.add_operation(operation)

        return receive_report, send_report

    def get_reports(self):
        if not (self._receive_report and self._send_report):
            self._receive_report, self._send_report = self._create_reports()
        return self._receive_report, self._send_report

    def get_total_report(self):
        receive_report, send_report = self.get_reports()
        return receive_report + send_report
