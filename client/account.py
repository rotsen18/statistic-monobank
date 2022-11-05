from dataclasses import dataclass

from client.descriptors import Amount, ObjectList


@dataclass
class MaskedPan:
    value: str


class Account:
    balance = Amount()
    credit_limit = Amount()
    masked_pans = ObjectList(MaskedPan)

    def __init__(self, account_data: dict):
        self.id = account_data.get('id')
        self.send_id = account_data.get('sendId')
        self.balance = account_data.get('balance', 0)
        self.credit_limit = account_data.get('creditLimit', 0)
        self.type = account_data.get('type')
        self.currency_code = account_data.get('currencyCode')
        self.cashback_type = account_data.get('cashbackType')
        self.masked_pans = account_data.get('maskedPan')
        self.iban = account_data.get('iban')

    def __str__(self):
        return self.id
