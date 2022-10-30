class Amount:
    def __set_name__(self, owner, name):
        self.property_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.property_name)

    def __set__(self, instance, value):
        if isinstance(value, int):
            setattr(instance, self.property_name, value/100)
        elif isinstance(value, float):
            setattr(instance, self.property_name, value)


class ObjectList:
    def __init__(self, target_class):
        self._target_cls = target_class

    def __set_name__(self, owner, name):
        self.property_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.property_name)

    def __set__(self, instance, values_list):
        accounts = [
            self._target_cls(value_data)
            for value_data in values_list
        ]
        setattr(instance, self.property_name, accounts)
