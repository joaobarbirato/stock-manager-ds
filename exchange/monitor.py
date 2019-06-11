from exchange.stock import Stock


class PartialMonitor:
    """
        No momento, é basicamente um dict em python, mas criei a classe caso precise adicionar mais coisa
    """
    def __init__(self):
        self._partial_dict =  {}

    def add_stock(self, obj):
        if isinstance(obj, list):
            for stock in obj:
                self._partial_dict[stock.get_id()] = stock

        if isinstance(obj, Stock):
            self._partial_dict[obj.get_id()] = obj

    def get_dict(self):
        return self._partial_dict


class Monitor:
    """
        Monitor q contem tds as stocks
    """
    def __init__(self):
        self._dict = {}
    
    def update_stock(self, stock):
        if isinstance(stock, Stock):
            if stock.get_id() in self._dict:
                self._dict[stock.get_id()].update_value(stock.get_value())
            else:
                self._dict[stock.get_id()] = stock

    def response_partial_monitor(self, list_id):
        """
            :param list_id lista de ids de stocks 
        """
        pm = PartialMonitor()
        pm.add_stock(list_id)
        return pm.get_dict()
