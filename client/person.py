from client.account import Account
from client.descriptors import ObjectList
from client.jars import Jar


class Client:
    accounts = ObjectList(Account)
    jars = ObjectList(Jar)

    def __init__(self, client_data):
        self.client_id = client_data.get('clientId')
        self.name = client_data.get('name')
        self.web_hook_url = client_data.get('webHookUrl')
        self.permissions = client_data.get('permissions')
        self.accounts = client_data.get('accounts')
        self.jars = client_data.get('jars')
