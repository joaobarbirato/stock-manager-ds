import zmq
from config import (ADDR, MONITOR_IN_PORT)


class Subscriber:
    """
        ????
    """
    def __init__(self):
        pass

    def buy(self):
        pass

    def sell(self):
        pass
    pass

class Manager:
    """
        Servidor em 
        https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/pyzmqdevices/streamer.html
    """
    def __init__(self):
        self._context = zmq.Context()
        self._socket = context.socket(zmq.PUSH)
        self._socket.connect("tcp://%s:%s" % (MONITOR_IN_PORT, ADDR))

    def create_stock(self, stock_id, stock_name, stock_value):
        pass
