from client.descriptors import Amount


class Jar:
    balance = Amount()
    goal = Amount()

    def __init__(self, jars_data: dict):
        self.id = jars_data.get('id')
        self.sendId = jars_data.get('sendId')
        self.title = jars_data.get('title')
        self.description = jars_data.get('description')
        self.currencyCode = jars_data.get('currencyCode')
        self.balance = jars_data.get('balance', 0)
        self.goal = jars_data.get('goal', 0)
