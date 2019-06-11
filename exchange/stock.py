class Stock:
    def __init__(self, name, id_stock, val):
        """
            :param id_stock: String identificadora da bolsa
            :param name: Nome da bolsa
            :param val: Valor inicial da bolsa
        """
        self._id = id_stock
        self._name = name
        self._val = val
        self._old_val = None
        self._status = None

    def _update_status(self):
        self._status = (self._val - self._old_val) / self._old_val
        return self._status

    def update_value(self, value):
        self._old_val = self._val
        self._val = value
        self._update_status()
        return value

    def get_name(self):
        return self._name

    def get_value(self):
        return self._val

    def get_old_value(self):
        return self._old_val

    def get_id(self):
        return self._id

    def to_dict(self):
        return {
            "name": self._name,
            "value": self._val,
            "old value": self._old_val
        }

    def __sub__(self, stk):
        if isinstance(stk, Stock):
            return self._val - stk.get_value()

    def __repr__(self):
        return "<Stock %r>" % self._name
