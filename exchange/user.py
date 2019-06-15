# -*- coding: utf-8 -*-

import zmq
from config import (ADDR, BROKER_IN_PORT)


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
        self._socket = self._context.socket(zmq.PUSH)
        self._socket.connect("tcp://%s:%s" % (BROKER_IN_PORT, ADDR))

    def request_stock_update(self, stock_id, stock_value):
        for i in range(0,10):
            print("Estou tentando mandar #%d" % i)
            self._socket.send(str('#%d' % i).encode())
