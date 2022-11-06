from datetime import datetime, timedelta

import settings
from statement.statement import Operation


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

    def print_report_data(self):
        print(f'name: {self.name}')
        print(f'first operation at {self.first_operation_date.strftime(settings.DATE_FORMAT)}')
        print(f'last operation at {self.last_operation_date.strftime(settings.DATE_FORMAT)}')
        print(f'total_operation_amount={self.total_operation_amount}')
        print(f'total_cashback_amount={self.total_cashback_amount}')
        print(f'total_commission_amount={self.total_commission_amount}')

    def get_all_amounts(self):
        return [operation.amount for operation in self.operations]

    def get_all_timestamps(self):
        return [operation.time for operation in self.operations]

    def get_all_date(self):
        return [operation.date for operation in self.operations]

    def get_all_balances(self):
        return [operation.balance for operation in self.operations]

    def get_amounts_per_day(self):
        start = self.first_operation_date.date()
        end = self.last_operation_date.date()
        current_date = start
        amount_per_day = {}
        while current_date <= end:
            amount_per_day[current_date.strftime(settings.DATE_FORMAT)] = 0
            current_date += timedelta(days=1)
        for operation in self.operations:
            date = operation.date.strftime(settings.DATE_FORMAT)
            amount_per_day[date] += operation.amount

        return list(amount_per_day.keys()), list(amount_per_day.values())

    def get_balances_per_date(self):
        start = self.first_operation_date.date()
        end = self.last_operation_date.date()
        current_date = start
        operations_per_day = {}
        # while current_date <= end:
        #     operations_per_day[current_date.strftime(settings.DATE_FORMAT)] = None
        #     current_date += timedelta(days=1)
        for current_operation in self.operations:
            date = current_operation.date.strftime(settings.DATE_FORMAT)
            saved_operation = operations_per_day.get(date, current_operation)
            if saved_operation is None:
                operation = current_operation
            else:
                operation = max([saved_operation, current_operation], key=lambda x: x.time)
            operations_per_day[date] = operation
        dates = list(operations_per_day.keys())
        # TODO fill empty days with balance
        # TODO reverse data
        balances = [round(operation.balance, 2) for operation in operations_per_day.values()]
        return dates, balances
